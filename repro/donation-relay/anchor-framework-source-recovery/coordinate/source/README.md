# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. The original capture is830448bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust; captured instructions and assembly are analysis inputs only.

The current source combines the recovered business implementation with authentic Anchor-generated reserved IDL operations and event recursion. One genuine SDK entrypoint routes reserved selectors to the generated framework and business selectors to the existing handler. The framework lives in its own Rust module, preserving business code in the original crate. This dispatch arrangement is a reconstruction step and does not yet reproduce the complete captured dispatcher. The original independent IDL adapter source remains for historical comparison; the active dispatch no longer calls it.

The selected native platform-tools v1.48 build is582480bytes, SHA256 `f060edd28946c9ff8fb5b92ace3bb05fad20990e78a79c98f5863a6e9c17a230`; unstripped697208bytes, SHA256 `6b81399ac20eb866d6baece29c41d9e99be0e86b44e3bc0b49ec0ede11e37808`. Evidence and a fresh current-location reproduction are retained in [anchor-framework-source-recovery](../../repro/donation-relay/anchor-framework-source-recovery/README.md).

The lock preserves every preceding registry package entry exactly and adds17 packages for Anchor0.31.1, its resolved0.31.2 macros and supporting dependencies. The direct indexmap2.11.4 pin uses an available compiler-compatible version. This is a measured build recipe, not unique historical dependency/compiler attribution. Relay-specific v1.48 evidence does not change core contract defaults.

Complete normalized original-window matches increase243→302 with59 gained and none lost. Raw matches70;190 of492 original windows remain unmatched. New matches include generated account admission/exit, IDL Create/Write/SetAuthority and the entire488-byte unchecked header decoder. Normalization masks only direct-call displacement and relocation-immediate fields; these counts do not prove transitive call/data closure or whole-byte identity. Checked header217 and payload reader77 remain unmatched.

All37 measured cases pass:12ordinary,3business rejections,6malformed headers,9IDL account rejections and7instruction-data cases. The frozen harness retains normal signatures, blockhash/history checks, full logs and transaction receipts, independent success effects and rollback checks. Its comparator excludes compute-metering lines and executable-image account bytes. Coverage is finite; fixed-relayer/swap/distribution success routes and allocation-failure behavior remain gaps.

The owned reconstructed error-model and34business codes remain. Decoded checks.rs:55/:192 business metadata is explicit program data rather than historical source attribution. Older framework/IDL data-selector proofs apply to their frozen artifacts; no unmeasured transfer to this output is claimed.

Remaining work includes replacing the business arena/context/wrapper abstraction with recovered generated Anchor source, matching checked decoder217 and payload77, reconstructing diagnostic data and exact ELF relocation/layout, and verifying the full binary. All other original core/dependency gaps remain in scope. Prior Linux evidence belongs to the preceding framework snapshot and does not certify this newer source.

Verify sealed Rust outputs and saved signed receipts without executing a VM:

```
python3 -B repro/donation-relay/anchor-framework-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/anchor-framework-source-recovery/receipt_verify.py --runtime
```
