import struct, hashlib
H=lambda b:hashlib.sha256(b).hexdigest()
MASK=(1<<64)-1

def select(elf,lo,size,code,kind):
 regs=[0]*11;regs[2 if kind=='name' else 1]=code;pc=lo+8;trace=[]
 for _ in range(256):
  assert lo<=pc<lo+size
  trace.append(pc);op,rs,off,imm=struct.unpack('<BBhi',elf.at(pc,8));d=rs&15;src=rs>>4
  if op==0x18:
   b=elf.at(pc,16);regs[d]=struct.unpack_from('<I',b,4)[0]+(struct.unpack_from('<I',b,12)[0]<<32);pc+=16
  elif op==0xb7:regs[d]=imm;pc+=8
  elif op==0xbf:regs[d]=regs[src];pc+=8
  elif op==0x05:pc+=8+8*off
  elif op in (0x15,0x55,0x65,0x75,0x25,0x35,0xa5,0xb5):
   x=regs[d];take={0x15:x==imm,0x55:x!=imm,0x65:x>imm,0x75:x>=imm,0x25:x>imm,0x35:x>=imm,0xa5:x<imm,0xb5:x<=imm}[op];pc+=8+(8*off if take else 0)
  elif op==0x85 and kind=='name':return dict(pointer=regs[2],length=regs[3],trace=trace)
  elif op==0x7b and kind=='message':
   pointer,length=struct.unpack('<QQ',elf.at(regs[1],16));assert pointer & 0xffffffff == 0 and elf.relocations[regs[1]]['type']==8;pointer >>= 32;return dict(descriptor=regs[1],pointer=pointer,length=length,trace=trace)
  else:raise AssertionError((pc,hex(op)))
 raise AssertionError('selector did not reach terminal')

def name_value(e,start,size,variant):
    # Bounded, call-free decoding of a single selector's normal allocation path.
    # Synthetic memory exists only in this read-only analysis; it is not a VM or
    # build input and is not evidence about allocation failure or other callers.
    regs=[0]*11;regs[1]=0x1000;regs[2]=variant;regs[3]=0x300006000;mem={}
    def store(addr,value,n):
        for i,b in enumerate((value & ((1<<(n*8))-1)).to_bytes(n,'little')):mem[addr+i]=b
    def load(addr,n):
        assert all(addr+i in mem for i in range(n)),(addr,n)
        return int.from_bytes(bytes(mem[addr+i] for i in range(n)),'little')
    store(0x300000000,regs[3],8);pc=start+32;trace=[]
    for _ in range(512):
        assert start<=pc<start+size;trace.append(pc)
        op,rs,off,imm=struct.unpack('<BBhi',e.at(pc,8));d=rs&15;src=rs>>4
        if op==0x18:
            b=e.at(pc,16);regs[d]=struct.unpack_from('<I',b,4)[0]+(struct.unpack_from('<I',b,12)[0]<<32);pc+=16
        elif op==0xbf:regs[d]=regs[src];pc+=8
        elif op==0xb7:regs[d]=imm & MASK;pc+=8
        elif op in (0x07,0x17,0x57):
            regs[d]=({0x07:lambda x:x+imm,0x17:lambda x:x-imm,0x57:lambda x:x&(imm&MASK)}[op](regs[d]))&MASK;pc+=8
        elif op==0x05:pc+=8+off*8
        elif op&7==5 and op!=0x95 and op!=0x85 and op!=0x8d:
            right=regs[src] if op&8 else imm&MASK;x=regs[d];kind=op&0xf0
            sx=x if x<(1<<63) else x-(1<<64);sy=right if right<(1<<63) else right-(1<<64)
            take={0x10:x==right,0x20:x>right,0x30:x>=right,0x50:x!=right,0x60:sx>sy,0x70:sx>=sy,0xa0:x<right,0xb0:x<=right}[kind]
            pc+=8+(off*8 if take else 0)
        elif op&7 in (2,3):
            n={0:4,8:2,16:1,24:8}[op&24];store((regs[d]+off)&MASK,regs[src] if op&7==3 else imm,n);pc+=8
        elif op&7==1:
            n={0:4,8:2,16:1,24:8}[op&24];regs[d]=load((regs[src]+off)&MASK,n);pc+=8
        elif op==0x95:
            cap=load(0x1000,8);ptr=load(0x1008,8);length=load(0x1010,8);assert cap==length
            data=bytes(mem[ptr+i] for i in range(length));return dict(bytes=data.decode(),length=length,trace=trace)
        else:raise AssertionError(('unexpected instruction or external call on bounded name path',pc,hex(op)))
    raise AssertionError('name selector failed to return')

def message_value(e,start,size,variant):
    regs=[0]*11;regs[2]=variant;pc=start+40;trace=[]
    for _ in range(256):
        assert start<=pc<start+size;trace.append(pc);op,rs,off,imm=struct.unpack('<BBhi',e.at(pc,8));d=rs&15
        if op==0x18:
            b=e.at(pc,16);regs[d]=struct.unpack_from('<I',b,4)[0]+(struct.unpack_from('<I',b,12)[0]<<32);pc+=16
        elif op==0xb7:regs[d]=imm;pc+=8
        elif op==0x05:pc+=8+off*8
        elif op in (0x15,0x65):pc+=8+(off*8 if (regs[d]==imm if op==0x15 else regs[d]>imm) else 0)
        elif op==0x8d:
            raw=e.at(regs[2],regs[3]);return dict(pointer=regs[2],length=regs[3],bytes=raw.decode(),sha256=H(raw),trace=trace)
        else:raise AssertionError((pc,hex(op)))
    raise AssertionError('message selector did not reach formatter')
