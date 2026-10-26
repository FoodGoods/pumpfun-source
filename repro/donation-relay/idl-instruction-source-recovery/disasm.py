#!/usr/bin/env python3
import importlib.util,struct
from pathlib import Path
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('elf_analysis',P/'analyze.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
def render(elf,start,end):
 out=[];pc=start
 while pc<end:
  b=elf.at(pc,8);op,r,off,imm=struct.unpack('<BBhi',b);d=r&15;sr=r>>4;n=8;src=f'r{sr}' if op&8 else str(imm)
  if op==24:
   n=16;b=elf.at(pc,n);v=struct.unpack_from('<I',b,4)[0]+(struct.unpack_from('<I',b,12)[0]<<32);t=f'r{d} = {v} (lddw)'
  elif op==133:
   rel=elf.relocations.get(pc);t='external '+str(rel) if rel and rel['type']==10 else 'call '+str(pc+8+imm*8)
  elif op==149:t='exit'
  elif op==141:t='callx '+str(imm)
  elif op&7 in (4,7):t=f'r{d} '+{0:'+=',16:'-=',32:'*=',48:'/=',64:'|=',80:'&=',96:'<<=',112:'>>=',128:'neg',144:'%=',160:'^=',176:'=',192:'s>>=',208:'endian'}.get(op&240,'?')+f' {src}'+(' (32)' if op&7==4 else '')
  elif op&7 in (5,6):
   name={0:'goto',16:'==',32:'>',48:'>=',64:'&',80:'!=',96:'s>',112:'s>=',160:'<',176:'<=',192:'s<',208:'s<='}.get(op&240,'?');t=f'if r{d} {name} {src} -> {pc+8+off*8}' if op&240 else f'goto {pc+8+off*8}'
  elif op&7==1:t=f'r{d} = u'+str({0:32,8:16,16:8,24:64}[op&24])+f'[r{sr}{off:+}]'
  elif op&7 in (2,3):t='u'+str({0:32,8:16,16:8,24:64}[op&24])+f'[r{d}{off:+}] = '+(f'r{sr}' if op&7==3 else str(imm))
  else:t=f'unknown {op}'
  out.append(f'{pc}: {b.hex():<32} {t}');pc+=n
 return '\n'.join(out)+'\n'
