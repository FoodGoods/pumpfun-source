#!/usr/bin/env python3
"""Verify the linux-current-source-build package seals and raw comparisons.

Portable mode (default): checks package self-integrity (manifest-sha256.json),
candidate binary hashes, and recomputes the raw byte comparisons against the
recorded shared-extent statistics.

Repo mode (--repo /path/to/pumpfun-source): additionally re-reads the captured
original Fees payload from evidence/original/pump_fees/deployed.so and repeats
every raw comparison from disk. Never builds, never executes the target,
never contacts a network, never changes source.
"""
from pathlib import Path
import argparse, hashlib, json

P = Path(__file__).resolve().parent
H = lambda b: hashlib.sha256(b).hexdigest()
read = lambda n: json.loads((P / n).read_text())

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path)
args = ap.parse_args()

CUR = 'fees-current-linux-v144.so'
FROZEN = 'fees-frozen-linux-v144.so'
assert {str(p.relative_to(P)): H(p.read_bytes()) for p in P.rglob('*') if p.is_file() and p != P / 'manifest-sha256.json' and '__pycache__' not in p.parts} == read('manifest-sha256.json')
assert not any(p.is_symlink() for p in P.rglob('*'))
cmp_data = read('raw-byte-comparison.json')
readme = (P / 'README.md').read_text()

cur = (P / CUR).read_bytes()
frozen = (P / FROZEN).read_bytes()
assert H(cur) == cmp_data['current_sha256'] == '6c44d9f2ffe9b18c79a6344b256d8acd7a34c10e77b894c51f46512a447b8ce6'
assert H(frozen) == cmp_data['frozen_sha256'] == '7e823e605097cdba7a3d782a2f20edaee9980d7d5a29822ac7d1a43400620133'
assert len(cur) == 863800 and len(frozen) == 768984

def cmp(a, b):
    shared = min(len(a), len(b))
    d = sum(x != y for x, y in zip(a, b))
    f = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    return {'shared_bytes': shared, 'shared_differing_positions': d, 'first_difference': f, 'length_delta': len(a) - len(b)}

recorded = {
    'current_vs_frozen': cmp(cur, frozen),
}
if args.repo:
    root = args.repo.resolve()
    orig = (root / 'evidence/original/pump_fees/deployed.so').read_bytes()
    assert H(orig) == cmp_data['original_sha256'] == '4f2955d0f6b40cc9ff7daa18ccad7d19119ba1249759f4e7e3bb691beee6b35e'
    assert len(orig) == 948944
    recorded['current_vs_original'] = cmp(cur, orig)
    recorded['frozen_vs_original'] = cmp(frozen, orig)
for key, got in recorded.items():
    assert got == {k: v for k, v in cmp_data[key].items() if k not in ('bytes_a', 'bytes_b')}, key
# frozen-vs-original is the upstream linux-v144-hosted-comparison published number
assert cmp_data['frozen_vs_original']['shared_differing_positions'] == 421958
assert cmp_data['frozen_vs_original']['first_difference'] == 24
assert cmp_data['frozen_vs_original']['length_delta'] == -179960
print(json.dumps({
    'verified': True,
    'current_sha256': H(cur),
    'frozen_sha256': H(frozen),
    'frozen_equals_hosted_candidate': H(frozen) == '7e823e605097cdba7a3d782a2f20edaee9980d7d5a29822ac7d1a43400620133',
    'original_sha256_recomputed': bool(args.repo),
    'whole_file_equality_with_original': False,
    'raw_comparisons_recomputed': sorted(recorded),
}, indent=2))
