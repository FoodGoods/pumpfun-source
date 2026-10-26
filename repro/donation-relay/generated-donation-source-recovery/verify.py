#!/usr/bin/env python3
"""Read-only full Rust output, data, registry and source verification; no VM."""
from pathlib import Path
import argparse,hashlib,json,gzip,importlib.util,tomllib,tarfile,struct
P=Path(__file__).resolve().parent;ROOT=P.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(current=False,registry_source=False):
 for n,h in read(P/'manifest.json').items():assert H((P/n).read_bytes())==h,n
 for n,h in read(P/'external-inputs.json').items():assert H((ROOT/n).read_bytes())==h,n
 a=mod('generated_donation_elf',P/'analyze.py');prior=read(ROOT/'repro/donation-relay/whitelist-generated-source-recovery/constants/match-ledger.json.gz');old=tomllib.loads((ROOT/'repro/donation-relay/whitelist-generated-source-recovery/constants/source/Cargo.lock').read_text())['package'];reg=lambda ps:{(x['name'],x['version']):x for x in ps if 'source' in x};oldreg=reg(old);summaries=[];ledgers={}
 for stage,expected,inputs in [('pruned',328,30),('qualified',361,34),('compared',361,34)]:
  p=P/stage;source=read(p/'source-manifest.json');assert len(source)==inputs and all(H((p/'source'/n).read_bytes())==h for n,h in source.items())
  assert set(source)=={str(f.relative_to(p/'source')) for f in (p/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])}
  b=read(p/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256'];assert H((p/'candidate.so').read_bytes())==b['candidate_sha256'] and H((p/'unstripped.so').read_bytes())==b['unstripped_sha256']
  class View:
   def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else p/n
  outputs=a.analyze(View())
  for n,v in outputs.items():assert v==read(p/(n if n.endswith('.gz') else n+'.gz')),n
  summary=outputs['comparison-summary.json'];ledger=outputs['match-ledger.json'];ledgers[stage]=ledger;assert summary['original_normalized_match_windows']==expected and not summary['whole_file_equal']
  assert not any(not x['normalized_candidate_indices'] and y['normalized_candidate_indices'] for x,y in zip(ledger,prior))
  newreg=reg(tomllib.loads((p/'source/Cargo.lock').read_text())['package']);assert all(newreg.get(k)==v for k,v in oldreg.items())
  assert set(newreg)-set(oldreg)==(set() if stage=='pruned' else {('anchor-spl','0.31.1'),('spl-associated-token-account','6.0.0'),('spl-associated-token-account-client','2.0.0')})
  summaries.append(dict(stage=stage,normalized_windows=expected,raw_windows=summary['original_raw_match_windows'],gained=sum(bool(x['normalized_candidate_indices']) and not y['normalized_candidate_indices'] for x,y in zip(ledger,prior))))
 assert all(bool(x['normalized_candidate_indices'])==bool(y['normalized_candidate_indices']) for x,y in zip(ledgers['pruned'],prior))
 assert all(bool(x['normalized_candidate_indices'])==bool(y['normalized_candidate_indices']) for x,y in zip(ledgers['qualified'],ledgers['compared']))
 for stage in ['constraint-order-failure','macro-name-failure','unrelated-qualification-failure']:
  p=P/stage;b=read(p/'build-result.json');assert b['returncode']==101 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256'];assert all(H((p/'source'/n).read_bytes())==h for n,h in read(p/'source-manifest.json').items())
 # Initial finite state comparison stopped at a real, retained log mismatch.
 negative=read(P/'qualified/donate-context-cases.json');assert not negative['all_requested_completed'] and len(negative['cases'])==6 and negative['passed']==5
 assert negative['cases'][-1]['name']=='epoch_tracker/mint' and negative['cases'][-1]['mismatches']['candidate']==['logs']
 assert negative['binary_hashes']['candidate']==H((P/'qualified/candidate.so').read_bytes())
 selected=P/'compared';proof=P/'current-source-proof';b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256'];assert read(proof/'source-manifest.json')==read(selected/'source-manifest.json')
 for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
 newreg=reg(tomllib.loads((selected/'source/Cargo.lock').read_text())['package']);registry={name+'-'+version+'.crate':v['checksum'] for (name,version),v in newreg.items()}
 for row in read(P/'primary-source.json'):
  archive=P/row['archive'];assert H(archive.read_bytes())==row['archive_sha256']==registry[archive.name]
  with tarfile.open(archive,'r:gz') as tar:data=tar.extractfile(row['member']).read()
  assert data==(P/row['path']).read_bytes() and H(data)==row['sha256']
 metadata=next(json.loads(line) for line in (selected/'resolve.log').read_text().splitlines() if line.startswith('{"packages":'));packages={(x['name'],x['version']):x for x in metadata['packages'] if x['source'] is not None};audit=read(P/'registry-source-audit.json');assert len(audit)==176 and sum(x['exact_files'] for x in audit)==3976 and set(packages)=={(x['name'],x['version']) for x in audit}
 for row in audit:
  assert row['archive_sha256']==newreg[(row['name'],row['version'])]['checksum'] and row['no_unexpected_files']
  if registry_source:
   source=Path(packages[(row['name'],row['version'])]['manifest_path']).parent;archive=next((ROOT/'work/relay-anchor-idl-scaffold/cargo-home/registry/cache').glob('*/'+row['name']+'-'+row['version']+'.crate'));assert H(archive.read_bytes())==row['archive_sha256'];known=set();total=0
   with tarfile.open(archive,'r:gz') as tar:
    for entry in tar:
     if not entry.isfile():continue
     name=entry.name.split('/',1)[1];data=tar.extractfile(entry).read();assert (source/name).read_bytes()==data;known.add(name);total+=len(data)
   assert len(known)==row['exact_files'] and total==row['exact_bytes'];assert not ({str(f.relative_to(source)) for f in source.rglob('*') if f.is_file()}-known-{'.cargo-checksum.json','.cargo-ok','.DS_Store'})
 # Recompute the limited constructor-pattern scan, not a claim of all metadata.
 original=a.Elf((ROOT/'evidence/dependencies/donation_relay/deployed.so').read_bytes());diagnostics=[]
 for window in read(P/'original-windows.json'):
  for r in window['data_references']:
   pc=r['pc']
   try:
    op,regs,stack,code=struct.unpack('<BBhi',original.at(pc+24,8));op2,regs2,stack2,line=struct.unpack('<BBhi',original.at(pc+40,8));op3,regs3,stack3,length=struct.unpack('<BBhi',original.at(pc+48,8))
    if (op,regs,op2,regs2,op3,regs3)!=(0x62,10,0x62,10,0x7a,10) or not 20<=length<=160:continue
    raw=original.at(r['target'],length)
    if raw.startswith(b'programs/contracts/src/') and raw.endswith(b'.rs'):diagnostics.append(dict(ordinal=window['ordinal'],pc=pc,pointer=r['target'],code=code,path=raw.decode(),line=line,length=length))
   except (ValueError,struct.error):pass
 assert diagnostics==read(P/'pruned/decoded-diagnostics.json') and len(diagnostics)==59
 class LedgerText:
  def read_text(self):return gzip.decompress((selected/'candidate-function-ledger.json.gz').read_bytes()).decode()
 class SelectorView:
  def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else LedgerText() if n=='candidate-function-ledger.json' else selected/n
 selectors=mod('generated_donation_selectors',selected/'check-selectors.py');selectors.P=SelectorView();assert {n:selectors.derive(n) for n in ['owned','anchor']}==read(selected/'selector-proof-both77.json')
 program=mod('generated_donation_program_selectors',selected/'check-program-data.py');program.P=SelectorView();assert program.derive()==read(selected/'program-data-proof-all34.json')
 if current:assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in read(proof/'source-manifest.json').items())
 print(json.dumps(dict(verified=True,successful_source_builds=4,builds=summaries,current_source_checked=current,registry_sources_checked=registry_source,diagnostic_records=59,selector_records=188,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');ap.add_argument('--check-registry-source',action='store_true');args=ap.parse_args();main(args.current,args.check_registry_source)
