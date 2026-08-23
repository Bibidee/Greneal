# Greneal

Greneal is a standalone GenLayer semantic change-control firewall. It lets a system owner register an immutable safety boundary for a governed resource, then allows maintainers to propose a change only when deterministic rules and independent GenLayer consensus agree that the change stays inside that boundary. Version 0.2.3 fixes live GenVM web-response compatibility while preserving the v0.2.2 state invariants; older Studionet deployments are legacy.

| Current release | Canonical Studionet deployment |
| --- | --- |
| Version | `v0.2.3` |
| Contract | [`0xf67E7f09355e4859384F1F81c26D83C9dB44a524`](https://explorer-studio.genlayer.com/address/0xf67E7f09355e4859384F1F81c26D83C9dB44a524) |
| Source commit | [`402356ffb3356aab2198e6d8be1fc1e7c4120803`](https://github.com/Bibidee/Greneal/commit/402356ffb3356aab2198e6d8be1fc1e7c4120803) |
| Deployed source SHA-256 | `b7cd0ac27b0b9d8be073581b6acd90b97b744c385b8bc11dbf81fe82575d498c` |

There is no frontend and no off-chain decision service. The only deployable source is `contracts/greneal.py`.

## Why this primitive exists

Parameter updates, upgrades, vendor substitutions, and dependency changes can look harmless at the transaction level while materially changing access, value flow, risk, or reversibility. A fixed allowlist cannot determine whether a natural-language change plan quietly expands a system's authority or defeats its stated safeguards.

Greneal is not a thin “AI decides X” wrapper. It separates deterministic enforcement from the semantic judgment that genuinely requires GenLayer:

1. the owner fixes the resource identifier, designated maintainer, challenge timing, bond, and immutable safety boundary;
2. the boundary commits its baseline URL and digest, while every proposal commits payload and evidence URLs and digests;
3. validators independently fetch all three artefacts, verify SHA-256 over the exact raw bytes, and only then perform semantic review;
4. deterministic contract logic validates the structured result and enforces verdict, challenge, bond, timeout, and actionability transitions;
5. downstream systems receive the committed payload hash and must verify the payload they execute against it.

## Lint and submission policy

`contracts/greneal.py` is the sole contract candidate. Tests, fixtures, deployment helpers, and documentation live outside `contracts/`. `scripts/preflight.py` lints that exact source path and fails if any other Python file enters the deployable directory. GitHub Actions runs the same pinned preflight on push and pull request.

## v0.2 security model

The boundary commits a baseline URL and SHA-256 hash. A proposal commits three immutable artefacts: payload URL/hash, evidence URL/hash, and the boundary's baseline URL/hash. Every validator fetches raw content and programmatically verifies SHA-256 before semantic interpretation. A mismatch, empty response, malformed model result, or unavailable source fails closed and leaves the proposal retryable; an LLM cannot assert payload binding.

### Consensus and enforcement

Validators independently classify `scope_preserved`, `access_expansion`, `economic_risk`, `reversibility`, and `compatibility`. Approval requires the safety conditions and deterministic confidence threshold to pass. The deciding categorical dimensions must agree exactly; rationale remains explanatory and does not participate in equivalence. Validators do not trust the leader's conclusion, fuzzy text matching is not used, and uncertainty or observation failure never becomes approval. Consensus is a replicated semantic judgment—not a guarantee of objective truth.

Approved changes have an open challenge window. The first exact-bond challenge opens one forced public re-review round; later objections need no slot because the proposal is already non-actionable and cannot bypass that round. After the window, anyone may re-review. Approval sends the single bond to a neutral sink, never the maintainer; blocked/inconclusive re-review lets the triggering challenger withdraw once. A second deadline permits anyone to settle a stalled round into that refund state. `is_actionable()` explicitly requires an active boundary, unpaused contract, reviewed approval, no active challenge, no held bond, and the finalization delay. Review artefacts are textual UTF-8: SHA-256 is calculated over raw fetched bytes first, then only verified bytes are decoded for semantic review.

`challenge_count` is permanent audit history, not an eligibility flag. Both `is_actionable()` and `consume_change()` call the same internal predicate: active contract and boundary, `reviewed/approved`, zero held bond, and a delay measured from the latest `reviewed_at`. The default challenge sink is the fixed dead address. A custom sink is a deployment-time trust choice—not provably neutral—and production deployments should use a demonstrably neutral recipient.

Deployment capacity is deliberately finite: 128 boundaries and 1,024 changes. Audit history is retained rather than deleted.

### v0.2.2 to v0.2.3 runtime correction

The v0.2.2 fetch path read `response.status_code`, but the pinned GenLayer runtime exposes `response.status`. Real reviews therefore failed during execution. The fail-closed lifecycle kept each proposal unchanged and retryable: no verdict or actionable permission was fabricated. v0.2.3 uses the supported field and adds regression coverage around `fetch_verified()` with exact-byte hashing and mismatch rejection.

## Studionet deployment evidence

The current hardened deployment is [Greneal v0.2.3 at `0xf67E7f09355e4859384F1F81c26D83C9dB44a524`](https://explorer-studio.genlayer.com/address/0xf67E7f09355e4859384F1F81c26D83C9dB44a524), deployed from source commit [`402356f`](https://github.com/Bibidee/Greneal/commit/402356f) in [transaction `0x47f5…b61ee5`](https://explorer-studio.genlayer.com/tx/0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5). Deployment finalized `SUCCESS` with majority agreement.

Explorer source was retrieved after finalization. Local and deployed source SHA-256 are both `b7cd0ac27b0b9d8be073581b6acd90b97b744c385b8bc11dbf81fe82575d498c`; the 23,885-character sources match byte for byte. The v0.2.2 address `0x39a2128a55aa74753eBF0EC6f3392475E59D25B5` and all earlier deployments are legacy.

Live artefacts are commit-pinned to repository commit `30958818d9d18cc2cfc8cb23216f25a82a78d442`. The baseline digest is `642c1f9f12720e6e7e08a9dfd412bdcb7c4a6367394f24d12d0aab3fd56b9324`; the safe payload digest is `f104fdf07e2abc1394e2fff27a507af7d9f3edee342e7b559752af4d8534be50`; the safe evidence digest is `f7ca797ab87920f22c3ef86bc580631ceda521cd180a4a41d76bc6ed603efc3b`; and the risky payload/evidence digest is `9aec9c169b2d4e33ecad2c2edb4f92cf22b0cf7a92ebc04d30b3b159d1aed000`.

### Live Studionet Validation

| Path | Verified live result |
| --- | --- |
| Safe | `APPROVED`, confidence 93; actionable only after the configured delay |
| Risky | `BLOCKED`, confidence 100 |
| Challenge timeout | Exact bond held; public timeout settlement enabled refund; withdrawal completed; held amount returned to zero |
| Successful re-review | `APPROVED`, confidence 100; bond slashed to the neutral sink; held amount zero |
| Double-settlement protection | Post-slash timeout and withdrawal attempts both reverted |

### Finalized v0.2.3 transaction ledger

| Scenario | Transaction | Final state or observed result |
| --- | --- | --- |
| Deployment | [`0x47f5…b61ee5`](https://explorer-studio.genlayer.com/tx/0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5) | `SUCCESS`, majority agree, source parity exact |
| Main boundary `v023-live` | [`0xbfbd…30f06`](https://explorer-studio.genlayer.com/tx/0xbfbdbcab2abc09249129960316ed1a6c0dafecdc22b7cf1bb1ba2d6e44230f06) | Active, 60-second challenge window |
| Safe proposal `v023-safe` | [`0xe1d7…50766`](https://explorer-studio.genlayer.com/tx/0xe1d78770cfbcfa4028b0ae3c8fcd5113ec88f8c250ab7cd01492c04737450766) | Proposed with verified immutable artefacts |
| Safe review | [`0x25dd…f00f`](https://explorer-studio.genlayer.com/tx/0x25dddf5250cac60e7bf50b6a738e973035f6d39ba6223ae0804ca0aafd56f00f) | `approved`, confidence 93; actionable only after delay |
| Risky proposal `v023-risky` | [`0x0716…966e`](https://explorer-studio.genlayer.com/tx/0x0716d097fc8d4ec34c89d68def388b0aeffef1a82ae80a228bd8f45f00e7966e) | Proposed with verified immutable artefact |
| Risky review | [`0x7ffe…506b`](https://explorer-studio.genlayer.com/tx/0x7ffe88f047807711c5ed790a4dbc593729983cdba14c76b5a89819f85219506b) | `blocked`, confidence 100; access/economic risk detected |
| First challenge-path proposal/review | [`proposal`](https://explorer-studio.genlayer.com/tx/0x991b56c51bb01e0ea5ca4439ac4f4d1bafcf61ee0ec76e19d633ed136c0831e2) / [`review`](https://explorer-studio.genlayer.com/tx/0x8367946391b6da1c6b3833d1b05f38b70830ed800259dfb0ab653c56e947573c) | Approved; test challenge was submitted after the short window |
| Expected late-challenge rejection | [`0xaa50…395ed6`](https://explorer-studio.genlayer.com/tx/0xaa50b552dc892e92be991427f87a6a4c0add7ce22bcc336f801c3903bd395ed6) | Finalized rollback; no bond held |
| Timeout-path proposal/review | [`proposal`](https://explorer-studio.genlayer.com/tx/0x78972fdaf96c7434e8164c4776314d4c5b941dbe5fb1aea2f911427da78101e7) / [`review`](https://explorer-studio.genlayer.com/tx/0x6862e9979aba9e61daf2cd413b60627c35b914c94fe13b033587c7bda27b60e6) | Approved before challenge |
| Bonded challenge | [`0xb166…1a6e1`](https://explorer-studio.genlayer.com/tx/0xb16619774ebc530d26ccc35d605634da18465d94e225ed8f61b8d52247e1a6e1) | Challenged; exact `0.001 GEN` bond held; non-actionable |
| Late re-review rejection | [`0xc991…90a2`](https://explorer-studio.genlayer.com/tx/0xc991f94b2ac8b3807a15e8ad37ad195080d6f87dd8f15c17545e559254e690a2) | Finalized rollback; challenge remained safely unresolved |
| Timeout settlement | [`0x1302…e303`](https://explorer-studio.genlayer.com/tx/0x13021aed4e52db3c8e471f7fbc093d26f650d3bafe87fc2897e0ec130427e303) | Cancelled into deterministic refund state |
| Refund withdrawal | [`0x1067…934c4`](https://explorer-studio.genlayer.com/tx/0x10671ccd9f37d1684af0a8ab72560631388aec7ebdcf968904bde62aa3d934c4) | Bond returned exactly once; held amount zero |
| Long-window boundary | [`0xef45…c5220`](https://explorer-studio.genlayer.com/tx/0xef45298e5087a1ab10eb3f295e19f43e22812b8a7529b2ac3e5e1f688f2c5220) | Active, 120-second challenge window |
| Re-review proposal/initial review | [`proposal`](https://explorer-studio.genlayer.com/tx/0xd6f0fb3ed7ecbbe2883adf1bb8f78cd6b81a620c1a57b46edce06a86f7be6c1b) / [`review`](https://explorer-studio.genlayer.com/tx/0x6b0a63b1a064872b1b38fdcb688ca0cfae3260d53fdebd81a26dc79a6d1c1384) | Approved before challenge |
| Re-review bonded challenge | [`0xacd5…f191d0`](https://explorer-studio.genlayer.com/tx/0xacd50863a675ee2aa1bc7acdea7ac9ae6730528de91811172881d754d0f191d0) | Exact bond held; proposal non-actionable |
| Successful re-review | [`0x034e…33c12`](https://explorer-studio.genlayer.com/tx/0x034e2767d0b157303dac4612840a2000692e75adf6b331173b38fe5d1c333c12) | Finalized `approved`, confidence 100; bond slashed to neutral sink and held amount zero |
| Expected post-slash timeout rejection | [`0x0bfb…a9ee1`](https://explorer-studio.genlayer.com/tx/0x0bfb67a860b17af959e70f70c64c4e1f7ae00a82fcf91a4e7ac6efa5e47a9ee1) | Finalized rollback; no second settlement |
| Expected post-slash withdrawal rejection | [`0x07bd…32320`](https://explorer-studio.genlayer.com/tx/0x07bdbbc6ff4df8425fd7fe2dd666015816931dc9f090a67b989ab28f1bf32320) | Finalized rollback; no refund after slashing |

The safe path became actionable only after its configured 60-second delay elapsed. The risky path remained non-actionable. Both challenged proposals were non-actionable while their bonds were unresolved. The two challenge paths prove timeout refund/withdrawal and successful re-review/slashing, with held accounting returning to zero in each terminal outcome.

## Release validation

- 27 Direct Mode tests passed.
- 16 preflight invariants passed.
- GenVM lint passed 3/3 checks on the sole deployable source.
- ABI schema generation passed.
- Exactly one deployable contract source exists: `contracts/greneal.py`.

Run `python scripts/preflight.py` for the complete release gate; it includes Direct Mode, syntax and invariant checks, GenVM lint, and schema generation.

## Intentional limitations

- External artefact availability affects liveness; unavailable content remains retryable and fail-closed.
- Validator semantic disagreement can prevent approval or require retry; consensus does not guarantee objective truth.
- Review artefacts must be bounded textual UTF-8, although integrity is computed over raw bytes before decoding.
- Each deployment has finite lifetime capacity: 128 boundaries and 1,024 changes.
- A custom `challenge_sink` is a deployment-time trust/configuration choice; the canonical deployment uses the default neutral dead-address sink.

For a one-page reviewer brief, see [`docs/SUBMISSION.md`](docs/SUBMISSION.md). Historical deployments remain documented in [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) and are explicitly marked legacy/superseded.
