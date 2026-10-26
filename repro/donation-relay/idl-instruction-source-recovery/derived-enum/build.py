from pathlib import Path
import json,os,subprocess,hashlib,shutil
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
H=lambda b:hashlib.sha256(b).hexdigest()
launch=json.loads((ROOT/'repro/donation-relay/source-build-11-idl-discriminator/attempt/build-launch.json').read_text())
env=dict(os.environ);env.update(launch['environment']);env['CARGO_TARGET_DIR']=str(P/'target')
source=P/'source';before=json.loads((P/'source-manifest.json').read_text());assert all(H((source/n).read_bytes())==h for n,h in before.items())
assert not (P/'target').exists(),'require fresh target directory'
cmd=list(launch['command']);cmd[cmd.index('--tools-version')+1]='v1.48';cmd[cmd.index('--manifest-path')+1]=str(source/'Cargo.toml');cmd[cmd.index('--sbf-out-dir')+1]=str(P/'artifacts')
(P/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
(P/'build-environment.json').write_text(json.dumps(launch['environment']|{'CARGO_TARGET_DIR':str(P/'target')},indent=2)+'\n')
with (P/'build.log').open('wb') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT)
unchanged=all(H((source/n).read_bytes())==h for n,h in before.items());assert unchanged
facts=dict(returncode=r.returncode,source_unchanged=unchanged,log_sha256=H((P/'build.log').read_bytes()))
if r.returncode==0:
 q=P/'artifacts/donation_relay_source_proposal.so';assert q.exists();shutil.copyfile(q,P/'candidate.so')
 unstripped=P/'target/sbf-solana-solana/release/donation_relay_source_proposal.so';shutil.copyfile(unstripped,P/'unstripped.so')
 facts.update(candidate_sha256=H(q.read_bytes()),candidate_bytes=q.stat().st_size,unstripped_sha256=H(unstripped.read_bytes()))
(P/'build-result.json').write_text(json.dumps(facts,indent=2)+'\n');print(json.dumps(facts,indent=2));assert r.returncode==0
