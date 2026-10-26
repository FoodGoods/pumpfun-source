#!/usr/bin/env python3
"""Offline full-body/data/receipt verification. No VM or target execution."""
import argparse,base64,copy,gzip,hashlib,importlib.util,json,re,struct,tomllib
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
H=lambda b:hashlib.sha256(b).hexdigest()
def mod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def read_json(path):
 raw=path.read_bytes();return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)
def comparable(row):
 out={k:row[k] for k in ['error','inner_instructions','return_data']}
 out['logs']=[x for x in row['logs'] if re.fullmatch(r'Program \S+ consumed \d+ of \d+ compute units',x) is None]
 relay='RLAYHr9TRFcKB2ubYQhspcnXiaGpaVzNQvHytt47RZu'
 for when in ['before','after']:
  out[when]=copy.deepcopy(row[when]);v=out[when].get(relay)
  if v:
   for field in ['data_length','data_sha256','data_base64']:v.pop(field)
   v['lamports']-=row['before'][relay]['lamports']
 return out

def main(signatures=False):
 wire=mod('anchor_receipt_wire',P/'receipt_helpers.py')
 frozen={x['case']['name']:x for x in read_json(ROOT/'repro/donation-relay/local-validation-proposal/fixture-blueprints.json')}
 counts=dict(receipt_cases=0,signature_fields=0)
 class Original:
  b=(ROOT/'evidence/dependencies/donation_relay/deployed.so').read_bytes()
 original=Original()
 def check_tx(rows,fixture):
  raw=base64.b64decode(rows[0]['transaction_base64']);assert all(r['transaction_base64']==rows[0]['transaction_base64'] for r in rows)
  tx=wire.parse(raw);keys=list(map(wire.b58,tx['keys']));budget,call=tx['instructions'];assert len(tx['instructions'])==2
  assert keys[budget[0]]=='ComputeBudget111111111111111111111111111111' and budget[2]==b'\2'+(1400000).to_bytes(4,'little')
  assert keys[call[0]]==wire.RELAY and call[2].hex()==fixture['instruction_hex']
  assert [keys[i] for i in call[1]]==[x['pubkey'] for x in fixture['instruction_accounts']]
  privileges={x['pubkey']:(x['signer'],x['writable']) for x in fixture['instruction_accounts']};privileges[keys[0]]=(True,True);privileges[wire.RELAY]=(False,False);privileges[keys[budget[0]]]=(False,False);assert set(keys)==set(privileges)
  for i,k in enumerate(keys):
   signer=i<tx['required'];writable=i<tx['required']-tx['readonly_signers'] if signer else i<len(keys)-tx['readonly_unsigned'];assert (signer,writable)==privileges[k]
  for row in rows:
   assert row['signature_verification']==[True]*tx['required'] and row['metadata']['signature']==wire.b58(tx['signatures'][0])
   for field in ['logs','inner_instructions','return_data']:assert row[field]==row['metadata'][field]
   if row['error'] is not None:assert all(row['before'][k]==row['after'][k] for k in row['before'] if k!=keys[0])
   counts['signature_fields']+=tx['required']
  if signatures:
   from solders.signature import Signature
   from solders.pubkey import Pubkey
   assert all(Signature.from_bytes(s).verify(Pubkey.from_bytes(k),tx['message']) for s,k in zip(tx['signatures'],tx['keys']))
  return keys
 for name in read_json(P/'stages.json'):
  d=P/name
  if not (d/'runtime-ordinary').exists():continue
  build=read_json(d/'build-result.json')
  for rd in sorted(d.glob('runtime-*')):
   if not rd.is_dir():continue
   run=read_json(rd/'comparison.json');proc=read_json(rd/'process-result.json');launch=read_json(rd/'launch.json')
   assert proc['returncode']==0 and proc['candidate_unchanged'] and proc['harness_unchanged']
   assert launch['bindings']==dict(launch['old_bindings'],candidate=build['candidate_sha256'])
   assert run['candidate_sha256']==build['candidate_sha256'] and run['all_requested_completed'] and run['passed']==run['case_count']
   for result in run['cases']:
    case=result['case'];f=frozen[case['name']];assert result['fixture']==f['fixture'] and case==f['case']
    left,right=result['original'],result['candidate'];keys=check_tx([left,right],f['fixture'])
    assert not result['mismatches'] and comparable(left)==comparable(right)
    if left['error'] is None:
     assert case['expected_error'] is None
     for row in [left,right]:wire.independent_effects(case,f['fixture'],row,keys)
    counts['receipt_cases']+=1
  if (d/'header-cases.json').exists():
   report=read_json(d/'header-cases.json');assert report['all_passed'] and report['normal_signature_blockhash_history_checks'] and len(report['cases'])==6
   assert report['binary_hashes']['candidate']==build['candidate_sha256']
   assert report['binary_hashes']['original']==H(original.b) and report['binary_hashes']['baseline']=='836d2ffbec4c437cf9447138e4e54de886744cf4841aeadb34aaeaf7e0249a8f'
   for row in report['cases']:
    f=frozen[row['base_case']['name']];assert f['case']==row['base_case'] and f['fixture']==row['base_fixture']
    expected=copy.deepcopy(row['base_fixture']);mutation=row['mutation'];account=mutation['account'];raw=base64.b64decode(expected['accounts'][account]['data_base64']);assert raw[:8].hex()==mutation['old_discriminator'] and mutation['new_discriminator']=='00'*8
    expected['accounts'][account]['data_base64']=base64.b64encode(bytes(8)+raw[8:]).decode();assert expected==row['fixture']
    left,prior,right=[row['results'][n] for n in ['original','baseline','candidate']];check_tx([left,prior,right],row['fixture']);assert comparable(left)==comparable(prior)==comparable(right)
    assert 'Custom(3002)' in left['error'].replace(' ','')
    assert any(('AnchorError caused by account: '+row['expected_outer_name']+'. Error Code: AccountDiscriminatorMismatch.') in log for log in left['logs'])
    counts['receipt_cases']+=1
  report=read_json(d/'instruction-cases.json')
  assert report['all_requested_completed'] and report['passed']==7 and len(report['cases'])==7
  assert report['binary_hashes']['original']==H(original.b)
  assert report['binary_hashes']['control']==H((ROOT/'repro/donation-relay/idl-owned-abi-recovery/pubkey-type/candidate.so').read_bytes())
  assert report['binary_hashes']['candidate']==H((d/'candidate.so').read_bytes())
  for result in report['cases']:
   f=frozen[result['base_case']['name']];assert result['base_case']==f['case'] and result['base_fixture']==f['fixture']
   expected=copy.deepcopy(f['fixture'])
   if result['mutated_args_hex'] is None:
    assert result['suffix_hex']==(b'ignored suffix').hex();expected['instruction_hex']+=result['suffix_hex']
   else:expected['instruction_hex']=expected['instruction_hex'][:16]+result['mutated_args_hex']
   assert expected==result['fixture']
   left,prior,right=[result['results'][n] for n in ['original','control','candidate']];keys=check_tx([left,prior,right],result['fixture'])
   assert comparable(left)==comparable(prior)==comparable(right) and all(not x for x in result['mismatches'].values())
   if result['expected_error'] is None:
    assert all(x['error'] is None for x in [left,prior,right])
    for row in [left,prior,right]:wire.independent_effects(result['base_case'],f['fixture'],row,keys)
   else:assert result['expected_error']==102 and 'Custom(102)' in left['error'].replace(' ','')
   counts['receipt_cases']+=1
  report=read_json(d/'idl-rejections.json');assert report['all_requested_completed'] and report['passed']==9 and len(report['cases'])==9
  assert report['binary_hashes']['candidate']==H((d/'candidate.so').read_bytes())
  assert report['binary_hashes']['control']==H((ROOT/'repro/donation-relay/framework-crate-recovery/full-enums-v148/candidate.so').read_bytes())
  assert report['binary_hashes']['original']==H(original.b)
  for result in report['cases']:
   f=frozen[result['case']['name']];assert result['case']==f['case'] and result['base_fixture']==f['fixture']
   expected=copy.deepcopy(f['fixture']);mutation=result['mutation'];kind=mutation['kind'];account=mutation['account'];data=base64.b64decode(expected['accounts'][account]['data_base64'])
   if kind=='truncate':expected['accounts'][account]['data_base64']=base64.b64encode(data[:mutation['value']]).decode()
   elif kind=='owner':
    name='relay-local-data/rejection-wrong-owner';expected['accounts'][account]['owner']=wire.b58(hashlib.sha256(name.encode()).digest())
   elif kind=='uninitialized':expected['accounts'][account].update(owner=wire.SYSTEM,lamports=0,data_base64='')
   elif kind=='authority':
    authority=hashlib.sha256(b'relay-local-data/rejection-wrong-authority').digest();expected['accounts'][account]['data_base64']=base64.b64encode(data[:8]+authority+data[40:]).decode()
   elif kind=='readonly':expected['instruction_accounts'][0]['writable']=False
   else:raise AssertionError(kind)
   assert expected==result['fixture']
   left,control,right=[result['results'][n] for n in ['original','control','candidate']];check_tx([left,control,right],result['fixture'])
   assert comparable(left)==comparable(control)==comparable(right) and all(not x for x in result['mismatches'].values())
   assert 'Custom('+str(result['expected_code'])+')' in left['error'].replace(' ','')
   counts['receipt_cases']+=1
 print(json.dumps(dict(verified=True,**counts,cryptographic_signatures_checked=signatures,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',action='store_true');args=ap.parse_args();main(args.runtime)
