# Independent Linux x86_64 Fees v1.44 builds

Builds on the upstream packages `repro/pump_fees/linux-v144-sysroot-provenance`,
`repro/pump_fees/linux-v144-hosted-comparison` and
`repro/pump_fees/linux-darwin-v144-attribution`.

Two genuine offline `cargo build-sbf --tools-version v1.44` builds with the
official Linux platform-tools v1.44 archive
(SHA-256 `6719b889d60677a8a2fcf4c82f68441a1afe0ab093edd2efe9f84a67a808b3e9`)
and CLI 2.1.21 on a Linux x86_64 host:

| Source snapshot | Candidate | SHA-256 |
| --- | --- | --- |
| Frozen Fees revision `4ffe8bd88761059693e481ae972443c10204f7af` | `fees-frozen-linux-v144.so` | `7e823e605097cdba7a3d782a2f20edaee9980d7d5a29822ac7d1a43400620133` |
| Current main `804df5c8` (sharing-authorize source 26) | `fees-current-linux-v144.so` | `6c44d9f2ffe9b18c79a6344b256d8acd7a34c10e77b894c51f46512a447b8ce6` |

## Findings

1. The frozen-revision Linux build reproduces, byte for byte, the previously
   published hosted run 40166255149 candidate (`7e823e60…`). This independently
   confirms the hosted build's determinism on a second Linux host.
2. The current-source Linux build differs from the retained macOS main
   candidate `2387f8139a13918a…` only in sysroot path strings
   (`/home/runner/...` versus `/Users/runner/...`) and dependent stack-frame
   layout deltas. Same 26 source inputs hash to the same values.
3. The raw comparison of the current-source Linux build `6c44d9f2…` against the
   frozen hosted-candidate build `7e823e60…` and the captured original
   `4f2955d0…` is recorded in `raw-byte-comparison.json`: 420,129 differing
   shared positions (first at 24, length delta +94,816) versus the frozen
   candidate; 460,758 differing shared positions (first at 24, length delta
   −85,144) versus the original. The upstream
   `linux-v144-sysroot-provenance` package already establishes that the
   original embeds `/home/runner/work/platform-tools` sysroot paths from the
   official Linux v1.44 archive; the frozen-source build's byte equality with
   the hosted candidate independently confirms determinism on a second Linux
   host.
4. Whole-file equality remains false for every local candidate versus the
   captured original. No source patch, binary patch, padding or normalization
   was applied; all builds were clean and offline after initial locked fetch.

## Verify

Run `python3 -B verify.py` for portable manifest/candidate/raw-comparison
checks. Add `--repo /path/to/pumpfun-source` to re-read the captured original
`evidence/original/pump_fees/deployed.so` and repeat all raw comparisons from
disk. Neither mode builds, executes the target or contacts a network.

## Reproduce

```sh
cargo build-sbf --manifest-path programs/pump-fees/Cargo.toml \
  --tools-version v1.44 --sbf-sdk <platform-tools>/sdk/sbf \
  --sbf-out-dir <out> -- --locked
```

with platform-tools v1.44 extracted so that `<platform-tools>/sdk/sbf/bin`
holds the shipped rustc/cargo.
