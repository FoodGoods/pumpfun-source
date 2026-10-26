# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. The original ELF is 830,448 bytes, SHA-256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Acceptance requires reconstructed Rust builds. Captured ELF/assembly files remain analysis inputs; no target executable instructions enter compilation.

The loader uses actual Anchor-generated IDL, event-recursion, whitelist and all five donation account contexts. Native routes initialize canonical temporary accounts, fund and SyncNative, transfer/reload, close the temporary account, emit log/self-CPI events and return serialized data. Owner, signer, PDA, rent, payer, token and native-mint/program constraints remain real checks. All five donation bodies now call a typed SPL mint-account policy. Settlement routes retain the prior arena reconstruction.

The selected platform-tools v1.48 output is 868,224 bytes, SHA-256 `42fcde021f4572737fb8eaf515f0e74728f6b8620d744207a323bb7d1f447131`. The unstripped output is 999,776 bytes, SHA-256 `55f719233458e995528bb81d332a0145e2d215dfc1261450fb65931305242299`. A fresh build from this repository path reproduces both exactly. The [typed mint evidence packet](../../repro/donation-relay/typed-mint-source-recovery/README.md) binds 38 compiled source/config inputs, complete ELF/function/data ledgers and signed receipts. README/LICENSE/NOTICE are ancillary. The candidate is larger than the capture.

Complete normalized matches rise from 397 to 403: six gains and no losses. There are 80 raw matches and 89 unmatched original windows. All five donation parsers/exits remain matched. The new matches include three complete typed extension lookups and their helpers. Normalization masks only call displacements and relocation immediates. The 3,440-byte policy106 still differs in three register-choice instructions and remains unmatched; shared donation112 and handler/wrapper structures remain unresolved. Function matching does not establish complete call/data/indirect/allocator closure or ELF equality.

All 241 distinct finite scenarios pass, including 27 new cases against the captured Token-2022 program. The new cases check authority, transfer fee, hook, delegate, close-authority, default state, nontransferability, malformed/unknown extensions and whitelist bypass. They use initialized canonical token accounts and independently check exact fixtures, signatures/privileges, CPI bytes/accounts, token/state/event/return effects, rent debit and rejection rollback. Existing native prefunding, rent top-up/Allocate/Assign, SyncNative/transfer/close and refund cases remain passing. Native Token-2022 routing is not proved by these fixtures.

The direct Token-2022 dependency is 7.0.0; Anchor SPL retains its own 6.0.0. Two registry records were added. A fresh audit checks all 177 registry packages resolved for the target against pinned archives: 4,055 files / 37,402,916 bytes. Final 34 program and both 77 framework name/message implementations are rederived from the actual output. Full observations remain saved; comparison omits compute-metering lines and executable-image bytes. Fixed-relayer/settlement success, arbitrary inputs/allocator/drop behavior and security acceptance remain unproved.

```sh
python3 -B repro/donation-relay/typed-mint-source-recovery/verify.py --current --check-registry-source
work/test-env/bin/python -B repro/donation-relay/typed-mint-source-recovery/receipt_verify.py --runtime
```

These rederive source/output/data/call/registry proofs and saved signed observations without executing programs. Earlier `--current` checks intentionally fail after source advances; historical verifiers remain usable. Exact policy106/shared donation112, donation wrappers, settlement contexts and full dispatcher/data/relocation/layout identity remain within the all-contract Rust-only goal. No whole-contract acceptance count increases.
