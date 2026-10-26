# Relay shared donation and wrapper reconstruction

Acceptance still requires reconstructed Rust to rebuild every captured whole ELF byte for byte. This checkpoint does not establish whole-contract identity. It replaces the five duplicated donation bodies with a common Rust context, arguments and amount result, restores instruction handlers and program-layer event emission, and preserves actual account, token, funding and error behavior.

The selected output matches **416 complete original windows after normalization, including 80 raw matches**. Normalization masks only direct-call displacements and relocation immediates. Against the preceding 403-window checkpoint, gains are 51, 104, 107, 110, 111, 178–182 and 190–193. Window21, the old token-account reload specialization, is no longer emitted. Net gain is13;76 of492 original inferred windows remain unmatched. The removed reload came from the prior context-specific donation implementation. The captured common function instead deserializes raw token data before and after transfer. No redundant reload or unused function was added to retain a count; its legitimate settlement callers remain to reconstruct.

## Rust recovery and measured variants

The common context has four borrowed references and four owned AccountInfo values: epoch tracker, debouncer, signer and whitelist references, followed by destination token, mint, source token and token program accounts. Compiler diagnostics report224bytes. DonationArgs is72bytes: message at0, config at24, amount at56, tip at64, epoch bump at66 and debouncer bump at67. The common result carries only epoch, received amount and tip:32bytes, or40bytes inside Result. Event construction happens in the outer instruction handlers. `shared_evidence.py` independently checks these compiler reports and actual original/candidate call edges.

The exact shared-context drop body528bytes, message checker536bytes, basis-point checker544bytes and both deserialization helpers288bytes now match. Explicitly binding the borrowed data slice restores the original deserializer scratch-slot reuse; acceptance still compares entire bodies without stack masking. Whole state initialization uses real Account::set_inner. Per-byte config equality restores the observed comparison shape. Owned AccountInfo CPI fields use direct clone calls, matching the inline Rc clone sequences in the capture; the signer retains its actual ToAccountInfo helper.

A crucial call-map correction is explicit: generated wrappers178–182 do not directly call handlers92–95. They call program functions190–193, which emit log/self-CPI events and call the instruction handlers; those handlers call common112. The original generated wrappers also contain an indirect serialization call. `shared_evidence.py` decodes the direct chain rather than silently skipping the program layer. Full indirect/data closure is not claimed.

The earlier private Anchor container allowed program functions to inline into generated wrappers. Public visibility restores the separate layer and all five complete generated wrapper bodies. Capturing the two bump bytes before constructing instruction arguments restores all four complete3096-byte program functions. These are measured compiler effects, not proof of unique historical source text. A paired-bump source variant emits the same stripped ELF and is not counted as an additional gain.

The common body112 remains unmatched: original10248bytes versus selected10328bytes, each with51 direct calls. The two regular instruction-handler bodies are2552bytes versus original2568; native bodies are6344 versus6272. Whole-body differences, including register, branch and stack choices, remain real acceptance failures. Original policy106 also remains unmatched; its three normalized register-choice residuals are rederived separately. No register/stack/branch masking, new forced-inlining attributes, target-code assembly, executable fragments, binary patching or unsafe source was added.

Fifteen measured source forms plus final-path reproduction are retained: **16 successful Rust builds**, no failed source builds. They include an unchanged-source geometry control, the initial split with a shifted macro coordinate, aggregate initialization and borrowed arguments, explicit deserializer slice binding, outer handlers, iterator equality and owned arguments, direct clones, borrowed args, tuple result, owned/reference mint helpers, dead-code pruning, public container, early field binding and paired bumps. The first split loses generated IDL matches because it shifts the program macro; the corrected forms preserve the captured line36. Several equivalent variants share stripped outputs. No source variant is accepted from size alone.

## Selected output and runtime evidence

The selected40 Rust/config inputs use unchanged Cargo.toml and Cargo.lock records from the preceding checkpoint. Direct Token-2022 remains7.0.0 and Anchor SPL retains its own6.0.0. All177 target-resolved registry packages are freshly checked against pinned archives:4055files/37402916bytes. The unchanged primary archive/index/member proofs are retained. Source snapshots preserve LICENSE/NOTICE; documentation is separate from compiled inputs.

- Selected stripped ELF:865096bytes, SHA-256 `6dfbc4d8339c9a6046d61cac6ee932fd15838abc73dd0369f7ea70979c4dd45e`.
- Selected unstripped ELF:998728bytes, SHA-256 `e0eaf6d7f33b26818eef7fea2a3b55549d22478d4ffe9198663e5cccca2a40ba`.
- Original capture:830448bytes, SHA-256 `367f07a62e3f74d358187d175cf3228848e81a56c781a9a75b9df7fed1268563`.

A fresh build from the final repository path reproduces both selected outputs exactly. The trial's print-type-sizes flag only requests diagnostics; the final-path reproduction omits it. Both outputs agree. Complete source/config, build commands/logs, stripped/unstripped ELFs, function/call/data/relocation/section/positional-residual ledgers and final34 program plus two77 framework name/message implementation proofs are sealed. Candidate size remains greater than the capture.

All **241 distinct finite scenarios pass on the exact selected output**, including the prior native/payer/IDL/business cases and27 Token-2022 policy fixtures. Real signatures, privileges, blockhash checks and transaction history remain enabled. Independent saved-receipt verification checks1475signature fields, cryptographic signatures, exact fixture/PDA/rent/transaction bytes, loaded Token-2022 executable hash, CPI order/accounts/data, token/state/event/return effects and rejection rollback. Repeated intermediate runs are not extra distinct scenarios. The verifiers do not execute VMs; the runtime runners did.

Full observations remain saved. The unchanged comparator excludes compute-metering log lines and executable-image bytes. These are finite checks, not proof for arbitrary allocator/RefCell/input states, native Token-2022 routing, fixed-relayer/settlement success or security acceptance.

```sh
python3 -B repro/donation-relay/shared-donation-source-recovery/verify.py --current --check-registry-source
work/test-env/bin/python -B repro/donation-relay/shared-donation-source-recovery/receipt_verify.py --runtime
```

These commands rederive source/output/layout/call/registry/receipt evidence without VM execution. Build/runtime scripts retain the actual work-directory invocations; moving a script is not a substituted reproduction command. Earlier --current checks intentionally fail once source advances; historical verifiers remain usable.

Next work remains exact common112/policy106 and instruction handlers92–95, genuine settlement callers of reload21, the six generated settlement contexts and handlers, dispatcher169, source/package/module topology, and full data/relocation/layout closure. The original all-contract Rust-only goal stays active. This checkpoint establishes no additional whole-contract byte identity. Shared checkout/index/license and unrelated core edits are preserved. Hosted CI remains a separate gate; the preceding workflow failed an unchanged Pump source-binding assertion.
