# Donation Relay reconstructed Rust

The captured comparison ELF is `evidence/dependencies/donation_relay/deployed.so` (830448bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`). Whole captured-byte identity is still unachieved. Target instructions/assembly are analysis inputs only; builds compile reconstructed Rust source.

Current27 compiled source/config inputs match [idl-owned-abi-recovery](../../repro/donation-relay/idl-owned-abi-recovery/README.md). The selected native v1.48 artifact is524080bytes, SHA256 `880ee38d64e196d430fb1c3ea3713674c014e579da6b40762a7898480419b98b`. A fresh build directly from this source location reproduces its stripped and unstripped bytes exactly. Main README and upstream error-model/LICENSE/NOTICE are ancillary files outside the compiled map.

The reconstructed error-model crate restores the external framework conversion/boxing boundary, owned error propagation/logging/lowering, account-name/source replacement and compared-value handling. Its77-variant framework enum follows authenticated Anchor0.31.1 source/generator; the34-variant program enum follows the decoded6000–6033 catalog. All111 names/messages have complete data proofs against the selected candidate and original selectors. Error3002 constructs Source(lib.rs:36) before boxing and then replaces/drops it through IdlAccount and outer account-name decorators. Errors6009/6018 carry the decoded checks.rs:55/:192 metadata. These are explicit reconstructed program values, not claims about this new source's historical file locations.

IDL parsers now return the compact owned framework error instead of a redundant cause/account/keys/values/origin wrapper. They receive mutable slice references following the observed AccountDeserialize ABI. Header uses the actual Pubkey field type and Borsh0.10.4 derives instead of a handwritten reader. All previously resolved external registry package entries remain unchanged; the root crate directly uses Borsh already in its lock, plus the local error-model dependency.

Complete comparison retains492 inferred original windows,368 candidate symbol windows,60 raw/243 normalized original matches,249 unmatched windows. Relative to the previous238-window snapshot, six full matches are added (including the288-byte IDL header writer) and one24-byte helper match is lost. The checked-header body is1088bytes, equal in length to the target but still instruction-unequal; unchecked-header also remains unmatched. These window counts are not source-recovery percentages, full call/data closure or whole-byte identity.

All15 existing finite ordinary/business-rejection cases pass. Six malformed-discriminator cases cover every checked IDL caller; nine additional rejection cases cover header lengths0/7/8/39/43, wrong owner, uninitialized account, wrong authority and readonly account. These tests derive from existing owned fixtures, preserve normal signatures/blockhash/history checks, and compare error/log/CPI/return/state observations with independent success-effect and rollback checks. The same transaction is submitted to original/control/candidate isolated VMs where recorded. Full logs and signed receipts are retained. The inherited comparator excludes compute-metering log lines and executable-image account bytes. The previous control also matches these visible failures, so finite success does not prove allocator/drop/OOM equivalence or every input.

[framework-crate-recovery](../../repro/donation-relay/framework-crate-recovery/README.md) retains earlier15builds including explicit SDK controls, native/current proof, nearby SDK/profile negatives and Linuxv1.48 proof of its preceding Rust snapshot. The target's tracked allocation-error callers and stable-quicksort source family favor Relay's v1.48 compiler family over measured v1.44/v1.50/v1.51 for that source; this does not change core contract defaults or uniquely authenticate the historical toolchain. The preceding Linux artifact is not a build proof for the newer IDL source.

Remaining work includes exact checked/unchecked IDL bodies, generated account/context and business wrappers, complete runtime/indirect/data/allocator closure, and whole ELF/relocation/layout equality. Fixed-relayer/swap/distribution success routes still lack broader runtime coverage; no historical authority is substituted. No whole-program/dependency identity counter increases from these finite tests or normalized matches.

Verify the current snapshot and saved signatures without executing programs:

```
python3 -B repro/donation-relay/idl-owned-abi-recovery/verify.py
work/test-env/bin/python -B repro/donation-relay/idl-owned-abi-recovery/verify.py --runtime --current
```
