# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. Original ELF830448bytes SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust. Raw captured ELF/assembly files remain analysis-only; decoded source metadata is expressed explicitly in Rust.

The loader uses actual Anchor-generated IDL, event-recursion, whitelist and all five donation account contexts. Native routes initialize canonical temporary token accounts, fund and SyncNative, perform the donation transfer/reload, close the temporary account, emit log/self-CPI events and return serialized data. Token, native-mint/program-pair, owner, signer, PDA, rent and payer constraints are real checks. Obsolete manual donation selectors/wrappers are removed. Settlement routes retain the prior arena model. Exact shared donation112, independently reconstructed mint policy and top-level handler/wrappers remain unresolved.

Selected native platform-tools v1.48 output863920bytes SHA256 `087057598554b4ced10f0d499362013374fdbf8ea20d4b52ac228a0007a86a5a`; unstripped994128bytes SHA256 `f9df0b0a4e7da213001c93928a43556a743fda0a3875052dfac3b2fbf132ed0e`. A fresh build from this repository path reproduces both exactly. [native-generated-source-recovery](../../repro/donation-relay/native-generated-source-recovery/README.md) binds38 inventoried inputs, full ELF/source/data and signed receipts. README/LICENSE/NOTICE are ancillary. The current ELF is larger than the capture; it is not whole-byte identical.

Complete normalized matches rise375→397:22 gains, none lost. Raw matches78;95 of492 windows remain unmatched. All five donation account parsers and appropriate exits now match, as do the complete native mint/program predicates, initialization closures and new CPI helpers. Normalization masks call displacements and relocation immediates; body matching does not prove complete call/data/indirect/allocator closure or ELF equality.

All214 distinct finite scenarios pass. Native cases cover prefunding1lamport or rent-plus12345, exact System rent top-up/Allocate/Assign, SyncNative/transfer/close instruction bytes/accounts, refunds and ordinary effects. Message/tip rejection after native funding, malformed state, bad PDA, insufficient funds, privilege escalation and wrong native mint preserve rollback. Signatures, blockhash/history, account privileges, exact fixture/PDA/rent bytes and independent effects are checked. No historical relayer is substituted. Native fixtures here execute Tokenkeg; Token-2022 runtime coverage is not claimed from these tests.

Full observations are retained; comparison omits compute-metering lines and executable-image bytes. Fixed-relayer/settlement success, arbitrary inputs/allocator/drop behavior and security acceptance remain unproved. Registry records are unchanged. Final34program and both77framework names/messages are rederived from the actual output; primary source members are authenticated. Earlier source-origin/macro-coordinate and whitelist boundary-annotation qualifications remain. No binary is patched or executable instruction fragments embedded.

```
python3 -B repro/donation-relay/native-generated-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/native-generated-source-recovery/receipt_verify.py --runtime
```

These rederive sealed current-source/output/data/call-map proofs and saved signed observations without executing programs. Older --current checks intentionally fail after source advances; historical verifiers remain usable. Shared donation112/mint policy, top-level wrappers, generated settlement contexts and full dispatcher/data/relocation/layout identity remain within the all-contract Rust-only goal. No whole-contract acceptance count increases.
