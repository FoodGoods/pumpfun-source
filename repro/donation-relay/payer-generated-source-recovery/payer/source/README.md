# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. Original ELF: 830448 bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust; raw captured ELF/assembly files are analysis-only. Decoded source metadata is expressed explicitly in Rust.

The current loader uses real Anchor-generated IDL, event-recursion, whitelist, donate_v1 and donate_pubkey_config_id_v1 routes. Both generated donation contexts use a boxed mint, typed states, genuine initialization/PDA/program constraints, token transfer/reload, event log/self-CPI and return serialization. The independently reconstructed mint policy remains; exact shared donation body recovery is still open. Obsolete manual selectors/wrappers for the three generated business routes are removed. Native/payer/settlement routes still use the prior arena model.

Selected native platform-tools v1.48 output: 731512 bytes, SHA256 `4ea6e7fb17caae45252f7fdf109d43f1ceed57b8f640ef6c5f46520d5eeacaac`; unstripped 858656 bytes, SHA256 `37ff073b1b24c790a1ed3febe24460e7297c83546d41db8cf6bcd5c4c9661c7f`. A fresh build from this repository path reproduces both exactly. [donation-layout-source-recovery](../../repro/donation-relay/donation-layout-source-recovery/README.md) binds 35 source/config inputs and full ELF/data/receipt evidence. README/LICENSE/NOTICE are ancillary.

Complete normalized original-window matches rise 361→371: ten gains and none lost. Raw matches: 77; 121 of 492 windows remain unmatched. The entire 14472-byte donation parser and 3088-byte exit now match, along with separate state-account exits and allocation-error helpers. Repeated real handler use restores the observed exit call boundaries without new forced-inlining attributes. Normalization masks call displacements and relocation immediates; matching bodies do not establish complete call/data/indirect/allocator closure or whole-file equality.

The selected output passes 139 distinct finite scenarios, including 18 new initialized-state rejects for the public-key-config route. Valid ephemeral signatures, actual account privileges, exact initialized bytes/PDA hashes/rent, CPIs, errors/logs, return data, success effects and rollback are checked. Negative prior-control log mismatches remain recorded. No historical relayer is substituted. Fixed-relayer success, wider native/payer/settlement coverage, every input and general allocator/drop behavior remain unproved. Full observations are saved; the inherited comparator excludes compute-metering lines and executable-image account bytes.

Registry package records are unchanged from the preceding snapshot. Primary account/Box/Program/constraint source members are authenticated, and selected output name/message data is rederived for 34 program codes and both 77-variant framework implementations. Earlier macro-coordinate/source-origin and whitelist call-boundary qualifications remain in their sealed packets. Historical source/compiler uniqueness is not claimed. No binary is patched or target executable fragments embedded.

```
python3 -B repro/donation-relay/donation-layout-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/donation-layout-source-recovery/receipt_verify.py --runtime
```

These rederive sealed current-source/output/data proofs and saved signed observations without VM execution. Earlier --current checks intentionally fail after source advances; historical verifiers remain usable. Public-key exit139, shared body112, top-level wrappers/dispatcher169, other generated business contexts and exact ELF data/relocation/layout remain within the all-contract Rust-only goal. No whole-contract acceptance count increases.
