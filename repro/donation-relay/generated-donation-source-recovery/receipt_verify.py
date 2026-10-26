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
  if (d/'instruction-cases.json').exists():
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
  if (d/'idl-rejections.json').exists():
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
  if (d/'business-wire-cases.json').exists():
   report=read_json(d/'business-wire-cases.json');specs=read_json(d/'business-wire-specs.json');assert len(specs)==48 and report['all_requested_completed'] and report['passed']==48 and len(report['cases'])==48
   assert report['binary_hashes']['candidate']==build['candidate_sha256'] and report['binary_hashes']['original']==H(original.b)
   assert report['binary_hashes']['control']==H((ROOT/'repro/donation-relay/anchor-framework-source-recovery/coordinate/candidate.so').read_bytes())
   idl=read_json(P/'captured-idl.json');assert report['idl_sha256']==H((P/'captured-idl.json').read_bytes());ixs={x['name']:x for x in idl['instructions']}
   allocation_controls=0
   for result,spec in zip(report['cases'],specs):
    assert result['spec']==spec;f=frozen[result['base_case']['name']];assert result['base_case']==f['case'] and result['base_fixture']==f['fixture'];expected=copy.deepcopy(f['fixture'])
    expected['instruction_hex']=f['fixture']['instruction_hex']+(b'ignored suffix').hex() if spec['data_hex'] is None else spec['data_hex'];assert expected==result['fixture']
    assert bytes.fromhex(expected['instruction_hex'])[:8]==bytes(ixs[spec['instruction']]['discriminator'])
    left,prior,right=[result['results'][n] for n in ['original','control','candidate']];keys=check_tx([left,prior,right],result['fixture']);assert comparable(left)==comparable(right) and not result['mismatches']['candidate']
    if spec['expect_control_equal']:assert comparable(left)==comparable(prior) and not result['mismatches']['control']
    if spec['expected']=='success':
     assert all(x['error'] is None for x in [left,prior,right])
     for row in [left,prior,right]:wire.independent_effects(result['base_case'],f['fixture'],row,keys)
    elif spec['expected']=='decode102':assert 'Custom(102)' in left['error'].replace(' ','')
    else:
     assert spec['expected']=='allocation_failure' and not spec['expect_control_equal'];assert left['error'] is not None and any('memory allocation failed' in x for x in left['logs']);assert set(result['mismatches']['control'])=={'error','logs'} and 'Custom(102)' in prior['error'].replace(' ','');allocation_controls+=1
    counts['receipt_cases']+=1
   assert allocation_controls==2
  if (d/'whitelist-cases.json').exists():
   report=read_json(d/'whitelist-cases.json');assert report['all_requested_completed'] and report['passed']==len(report['cases']) and len(report['cases']) in [15,18]
   assert report['binary_hashes']['candidate']==build['candidate_sha256'] and report['binary_hashes']['original']==H(original.b)
   assert report['binary_hashes']['control']==H((ROOT/'repro/donation-relay/business-wire-source-recovery/framework-writer/candidate.so').read_bytes())
   from_fixture=frozen['donate_v1'];negative_controls=set()
   for result in report['cases']:
    assert result['base_case']==from_fixture['case'] and result['base_fixture']==from_fixture['fixture'];expected=copy.deepcopy(from_fixture['fixture']);mutation=result['mutation'];kind=mutation['kind'];key=mutation['account'];assert key==expected['canonical_pdas']['mint_whitelist'];owner=next(x['pubkey'] for x in expected['instruction_accounts'] if x['signer'] and x['pubkey']!=wire.RELAY)
    # The owner signer is the original donate_v1 `from` account (index5).
    owner=expected['instruction_accounts'][5]['pubkey'];assert owner in expected['test_owned_pubkeys']
    metas=[dict(pubkey=key,signer=False,writable=True),dict(pubkey=owner,signer=True,writable=True),dict(pubkey=wire.SYSTEM,signer=False,writable=False)]
    raw=base64.b64decode(expected['accounts'][key]['data_base64'])
    if kind=='readonly_whitelist':metas[0]['writable']=False
    elif kind=='discriminator':expected['accounts'][key]['data_base64']=base64.b64encode(bytes(8)+raw[8:]).decode()
    elif kind=='truncate':expected['accounts'][key]['data_base64']=base64.b64encode(raw[:mutation['value']]).decode()
    elif kind=='owner':expected['accounts'][key]['owner']=wire.b58(hashlib.sha256(b'relay-local-data/whitelist-wrong-owner').digest())
    elif kind=='pda':
     wrong=wire.b58(hashlib.sha256(b'relay-local-data/whitelist-wrong-pda').digest());assert mutation['new_account']==wrong;expected['accounts'][wrong]=copy.deepcopy(expected['accounts'][key]);metas[0]['pubkey']=wrong
    elif kind=='rent':expected['accounts'][key]['lamports']-=1
    elif kind=='readonly_signer':metas[1]['writable']=False
    elif kind=='not_signer':metas[1]['signer']=False
    elif kind=='system':
     wrong=wire.b58(hashlib.sha256(b'relay-local-data/whitelist-wrong-system').digest());assert mutation['new_account']==wrong;expected['accounts'][wrong]=dict(lamports=1,data_base64='',owner=wire.SYSTEM,executable=False,rent_epoch=0);metas[2]['pubkey']=wrong
    elif kind=='missing':metas=metas[:mutation['value']]
    elif kind.startswith('initialize_'):
     assert kind in ['initialize_create','initialize_prefunded','initialize_insufficient'];expected['accounts'][key].update(owner=wire.SYSTEM,data_base64='',lamports=1 if kind=='initialize_prefunded' else 0)
     if kind=='initialize_insufficient':expected['accounts'][owner]['lamports']=1
    else:assert kind=='none'
    expected['instruction_accounts']=metas;expected['instruction_hex']='d185fd0c5009e780'+'00000000';assert expected==result['fixture']
    left,prior,right=[result['results'][n] for n in ['original','control','candidate']];keys=check_tx([left,prior,right],result['fixture']);assert comparable(left)==comparable(right) and not result['mismatches']['candidate'];assert 'Custom('+str(result['expected_code'])+')' in left['error'].replace(' ','')
    if result['name'] in ['wrong_space','wrong_system','missing0']:assert result['mismatches']['control']==['logs'];negative_controls.add(result['name'])
    else:assert comparable(left)==comparable(prior) and not result['mismatches']['control']
    for row in [left,prior,right]:
     calls=[c for group in row['inner_instructions'] for c in group]
     if kind.startswith('initialize_'):
      rent=(1037+128)*3480*2;ops=[2,8,1] if kind=='initialize_prefunded' else [0];assert len(calls)==len(ops)
      for call,op in zip(calls,ops):
       ix=call['instruction'];data=wire.wire_vec(ix['data']);accounts=[keys[x] for x in wire.wire_vec(ix['accounts'])];assert keys[ix['programIdIndex']]==wire.SYSTEM and call['stackHeight']==2 and int.from_bytes(data[:4],'little')==op
       if op==0:assert len(data)==52 and int.from_bytes(data[4:12],'little')==rent and int.from_bytes(data[12:20],'little')==1037 and data[20:]==wire.un58(wire.RELAY) and accounts==[owner,key]
       elif op==2:assert len(data)==12 and int.from_bytes(data[4:],'little')==rent-1 and accounts==[owner,key]
       elif op==8:assert len(data)==12 and int.from_bytes(data[4:],'little')==1037 and accounts==[key]
       else:assert len(data)==36 and data[4:]==wire.un58(wire.RELAY) and accounts==[key]
     else:assert not calls
    counts['receipt_cases']+=1
   assert negative_controls=={'wrong_space','wrong_system','missing0'}
  if d.name=='compared':
   report=read_json(d/'donate-context-cases.json');assert report['all_requested_completed'] and report['passed']==18 and len(report['cases'])==18
   assert report['binary_hashes']['candidate']==build['candidate_sha256'] and report['binary_hashes']['original']==H(original.b) and report['binary_hashes']['control']==H((ROOT/'repro/donation-relay/whitelist-generated-source-recovery/constants/candidate.so').read_bytes())
   seen=set();negative=set()
   for result in report['cases']:
    f=frozen['donate_v1'];assert result['base_case']==f['case'] and result['base_fixture']==f['fixture'];expected=copy.deepcopy(f['fixture']);raw=bytes.fromhex(expected['instruction_hex']);config=raw[16:48];mint=wire.un58(expected['instruction_accounts'][3]['pubkey'])
    for label,type_name,size,tail in [('epoch_tracker','EpochTrackerV1',90,bytes(16)),('debouncer','DebouncerV1',82,bytes(8))]:
     key=expected['canonical_pdas'][label];fixture_state=result['initialized_accounts'][key];b=base64.b64decode(fixture_state['data_base64']);bump=b[8];assert hashlib.sha256(label.encode()+b'_v1'+config+mint+bytes([bump])+wire.un58(wire.RELAY)+b'ProgramDerivedAddress').digest()==wire.un58(key)
     data=wire.account_disc(type_name)+bytes([bump,1])+config+mint+tail;assert len(data)==size
     expected['accounts'][key]=dict(lamports=(size+128)*3480*2,data_base64=base64.b64encode(data).decode(),owner=wire.RELAY,executable=False,rent_epoch=0)
    assert expected['accounts']==result['initialized_accounts']
    mutation=result['mutation'];label=mutation['target'];kind=mutation['kind'];assert label in ['epoch_tracker','debouncer'];key=expected['canonical_pdas'][label];assert mutation['account']==key;data=base64.b64decode(expected['accounts'][key]['data_base64']);index=0 if label=='epoch_tracker' else 1
    if kind=='short0':expected['accounts'][key]['data_base64']=''
    elif kind=='short8':expected['accounts'][key]['data_base64']=base64.b64encode(data[:8]).decode()
    elif kind=='discriminator':expected['accounts'][key]['data_base64']=base64.b64encode(bytes(8)+data[8:]).decode()
    elif kind=='owner':expected['accounts'][key]['owner']=wire.b58(hashlib.sha256(b'relay-local-data/donate-context-wrong-owner').digest())
    elif kind=='config':expected['accounts'][key]['data_base64']=base64.b64encode(data[:10]+hashlib.sha256(b'relay-local-data/donate-context-wrong-config').digest()+data[42:]).decode()
    elif kind=='mint':expected['accounts'][key]['data_base64']=base64.b64encode(data[:42]+hashlib.sha256(b'relay-local-data/donate-context-wrong-mint').digest()+data[74:]).decode()
    elif kind=='invalid_enum':expected['accounts'][key]['data_base64']=base64.b64encode(data[:9]+b'\x02'+data[10:]).decode()
    elif kind=='readonly':expected['instruction_accounts'][index]['writable']=False
    else:
     assert kind=='pda';wrong=wire.b58(hashlib.sha256(('relay-local-data/donate-context-wrong-'+label).encode()).digest());expected['accounts'][wrong]=copy.deepcopy(expected['accounts'][key]);expected['instruction_accounts'][index]['pubkey']=wrong
    assert expected==result['fixture'];assert result['name']==label+'/'+kind;seen.add(result['name'])
    left,prior,right=[result['results'][n] for n in ['original','control','candidate']];check_tx([left,prior,right],result['fixture']);assert left['error'] is not None and comparable(left)==comparable(right) and not result['mismatches']['candidate']
    if kind in ['config','mint']:
     assert result['mismatches']['control']==['logs'];negative.add(result['name']);line={('epoch_tracker','config'):102,('debouncer','config'):110,('epoch_tracker','mint'):127,('debouncer','mint'):118}[(label,kind)]
     assert any('programs/contracts/src/tools/donate/shared.rs:'+str(line)+'.' in x for x in left['logs'])
     if kind=='mint':assert sum(x in ['Program log: Left:','Program log: Right:'] for x in left['logs'])==2
    else:assert comparable(left)==comparable(prior) and not result['mismatches']['control']
    counts['receipt_cases']+=1
   assert len(seen)==18 and len(negative)==4
 print(json.dumps(dict(verified=True,**counts,cryptographic_signatures_checked=signatures,vm_execution=False)))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--runtime',action='store_true');args=ap.parse_args();main(args.runtime)
