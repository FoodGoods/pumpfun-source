# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. The original capture is830448bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust; captured instructions and assembly are analysis inputs only.

The current source combines recovered business behavior with authentic Anchor-generated reserved IDL operations and event recursion. One genuine SDK entrypoint routes reserved selectors to the generated framework and business selectors to the existing handler. The framework occupies its own module, preserving business code in the original crate. The top-level route and business arena/context/wrappers still differ from the original generated structures.

All eleven business argument structs now use Borsh0.10.4 derives reconstructed from the captured IDL, with actual Pubkey/array distinctions and Share/ShareType. The account writers use Anchor's real `__private::BpfWriter` export rather than a root-crate copy. This restores shared reader/error-construction boundaries without executable blobs or forced compiler annotations. Older independent IDL adapter and reader files remain for historical comparison; the active routes use the recovered framework and derived business arguments.

The selected native platform-tools v1.48 ELF is587176bytes, SHA256 `4be6d422c4b8879c06239a2c47b0e4fe7c7ef131acdb018da4284a036672ca0e`; unstripped702944bytes SHA256 `a4ae875b0400aae91b886925e971959d1d883dd84354a3963d7afa23ed67123f`. A fresh build from this final source path reproduces both files exactly. [business-wire-source-recovery](../../repro/donation-relay/business-wire-source-recovery/README.md) binds28 inventoried Rust/config inputs and the measured evidence. README/LICENSE/NOTICE are ancillary.

Complete normalized matches rise303→309 with six gains and none lost. Raw matches75;183 of492 inferred original windows remain unmatched. New matches include String/vector readers, the4032-byte reserved-IDL dispatcher170 and the2248-byte byte-vector reader77. Both IDL headers217/218 remain matched. Normalization masks only direct-call displacement and relocation immediates; these are complete instruction-shape counts, not source-recovery percentages, transitive call/data closure or whole-file identity. Error helper34 still differs.

The observed lib.rs:36 macro coordinate and root-only compiler mapping `--remap-path-prefix=src/=programs/contracts/src/` preserve the captured diagnostic filename. This is reconstructed program metadata, not historical source attribution. Canonical public registry paths permit consistent SDK cwd remapping. Registry package records are unchanged from the preceding303-window build: Anchor0.31.1, resolved0.31.2 macros and existing locked dependencies. No unique historical toolchain/dependency claim follows.

All85 measured cases pass: the prior37 plus48 business-wire cases covering all eleven selectors, field truncations, invalid UTF-8/share tags, valid donation suffixes and two enormous declared byte-vector lengths. In the last two, original/candidate both fail allocation while the prior handwritten decoder returns102; those negative controls remain saved. This repairs two observed paths without proving arbitrary OOM behavior. Normal signatures/blockhash/history, frozen comparator and independent effect/rollback checks remain enabled. Full logs are retained; comparison excludes compute-metering lines and executable-image account bytes.

Fixed-relayer/swap/distribution success routes, complete data/indirect/allocator closure, generated business wrappers and full ELF layout still need recovery/verification. The older111selector-data proofs apply to their own frozen artifacts; no unmeasured transfer is claimed. Earlier Linux evidence belongs to a preceding source snapshot. Other original core/dependency gaps remain within the full goal.

```
python3 -B repro/donation-relay/business-wire-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/business-wire-source-recovery/receipt_verify.py --runtime
```

These verify sealed outputs/current source and saved signed receipts without executing programs. Historical packet --current checks intentionally fail after source advances; their default historical checks remain usable.
