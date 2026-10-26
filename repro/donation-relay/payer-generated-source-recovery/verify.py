#!/usr/bin/env python3
"""Read-only source/output/full-body/data/call-map checks; no VM execution."""
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
 a=mod('payer_generated_elf',P/'analyze.py');selected=P/'payer';source=read(selected/'source-manifest.json');assert len(source)==36 and all(H((selected/'source'/n).read_bytes())==h for n,h in source.items())
 assert set(source)=={str(f.relative_to(selected/'source')) for f in (selected/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])}
 b=read(selected/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((selected/'build.log').read_bytes())==b['log_sha256'];assert H((selected/'candidate.so').read_bytes())==b['candidate_sha256'] and H((selected/'unstripped.so').read_bytes())==b['unstripped_sha256']
 class View:
  def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else selected/n
 outputs=a.analyze(View())
 for n,v in outputs.items():assert v==read(selected/(n if n.endswith('.gz') else n+'.gz')),n
 summary=outputs['comparison-summary.json'];assert summary['original_normalized_match_windows']==375 and summary['original_raw_match_windows']==77 and not summary['whole_file_equal'];ledger=outputs['match-ledger.json'];prior=read(ROOT/'repro/donation-relay/donation-layout-source-recovery/pubkey/match-ledger.json.gz');assert not any(not x['normalized_candidate_indices'] and y['normalized_candidate_indices'] for x,y in zip(ledger,prior));fs=outputs['candidate-function-ledger.json'];gains=[dict(ordinal=x['ordinal'],bytes=x['bytes'],candidate_names=[fs[i]['names'] for i in x['normalized_candidate_indices']]) for x,y in zip(ledger,prior) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']];assert gains==read(P/'gains.json') and [x['ordinal'] for x in gains]==[138,139,140,141]
 old=tomllib.loads((ROOT/'repro/donation-relay/donation-layout-source-recovery/pubkey/source/Cargo.lock').read_text())['package'];assert tomllib.loads((selected/'source/Cargo.lock').read_text())['package']==old
 # Correct previously misidentified window139 using decoded actual call edges.
 original=a.Elf((ROOT/'evidence/dependencies/donation_relay/deployed.so').read_bytes());windows=read(P/'original-windows.json');of=outputs['original-function-ledger.json'];rows=read(P/'corrected-call-map.json');assert [(r['wrapper'],r['parser'],r['closures'],r['exit']) for r in rows]==[(178,121,[122,123,124],125),(179,135,[136,137,124],125),(182,138,[139,140,124],141)]
 idl={x['name']:x for x in read(P/'captured-idl.json')['instructions']}
 for row in rows:
  assert row['instruction'] in idl;log=('Instruction: '+''.join(x.capitalize() for x in row['instruction'].split('_'))).encode();wrapper=of[row['wrapper']];targets={x['target'] for x in wrapper['direct_calls']};assert windows[row['parser']]['start'] in targets and windows[row['exit']]['start'] in targets
  assert any(original.at(x['target'],len(log))==log for x in wrapper['data_references'])
  parser_targets={x['target'] for x in of[row['parser']]['direct_calls']}
  for closure in row['closures']:assert windows[closure]['start'] in parser_targets and ledger[closure]['normalized_candidate_indices']
  assert ledger[row['parser']]['normalized_candidate_indices'] and ledger[row['exit']]['normalized_candidate_indices']
 assert windows[139]['start'] not in {x['target'] for x in of[179]['direct_calls']} and windows[139]['start'] in {x['target'] for x in of[138]['direct_calls']}
 registry={x['name']+'-'+x['version']+'.crate':x['checksum'] for x in old if 'source' in x}
 for row in read(P/'primary-source.json'):
  archive=P/row['archive'];assert H(archive.read_bytes())==row['archive_sha256']==registry[archive.name]
  with tarfile.open(archive,'r:gz') as tar:data=tar.extractfile(row['member']).read()
  assert data==(P/row['path']).read_bytes() and H(data)==row['sha256']
 proof=P/'current-source-proof';b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256'];assert read(proof/'source-manifest.json')==source
 for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
 class LedgerText:
  def read_text(self):return gzip.decompress((selected/'candidate-function-ledger.json.gz').read_bytes()).decode()
 class SelectorView:
  def __truediv__(self,n):return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else LedgerText() if n=='candidate-function-ledger.json' else selected/n
 selectors=mod('payer_generated_selectors',selected/'check-selectors.py');selectors.P=SelectorView();assert {n:selectors.derive(n) for n in ['owned','anchor']}==read(selected/'selector-proof-both77.json')
 program=mod('payer_generated_program_selectors',selected/'check-program-data.py');program.P=SelectorView();assert program.derive()==read(selected/'program-data-proof-all34.json')
 if current:assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in source.items())
 print(json.dumps(dict(verified=True,successful_source_builds=2,normalized_windows=375,raw_windows=77,gained=[138,139,140,141],lost=[],corrected_call_map=True,current_source_checked=current,selector_records=188,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');args=ap.parse_args();main(args.current)
