# Donation Relay reconstructed Rust

Whole captured-byte identity remains unachieved. Original ELF: 830448 bytes, SHA256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`. Builds compile Rust; raw captured ELF/assembly files remain analysis-only. Decoded source metadata is expressed explicitly in Rust.

The loader now uses real Anchor-generated IDL, event-recursion, whitelist, donate_v1, donate_pubkey_config_id_v1 and donate_pubkey_config_id_with_payer_v1 routes. The donation contexts have typed states, boxed mint, actual initialization/PDA/token/program constraints and real separate payer/authority handling. Transfers/reloads, event log/self-CPI and returns execute normally. The reconstructed mint-safety policy remains. The obsolete manual selectors/wrappers for these generated business routes are removed. Native and settlement routes still use the earlier arena implementation; exact common body112 and top-level wrapper recovery remain open.

Selected native platform-tools v1.48 output: 775952 bytes, SHA256 `54b75f94118f3ccbdffba7a76bca6d9375a49ac261d2d47448eb4427709e6eb5`; unstripped 904248 bytes, SHA256 `edb597634249710a83d568e4bfa8a3864a8ee9a2720908d417b619627de03ee9`. A fresh build from this repository path reproduces both exactly. [payer-generated-source-recovery](../../repro/donation-relay/payer-generated-source-recovery/README.md) binds36 inventoried inputs and full ELF/source/data/receipt evidence. README/LICENSE/NOTICE are ancillary.

Complete normalized matches rise371→375: four gains, none lost. Raw matches77;117 of492 windows remain unmatched. New complete bodies are payer parser138, its initialization closures139/140 and exit141. The corrected ELF call map establishes that both non-payer donation wrappers share exit125; historical notes labeling139 a public-key exit were mistaken. Normalization masks call displacements and relocation immediates; complete matching instruction bodies are not whole data/call/indirect/allocator closure or ELF equality.

All162 finite scenarios pass. They include eighteen initialized-state rejects per generated donation route, actual payer permission/funding/alias cases, ordinary effects, prior malformed arguments/allocation controls and whitelist initialization checks. The independent verifier checks actual System CreateAccount data/rent/owners/account order and total payer debit, token/event/return/state effects, signatures/privileges and rollback. Readonly payer correctly triggers runtime privilege escalation during initialization; absent signature and insufficient funding also match. Payer/authority aliasing uses a genuine shared signer/account. No historical authority is substituted.

Full observations are retained; the inherited comparator omits compute-metering lines and executable-image bytes. Fixed-relayer/native/settlement success, arbitrary input/allocator/drop behavior and security acceptance remain unproved. Registry package records are unchanged. Primary sources are authenticated, and final34 program plus both77 framework names/messages are rederived from the actual output. Earlier macro-coordinate/source-origin and whitelist annotation qualifications remain. No binary is patched or executable fragments embedded.

```
python3 -B repro/donation-relay/payer-generated-source-recovery/verify.py --current
work/test-env/bin/python -B repro/donation-relay/payer-generated-source-recovery/receipt_verify.py --runtime
```

These rederive sealed current-source/output/data/call-map proofs and saved finite signed observations without executing programs. Earlier --current checks intentionally fail after source advances; historical verifiers remain usable. Native mint-pair/context recovery, shared donation112/wrappers, settlement contexts and complete dispatcher/data/relocation/layout identity remain within the full all-contract Rust-only goal. No whole-contract acceptance count increases.
