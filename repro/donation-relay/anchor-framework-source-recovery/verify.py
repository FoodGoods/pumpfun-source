#!/usr/bin/env python3
"""Recompute complete body ledgers from genuine Rust outputs, without execution."""
from pathlib import Path
import argparse,hashlib,json,gzip,importlib.util,tomllib,tarfile
P=Path(__file__).resolve().parent;ROOT=P.parents[2];H=lambda b:hashlib.sha256(b).hexdigest()
def read(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def main(current=False,registry_source=False):
 for n,h in read(P/'manifest.json').items():assert H((P/n).read_bytes())==h,n
 for n,h in read(P/'external-inputs.json').items():assert H((ROOT/n).read_bytes())==h,n
 spec=importlib.util.spec_from_file_location('anchor_source_analysis',P/'analyze.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 for row in read(P/'primary-source.json'):
  archive=P/'primary/archives'/row['archive_name'];assert H(archive.read_bytes())==row['archive_sha256']
  with tarfile.open(archive,'r:gz') as t:data=t.extractfile(row['archive_member']).read()
  assert data==(P/row['path']).read_bytes() and H(data)==row['sha256']
 results=[]
 for stage in read(P/'stages.json'):
  p=P/stage;inventory=read(p/'source-manifest.json');sources=read(p/'compiled-source-manifest.json');assert sources=={n:h for n,h in inventory.items() if not n.startswith('target/') and (n.endswith('.rs') or Path(n).name in ['Cargo.toml','Cargo.lock'])};assert all(H((p/'source'/n).read_bytes())==h for n,h in sources.items())
  expected={str(f.relative_to(p/'source')) for f in (p/'source').rglob('*') if f.is_file() and (f.suffix=='.rs' or f.name in ['Cargo.toml','Cargo.lock'])};assert set(sources)==expected
  b=read(p/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((p/'build.log').read_bytes())==b['log_sha256']
  assert H((p/'candidate.so').read_bytes())==b['candidate_sha256'] and H((p/'unstripped.so').read_bytes())==b['unstripped_sha256']
  # Analyzer input paths are a read-only view; no copying/patching target bytes.
  class View:
   def __truediv__(self,n):
    return ROOT/'evidence/dependencies/donation_relay/deployed.so' if n=='original.so' else P/'original-windows.json' if n=='original-windows.json' else p/n
  outputs=a.analyze(View())
  for n,v in outputs.items():assert v==read(p/(n if n.endswith('.gz') else n+'.gz')),n
  summary=outputs['comparison-summary.json'];assert not summary['whole_file_equal']
  locked={(x['name'],x['version']):x['checksum'] for x in tomllib.loads((p/'source/Cargo.lock').read_text())['package'] if 'source' in x}
  archives=read(p/'registry-archives.json');assert {(x['name'],x['version']):x['checksum'] for x in archives}==locked
  delta=read(p/'delta.json');old=read(ROOT/'repro/donation-relay/idl-instruction-source-recovery/payload-io-boundary/match-ledger.json.gz');new=outputs['match-ledger.json'];cf=outputs['candidate-function-ledger.json']
  expected=[dict(ordinal=x['ordinal'],bytes=x['bytes'],candidate_names=[cf[i]['names'] for i in x['normalized_candidate_indices']]) for x,y in zip(new,old) if x['normalized_candidate_indices'] and not y['normalized_candidate_indices']]
  assert expected==delta['gained'];assert delta['lost']==[x['ordinal'] for x,y in zip(new,old) if not x['normalized_candidate_indices'] and y['normalized_candidate_indices']]
  results.append(dict(stage=stage,normalized_windows=summary['original_normalized_match_windows'],raw_windows=summary['original_raw_match_windows'],gained=len(delta['gained']),lost=len(delta['lost'])))
 selected=P/'coordinate'
 old=tomllib.loads((ROOT/'repro/donation-relay/idl-owned-abi-recovery/pubkey-type/source/Cargo.lock').read_text())['package'];new=tomllib.loads((selected/'source/Cargo.lock').read_text())['package']
 registry=lambda ps:{(v['name'],v['version']):v for v in ps if 'source' in v}
 prior,latest=registry(old),registry(new);assert all(latest.get(k)==v for k,v in prior.items()) and len(latest.keys()-prior.keys())==17
 audit=read(P/'dependency-source-audit.json');metadata=next(json.loads(line) for line in (selected/'resolve.log').read_text().splitlines() if line.startswith('{"packages":'))
 packages={(x['name'],x['version']):x for x in metadata['packages'] if x['source'] is not None};assert set(packages)=={(x['name'],x['version']) for x in audit}
 assert len(audit)==173 and sum(x['source_members_exact'] for x in audit)==3924
 for row in audit:
  assert row['archive_sha256']==latest[(row['name'],row['version'])]['checksum'] and row['no_unexpected_files']
  if registry_source:
   source=Path(packages[(row['name'],row['version'])]['manifest_path']).parent;cache=ROOT/'work/relay-anchor-idl-scaffold/cargo-home/registry/cache';archive=next(cache.glob('*/'+row['name']+'-'+row['version']+'.crate'));assert H(archive.read_bytes())==row['archive_sha256'];known=set();total=0
   with tarfile.open(archive,'r:gz') as tar:
    for entry in tar:
     if not entry.isfile():continue
     name=entry.name.split('/',1)[1];data=tar.extractfile(entry).read();assert (source/name).read_bytes()==data;known.add(name);total+=len(data)
   assert len(known)==row['source_members_exact'] and total==row['source_bytes_exact']
   assert not ({str(q.relative_to(source)) for q in source.rglob('*') if q.is_file()}-known-{'.cargo-checksum.json','.cargo-ok','.DS_Store'})
 assert not read(selected/'delta.json')['lost']
 assert len(read(selected/'delta.json')['gained'])==60
 assert read(selected/'match-ledger.json.gz')[217]['normalized_candidate_indices']
 assert read(selected/'match-ledger.json.gz')[218]['normalized_candidate_indices']
 for failure in ['fallback-type-failure','flat-name-resolution-failure']:
  d=P/failure;b=read(d/'build-result.json');assert b['returncode']==101 and b['source_unchanged'] and H((d/'build.log').read_bytes())==b['log_sha256']
  assert all(H((d/'source'/n).read_bytes())==h for n,h in read(d/'source-manifest.json').items())
 canonical_proof=P/'canonical-current-source-proof'
 if canonical_proof.exists():
  b=read(canonical_proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((canonical_proof/'build.log').read_bytes())==b['log_sha256']
  for n in ['candidate.so','unstripped.so']:assert (canonical_proof/n).read_bytes()==(P/'canonical'/n).read_bytes()
  assert read(canonical_proof/'compiled-source-manifest.json')==read(P/'canonical/compiled-source-manifest.json')
 proof=P/'current-source-proof'
 if proof.exists():
  inventory=read(proof/'source-manifest.json');assert read(proof/'compiled-source-manifest.json')=={n:h for n,h in inventory.items() if not n.startswith('target/') and (n.endswith('.rs') or Path(n).name in ['Cargo.toml','Cargo.lock'])}
  b=read(proof/'build-result.json');assert b['returncode']==0 and b['source_unchanged'] and H((proof/'build.log').read_bytes())==b['log_sha256']
  for n in ['candidate.so','unstripped.so']:assert (proof/n).read_bytes()==(selected/n).read_bytes()
  before=read(selected/'compiled-source-manifest.json');after=read(proof/'compiled-source-manifest.json')
  # README is ancillary documentation updated when the proven source is promoted.
  assert {n:h for n,h in before.items() if n!='README.md'}=={n:h for n,h in after.items() if n!='README.md'}
 if current:
  assert proof.exists()
  assert all(H((ROOT/'programs/donation-relay'/n).read_bytes())==h for n,h in read(proof/'compiled-source-manifest.json').items())
 print(json.dumps(dict(verified=True,builds=results,current_source_checked=current,current_location_proof=proof.exists(),registry_source_checked=registry_source,whole_original_byte_identity=False,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--current',action='store_true');ap.add_argument('--check-registry-source',action='store_true');args=ap.parse_args();main(args.current,args.check_registry_source)
