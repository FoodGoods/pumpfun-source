#!/usr/bin/env python3
"""Read-only complete Rust-output and metadata verification; no VM execution."""
from pathlib import Path
import argparse,hashlib,json,gzip,importlib.util,tomllib,tarfile
P=Path(__file__).resolve().parent;ROOT=P.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(current=False):
 for n,h in read(P/'manifest.json').items():assert H((P/n).read_bytes())==h,n
 for n,h in read(P/'external-inputs.json').items():assert H((ROOT/n).read_bytes())==h,n
 a=mod('donation_layout_elf',P/'analyze.py');prior=read(ROOT/'repro/donation-relay/generated-donation-source-recovery/compared/match-ledger.json.gz');old=tomllib.loads((ROOT/'repro/donation-relay/generated-donation-source-recovery/compared/source/Cargo.lock').read_text())['package'];summaries=[];positive=prior;derived={}
 for stage,expected,inputs,gained in [('pruned',361,34,[]),('boxed',363,34,[34,35]),('program-types',365,34,[121,135]),('pubkey',371,35,[17,18,28,125,136,137])]:
  p=P/stage;source=read(p/'source-manifest.json');assert len(source)==inputs and all(H((p/'source'/n).read_bytes())==h for n,h in source.items())
  assert set(source)=={str(f.relative_to(p/'source')) for f in (p/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])}
  b=read(p/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256'];assert H((p/'candidate.so').read_bytes())==b['candidate_sha256'] and H((p/'unstripped.so').read_bytes())==b['unstripped_sha256']
  class View:
   def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else p/n
  outputs=a.analyze(View());derived[stage]=outputs
  for n,v in outputs.items():assert v==read(p/(n if n.endswith('.gz') else n+'.gz')),n
  summary=outputs['comparison-summary.json'];ledger=outputs['match-ledger.json'];assert summary['original_normalized_match_windows']==expected and summary['original_raw_match_windows']==77 and not summary['whole_file_equal']
  assert not any(not x['normalized_candidate_indices'] and y['normalized_candidate_indices'] for x,y in zip(ledger,positive))
  assert [x['ordinal'] for x,y in zip(ledger,positive) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']]==gained;positive=ledger
  assert tomllib.loads((p/'source/Cargo.lock').read_text())['package']==old
  summaries.append(dict(stage=stage,normalized_windows=expected,gained=gained,lost=[]))
 selected=P/'pubkey';latest=derived['pubkey']['match-ledger.json'];fs=derived['pubkey']['candidate-function-ledger.json'];gains=[dict(ordinal=x['ordinal'],bytes=x['bytes'],candidate_names=[fs[i]['names'] for i in x['normalized_candidate_indices']]) for x,y in zip(latest,prior) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']];assert gains==read(P/'gains.json')
 for ordinal in [17,18,34,35,121,125,135,136,137]:assert latest[ordinal]['normalized_candidate_indices']
 proof=P/'current-source-proof';b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256'];assert read(proof/'source-manifest.json')==read(selected/'source-manifest.json')
 for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
 registry={x['name']+'-'+x['version']+'.crate':x['checksum'] for x in old if 'source' in x}
 for row in read(P/'primary-source.json'):
  archive=P/row['archive'];assert H(archive.read_bytes())==row['archive_sha256']==registry[archive.name]
  with tarfile.open(archive,'r:gz') as tar:data=tar.extractfile(row['member']).read()
  assert data==(P/row['path']).read_bytes() and H(data)==row['sha256']
 class LedgerText:
  def read_text(self):return gzip.decompress((selected/'candidate-function-ledger.json.gz').read_bytes()).decode()
 class SelectorView:
  def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else LedgerText() if n=='candidate-function-ledger.json' else selected/n
 selectors=mod('donation_layout_selectors',selected/'check-selectors.py');selectors.P=SelectorView();assert {n:selectors.derive(n) for n in ['owned','anchor']}==read(selected/'selector-proof-both77.json')
 program=mod('donation_layout_program_selectors',selected/'check-program-data.py');program.P=SelectorView();assert program.derive()==read(selected/'program-data-proof-all34.json')
 if current:assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in read(proof/'source-manifest.json').items())
 print(json.dumps(dict(verified=True,successful_source_builds=5,builds=summaries,current_source_checked=current,selector_records=188,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');args=ap.parse_args();main(args.current)
