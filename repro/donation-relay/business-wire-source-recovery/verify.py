#!/usr/bin/env python3
"""Recompute complete Rust-output ledgers; no VM or captured program execution."""
from pathlib import Path
import argparse,gzip,hashlib,json,importlib.util,tomllib,tarfile
P=Path(__file__).resolve().parent;ROOT=P.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def main(current=False):
 for n,h in read(P/'manifest.json').items():assert H((P/n).read_bytes())==h,n
 for n,h in read(P/'external-inputs.json').items():assert H((ROOT/n).read_bytes())==h,n
 spec=importlib.util.spec_from_file_location('business_wire_elf',P/'analyze.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 for row in read(P/'primary-source.json'):
  archive=ROOT/row['archive'];assert H(archive.read_bytes())==row['archive_sha256']
  with tarfile.open(archive,'r:gz') as t:b=t.extractfile(row['member']).read()
  assert H(b)==row['sha256'] and b==(P/row['path']).read_bytes()
 prior=read(ROOT/'repro/donation-relay/anchor-framework-source-recovery/coordinate/match-ledger.json.gz');old=tomllib.loads((ROOT/'repro/donation-relay/anchor-framework-source-recovery/coordinate/source/Cargo.lock').read_text())['package'];results=[]
 for stage,expected,gains in [('typed-wire',308,[74,78,170,388,443]),('framework-writer',309,[74,77,78,170,388,443])]:
  p=P/stage;source=read(p/'source-manifest.json');assert len(source)==28
  assert all(H((p/'source'/n).read_bytes())==h for n,h in source.items())
  assert set(source)=={str(f.relative_to(p/'source')) for f in (p/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])}
  assert tomllib.loads((p/'source/Cargo.lock').read_text())['package']==old
  b=read(p/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256']
  assert H((p/'candidate.so').read_bytes())==b['candidate_sha256'] and H((p/'unstripped.so').read_bytes())==b['unstripped_sha256']
  class View:
   def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else p/n
  outputs=a.analyze(View())
  for n,v in outputs.items():assert v==read(p/(n if n.endswith('.gz') else n+'.gz')),n
  summary=outputs['comparison-summary.json'];assert summary['original_normalized_match_windows']==expected and summary['original_raw_match_windows']==75 and not summary['whole_file_equal']
  ledger=outputs['match-ledger.json'];assert [x['ordinal'] for x,y in zip(ledger,prior) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']]==gains
  assert not any(not x['normalized_candidate_indices'] and y['normalized_candidate_indices'] for x,y in zip(ledger,prior))
  results.append(dict(stage=stage,normalized_windows=expected,gained=gains,lost=[]))
 for stage in ['private-module-failure','root-export-failure']:
  p=P/stage;b=read(p/'build-result.json');assert b['returncode']==101 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256'];assert all(H((p/'source'/n).read_bytes())==h for n,h in read(p/'source-manifest.json').items())
 selected=P/'framework-writer';proof=P/'current-source-proof';b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256'];assert read(proof/'source-manifest.json')==read(selected/'source-manifest.json')
 for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
 if current:assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in read(proof/'source-manifest.json').items())
 print(json.dumps(dict(verified=True,source_builds=3,builds=results,current_source_checked=current,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');args=ap.parse_args();main(args.current)
