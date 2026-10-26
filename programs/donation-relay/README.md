# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. The original ELF is830448bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust; raw captured ELF/assembly are analysis-only; recovered metadata is expressed explicitly in Rust.

The current source combines real Anchor-generated IDL, event-recursion and whitelist paths with the reconstructed business implementation for the other instructions. The whitelist route uses the actual account derives, initialization constraints, update and access checks. Other business arena/context/wrapper paths and top-level routing still need recovery. The obsolete manual whitelist branch remains inside the legacy dispatcher, although the loader selects the generated handler.

Selected native platform-tools v1.48 output:614880bytes SHA256 `d8c99c89eba893b030c16733a88300eaf551648853b722bc03b37b67529a2c35`; unstripped733248bytes SHA256 `9d1885d78b5db99f98fb2f818ecfa3bf747277fdb342454d26955492f6790568`. A fresh build from this final repository path reproduces both files exactly. [whitelist-generated-source-recovery](../../repro/donation-relay/whitelist-generated-source-recovery/README.md) binds30 inventoried Rust/config inputs, primary macros, full ELF ledgers and receipts. README/LICENSE/NOTICE are ancillary.

Complete normalized original-window matches rise309→328:19 gains, none lost. Raw matches75;164 of492 original windows remain unmatched. The complete whitelist update101, access check105, parser156, initialization closure157, exit158, checked/unchecked state165/166 and wrapper188 match, alongside previous IDL headers/dispatcher and shared byte reader. Normalization masks call displacements and relocation immediates. These counts do not establish complete data/call/indirect/allocator closure or whole-file equality.

Captured diagnostic filenames and macro coordinates are restored as observed program metadata. The source does not attribute surrounding reconstructed comments to historical text. Borrowed seed slices and primary-macro constant expressions restore actual emitted structure. Two explicit #[inline(never)] annotations retain the independently observed body/check call boundaries; historical annotations are unknown. All code remains Rust, with no embedded executable fragments or patched ELF. Existing registry package records are unchanged; Anchor's init-if-needed feature is enabled. Codegen-units16 regresses matching and is rejected; codegen-units1 is retained. No unique historical recipe claim follows.

The selected output passes103 finite scenarios: the preceding85 plus18 whitelist rejection/initialization cases. Valid ephemeral signatures exercise CreateAccount and prefunded Transfer/Allocate/Assign before the genuine wrong-relayer rejection, plus insufficient funding. The historical relayer key is never substituted or invented as signed. The verifier independently checks System instruction data/account order/depth and rollback. Three earlier manual-control log mismatches remain recorded; original/candidate match. Successful fixed-relayer whitelist, swap and distribution routes still need runtime coverage.

Normal signatures, blockhash/history, frozen comparison and independent effects/rollback remain enabled. Full observations are saved; comparison omits compute-metering lines and executable-image account bytes. Finite allocator tests are not general OOM/drop equivalence. The final artifact also rederives complete names/messages for34 program codes and both77-variant framework implementations. Earlier Linux evidence applies to preceding snapshots.

```
python3 -B repro/donation-relay/whitelist-generated-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/whitelist-generated-source-recovery/receipt_verify.py --runtime
```

These recheck sealed current-source/output/data proofs and saved transactions without VM execution. Older packet --current checks intentionally fail after source advances; historical checks remain usable. Remaining work includes obsolete-route pruning, other generated business account/context/wrapper paths, dispatcher169, helper34 and full data/relocation/layout identity. All original core/dependency work remains in the active Rust-only goal.
