#!/usr/bin/env python3
"""Offline Rust-output, full-body/data/provenance verifier. No VM execution."""
from pathlib import Path
import argparse,gzip,hashlib,json,importlib.util,tomllib,tarfile,struct
P=Path(__file__).resolve().parent;ROOT=P.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(current=False):
 for n,h in read(P/'manifest.json').items():assert H((P/n).read_bytes())==h,n
 for n,h in read(P/'external-inputs.json').items():assert H((ROOT/n).read_bytes())==h,n
 a=mod('whitelist_elf',P/'analyze.py');original=a.Elf((ROOT/'evidence/dependencies/donation_relay/deployed.so').read_bytes());windows=read(P/'original-windows.json');prior=read(ROOT/'repro/donation-relay/business-wire-source-recovery/framework-writer/match-ledger.json.gz');old=tomllib.loads((ROOT/'repro/donation-relay/business-wire-source-recovery/framework-writer/source/Cargo.lock').read_text())['package'];results=[];positive=prior
 expected=dict(context=322,state=324,body=325,cgu16=247,boundaries=326,constants=328)
 for stage in read(P/'stages.json'):
  p=P/stage;source=read(p/'source-manifest.json');assert len(source)==(29 if stage=='context' else 30)
  assert all(H((p/'source'/n).read_bytes())==h for n,h in source.items())
  assert set(source)=={str(f.relative_to(p/'source')) for f in (p/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])}
  assert tomllib.loads((p/'source/Cargo.lock').read_text())['package']==old
  b=read(p/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256']
  assert H((p/'candidate.so').read_bytes())==b['candidate_sha256'] and H((p/'unstripped.so').read_bytes())==b['unstripped_sha256']
  class View:
   def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else p/n
  outputs=a.analyze(View())
  for n,v in outputs.items():assert v==read(p/(n if n.endswith('.gz') else n+'.gz')),n
  summary=outputs['comparison-summary.json'];ledger=outputs['match-ledger.json'];assert summary['original_normalized_match_windows']==expected[stage] and not summary['whole_file_equal']
  if stage!='cgu16':assert not any(not x['normalized_candidate_indices'] and y['normalized_candidate_indices'] for x,y in zip(ledger,positive));positive=ledger
  else:
   assert not any(x['normalized_candidate_indices'] and not y['normalized_candidate_indices'] for x,y in zip(ledger,positive))
   assert sum(not x['normalized_candidate_indices'] and bool(y['normalized_candidate_indices']) for x,y in zip(ledger,positive))==78
  results.append(dict(stage=stage,normalized_windows=expected[stage],raw_windows=summary['original_raw_match_windows']))
 selected=P/'constants';latest=read(selected/'match-ledger.json.gz');gained=[x['ordinal'] for x,y in zip(latest,prior) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']];assert gained==[3,12,27,79,101,105,156,157,158,165,166,177,188,291,292,293,319,321,323]
 for record in read(P/'diagnostic-proofs.json'):
  pc=record['pointer_instruction'];assert any(x['pc']==pc and x['target']==record['pointer'] for x in windows[record['ordinal']]['data_references'])
  for off,raw in record['instructions'].items():assert original.at(pc+int(off),len(bytes.fromhex(raw))).hex()==raw
  assert struct.unpack_from('<I',original.at(pc,16),4)[0]==record['pointer']
  for off,expected_value,op in [(24,record['error_code'],0x62),(40,record['line'],0x62),(48,record['path_length'],0x7a)]:
   code,regs,stack,value=struct.unpack('<BBhi',original.at(pc+off,8));assert code==op and regs==10 and value==expected_value
  data=original.at(record['pointer'],record['path_length']);assert data.decode()==record['path'] and H(data)==record['path_sha256']
 registry={x['name']+'-'+x['version']+'.crate':x['checksum'] for x in old if 'source' in x}
 for row in read(P/'primary-source.json'):
  archive=P/row['archive'];assert H(archive.read_bytes())==row['archive_sha256']==registry[archive.name]
  with tarfile.open(archive,'r:gz') as t:data=t.extractfile(row['member']).read()
  assert H(data)==row['sha256'] and data==(P/row['path']).read_bytes()
 failure=P/'included-doc-failure';b=read(failure/'build-result.json');assert b['returncode']==101 and b['source_unchanged'] and H((failure/'build.log').read_bytes())==b['log_sha256'];assert all(H((failure/'source'/n).read_bytes())==h for n,h in read(failure/'source-manifest.json').items())
 proof=P/'current-source-proof';b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256'];assert read(proof/'source-manifest.json')==read(selected/'source-manifest.json')
 for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
 class LedgerText:
  def read_text(self):return gzip.decompress((selected/'candidate-function-ledger.json.gz').read_bytes()).decode()
 class SelectorView:
  def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else LedgerText() if n=='candidate-function-ledger.json' else selected/n
 selectors=mod('whitelist_selectors',selected/'check-selectors.py');selectors.P=SelectorView();assert {n:selectors.derive(n) for n in ['owned','anchor']}==read(selected/'selector-proof-both77.json')
 program=mod('whitelist_program_selectors',selected/'check-program-data.py');program.P=SelectorView();assert program.derive()==read(selected/'program-data-proof-all34.json')
 if current:assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in read(proof/'source-manifest.json').items())
 print(json.dumps(dict(verified=True,successful_source_builds=7,builds=results,final_gained=gained,current_source_checked=current,selector_records_rederived=188,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');args=ap.parse_args();main(args.current)
