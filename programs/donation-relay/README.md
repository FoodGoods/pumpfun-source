# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. Acceptance requires reconstructed Rust builds. The capture is830448bytes, SHA-256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Captured ELF/assembly files remain analysis inputs; target executable instructions do not enter compilation.

All five donation routes now use one common Rust body with a224-byte context,72-byte arguments and a32-byte amount result. Instruction handlers construct events; public program functions emit them; generated wrappers perform account parsing and return serialization. Funding, SyncNative, token transfer, temporary-account closure, owner/signer/PDA/rent/payer constraints and typed mint policy remain real. Settlement routes retain the prior arena reconstruction.

The selected platform-tools v1.48 output is865096bytes, SHA-256 `6dfbc4d8339c9a6046d61cac6ee932fd15838abc73dd0369f7ea70979c4dd45e`. Unstripped output is998728bytes, SHA-256 `e0eaf6d7f33b26818eef7fea2a3b55549d22478d4ffe9198663e5cccca2a40ba`. A fresh final-path build reproduces both exactly. The [shared donation evidence packet](../../repro/donation-relay/shared-donation-source-recovery/README.md) binds40 Rust/config inputs and complete output/source/receipt evidence. LICENSE/NOTICE and documentation are ancillary. The candidate remains larger than the capture.

Complete normalized matches rise403→416:14 gains and one removed token reload specialization. There are80 raw matches and76 unmatched original windows. New matches include shared-context drop, message/bps checks, raw deserialization helpers, all five generated donation wrappers and all four program-layer functions. The captured common body deserializes token data before/after transfer; the removed reload's legitimate settlement callers remain to reconstruct. No dummy call preserves its count.

Common112 still differs:10248 original bytes versus10328 candidate bytes. The instruction handlers and policy106 also remain unmatched. Normalization masks only call displacements and relocation immediates; register/branch/stack differences remain failures. Source/package/module topology and complete call/data/indirect/allocator/ELF layout closure are not proved by window matches.

All241 distinct finite signed scenarios pass on this exact output, including27 Token-2022 policy fixtures. Independent verification checks exact fixtures/PDA/rent/signatures/privileges, loaded Token-2022 hash, CPI bytes/accounts/order, state/token/event/return effects and rollback. Native Token-2022 routing, arbitrary input/allocator/RefCell behavior, fixed-relayer/settlement success and security acceptance remain unproved. Full logs are saved; comparison omits compute-metering lines and executable-image bytes.

Cargo records are unchanged from the preceding checkpoint. Direct Token-2022 remains7.0.0; Anchor SPL retains6.0.0. A fresh registry audit checks177 resolved packages,4055files/37402916bytes against pinned archives. Final34 program and both77 framework name/message implementations are rederived from the actual output.

```sh
python3 -B repro/donation-relay/shared-donation-source-recovery/verify.py --current --check-registry-source
work/test-env/bin/python -B repro/donation-relay/shared-donation-source-recovery/receipt_verify.py --runtime
```

These rederive saved evidence without VM execution. Earlier --current checks intentionally fail after source advances. Exact common/policy/handler bodies, generated settlement contexts, dispatcher and complete data/relocation/layout identity remain within the active all-contract Rust-only goal. This checkpoint establishes no additional whole-contract byte identity.
