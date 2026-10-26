# Relay typed mint-policy reconstruction

This checkpoint reconstructs the mint policy with SPL Token's typed extension APIs. Acceptance still requires reconstructed Rust to rebuild every captured whole ELF byte for byte. This checkpoint does not meet that requirement.

The selected Rust output matches 403 complete original function windows after only direct-call displacement and relocation-immediate normalization. There are 80 raw matches and 89 unmatched original windows. Gains over the preceding 397-window native checkpoint are 30, 31, 32, 238, 241 and 252; no previous matches are lost. Windows 30–32 are full typed extension lookups for NonTransferable, DefaultAccountState and MintCloseAuthority. The other gains cover TLV indices, extension-type conversion and the optional-key conversion. Counts are inferred-window evidence, not a percentage of recovered source or whole-file identity.

## Selected Rust and dependencies

`policy/source` contains the 38 inventoried Rust/config inputs, including the lockfile. All five generated donation handlers now call the public typed mint-account policy. It borrows mint data, unpacks StateWithExtensions, rejects base mint/freeze authority, and checks transfer-fee authority/basis points, transfer hooks, permanent delegates, close authority, default state and nontransferability. Lookup errors remain suppressed, as the capture does. Whitelisted/native mints retain their observed bypass. Settlement routes retain the prior arena reconstruction.

The direct SPL Token-2022 dependency is now pinned to 7.0.0. Anchor SPL still resolves its own 6.0.0 dependency. The only added registry records are Token-2022 7.0.0 and confidential-transfer proof generation 0.3.0; all preexisting package records remain unchanged apart from dependency-string version disambiguation and the root's direct 7.0.0 selection. Public immutable crate archives, index checksum records, selected source members and full archive-member inventories authenticate the additions. The freshly executed registry audit verifies all 177 registry packages resolved for this target: 4,055 files / 37,402,916 bytes, exactly equal to their pinned archives. This does not identify unique historical package versions.

A private v6 policy compiled to 3,432 bytes with promoted arguments. Public v6 preserves the 3,440-byte boundary but lacks recognized extension tags 25–27. An aliased v7 trial inlines the decoder and produces a 4,016-byte policy. Direct v7 also serves the existing runtime's real decoders and restores the 3,440-byte boundary. These measured source variants are retained. One failed source trial imported Anchor's one-parameter Result over existing two-parameter results; explicit imports repair that compile failure. Equivalent primitive, bit-mask, operand-order, boolean, POD-comparison and tuple fee checks were measured rather than assumed to match.

The selected fee-mask form has exactly three differing normalized instructions against the entire original policy window 106, at offsets 1360, 1368 and 1376. They use the other register for the combined basis-point result. `policy_residual.py` rederives these residuals and the actual calls to recovered windows 30–32. **Window 106 remains unmatched.** There is no register/stack/branch masking, instruction patching, embedded target-code blob or assembly compiler input. Equivalent source variants that produce the same ELF are not extra recovery gains.

Selected platform-tools v1.48 output:

- Stripped: 868,224 bytes; SHA-256 `42fcde021f4572737fb8eaf515f0e74728f6b8620d744207a323bb7d1f447131`.
- Unstripped: 999,776 bytes; SHA-256 `55f719233458e995528bb81d332a0145e2d215dfc1261450fb65931305242299`.
- Capture: 830,448 bytes; SHA-256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`.

A fresh build from the final repository source path reproduces both selected outputs exactly. The candidate remains larger than the capture. Ten successful Rust builds are retained: selected output, eight successful background variants, and final-path reproduction. The separate failed import trial is retained. Full source/build commands and logs, both ELF forms, all function/call/data/relocation/section/positional-residual ledgers and actual 34 program plus two 77-framework name/message implementation proofs are bound by the manifest. README/LICENSE/NOTICE are ancillary and are not compiled inputs.

## Runtime evidence

All 241 distinct finite scenarios pass on this exact candidate: the previous 214 plus 27 new Token-2022 mint-policy cases. The new cases run the captured Token-2022 executable with real signatures, privileges, blockhash checks and transaction history. Canonical source/destination token accounts are initialized with zero withheld balances so these cases isolate policy behavior from ATA creation. They cover base/empty headers; mint/freeze authority; fee configuration versus withdrawal authority; old/new fee rates; hook authority/program; permanent delegate; close authority; initialized/frozen/uninitialized default state; nontransferability; malformed fee length; unknown extension; whitelist bypass; and recognized tags 25/26 preceding unsafe extensions. Unknown-extension lookup failure is intentionally suppressed even when it hides a later unsafe extension; this is captured behavior, not a proposed policy fix.

The original, preceding native control and selected candidate agree in all 27 new cases. The independent receipt verifier reconstructs exact fixture mutations, rent, canonical token PDA seeds, account metas and transaction bytes. It checks the actual loaded Token-2022 program hash, token transfer CPI bytes/order/accounts, token/state/event/return effects, tracker/debouncer rent debit and complete non-fee-payer rollback on rejection. Its `--runtime` option verifies cryptographic signatures and canonical PDA derivation; it does not execute VMs. Final saved receipts contain 1,475 signature fields across 241 cases. Repeated background runs are not added to the distinct case count.

Full VM observations are retained. The unchanged comparator omits compute-metering log lines and executable-image bytes. The new fixtures establish finite Token-2022 policy coverage; native Token-2022 routing, arbitrary allocator/drop/input behavior, fixed-relayer/settlement success and security acceptance remain unproved.

## Verification and remaining work

```sh
python3 -B repro/donation-relay/typed-mint-source-recovery/verify.py --current --check-registry-source
work/test-env/bin/python -B repro/donation-relay/typed-mint-source-recovery/receipt_verify.py --runtime
```

These commands rederive saved source/output/function/data/call/registry/receipt evidence without executing any captured or candidate program. Build scripts and runtime runners preserve their actual work-directory invocations; copying them out of their recorded directory is not a reproducible command substitution. Earlier `--current` checks intentionally fail once source advances; historical verifiers remain usable.

Next work remains exact policy106/common donation112, top-level donation handler/event wrappers, generated settlement contexts, dispatcher169 and complete data/relocation/layout closure. The four core contracts and all remaining dependencies retain their full Rust-only whole-ELF acceptance requirements. No whole-contract identity count increases. Shared checkout/index/license and unrelated core work are preserved; publication stays on the isolated Relay research branch. Hosted CI is reported separately from local source/output/receipt evidence.
