# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. Original ELF830448bytes SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile reconstructed Rust; raw captured ELF/assembly files are analysis-only, and decoded metadata is expressed explicitly in Rust.

The current source uses real Anchor-generated IDL, event-recursion, whitelist and donate_v1 routes. Donation uses typed state, actual generated initialization/PDA/account constraints, token interfaces, transfer/reload, event emission/self-CPI and return serialization. The reconstructed mint-safety policy remains in the handler; its exact source remains unresolved. Other business routes retain the previous independent arena/context/wrapper implementation. The obsolete manual whitelist selector/wrapper is removed; an obsolete manual donate_v1 route still remains inside legacy dispatch and needs pruning.

Selected native platform-tools v1.48 output703032bytes SHA256 `82669343549ca31f6fd5ef20e995cb294abd468026e7b71164621bc5b238b9c5`; unstripped830024bytes SHA256 `8533568204dc8b915577f53b4543f48b76e910f27d55e7518ae3461568870315`. A fresh build from this repository path reproduces both exactly. [generated-donation-source-recovery](../../repro/donation-relay/generated-donation-source-recovery/README.md) binds34inventoried Rust/config inputs, complete ELF ledgers, primary dependency source and signed receipts. README/LICENSE/NOTICE are ancillary.

Complete normalized original-window matches increase328→361,33gains and no losses. Raw matches77;131of492windows remain unmatched. New matches include three donation initialization closures, typed state decoders, event serialization, token-interface admissions/reload and real token/associated-token CPI helpers. Main parser121 and exit125 still differ. Normalization masks only direct-call displacements and relocation immediates; matching instruction shape is not complete data/call/indirect/allocator closure or whole ELF identity.

The selected candidate passes121distinct finite scenarios, including18new initialized tracker/debouncer rejects. Compared public keys and decoded source origins repair four old manual-control log mismatches. The preceding103cases include actual donation effects, malformed argument/allocation cases, whitelist rejection/create/prefunded CPI and rollback. Valid ephemeral signatures and real account privileges are required; no historical relayer is substituted. Fixed-relayer success, arbitrary inputs/allocations and wider swap/distribution behavior remain unverified. Full observations are retained; the frozen comparator excludes compute-metering lines and executable-image account bytes.

Anchor SPL0.31.1 and two associated-token packages are added without altering prior registry package entries. All176active package source trees were checked against authenticated crate archives. Both77framework implementations and34program error names/messages are rederived from this actual output. Source paths/macro coordinates preserve observed diagnostic data rather than attributing reconstructed comments to historical authors. Existing documented whitelist call-boundary annotations remain. No binary is patched and no target instruction blobs enter the source.

```
python3 -B repro/donation-relay/generated-donation-source-recovery/verify.py --current --check-registry-source
work/test-env/bin/python -B repro/donation-relay/generated-donation-source-recovery/receipt_verify.py --runtime
```

These rederive sealed source/output/data proofs and saved transaction observations without VM execution. Earlier --current checks intentionally fail after source advances; historical verifiers remain valid. Full business parser/exit/shared-body recovery, remaining contexts/wrappers, dispatcher169/helper34 and ELF data/relocation/layout equality remain within the all-contract Rust-only goal. No whole-contract acceptance count increases.
