# Greneal

Greneal is a standalone GenLayer semantic change-control firewall. It lets a system owner register an immutable safety boundary for a governed resource, then allows maintainers to propose a change only when deterministic rules and independent GenLayer consensus agree that the change stays inside that boundary. Version 0.2.1 is a material source change; the currently recorded Studionet v0.1.3 deployment does not contain these hardening changes.

There is no frontend and no off-chain decision service. The only deployable source is `contracts/greneal.py`.

## Why this primitive exists

Parameter updates, upgrades, vendor substitutions, and dependency changes can look harmless at the transaction level while materially changing access, value flow, risk, or reversibility. A fixed allowlist cannot determine whether a natural-language change plan quietly expands a system's authority or defeats its stated safeguards.

Greneal separates deterministic enforcement from semantic review:

1. the owner fixes the resource identifier, designated maintainer, review window, bond, and safety boundary;
2. the maintainer commits a change proposal with a public evidence URL and an immutable digest of the declared change;
3. validators independently retrieve baseline and change evidence and assess the defined safety dimensions;
4. exact consensus agreement is required on the dimensions that decide whether the change is within scope;
5. only an approved result that survives a challenge window becomes eligible for downstream execution.

## Lint and submission policy

`contracts/greneal.py` is the sole contract candidate. Tests, fixtures, deployment helpers, and documentation live outside `contracts/`. `scripts/preflight.py` lints that exact source path and fails if any other Python file enters the deployable directory. GitHub Actions runs the same pinned preflight on push and pull request.

## v0.2 security model

The boundary commits a baseline URL and SHA-256 hash. A proposal commits three immutable artefacts: payload URL/hash, evidence URL/hash, and the boundary's baseline URL/hash. Every validator fetches raw content and programmatically verifies SHA-256 before semantic interpretation. A mismatch, empty response, malformed model result, or unavailable source fails closed and leaves the proposal retryable; an LLM cannot assert payload binding.

Approved changes have an open challenge window. The first exact-bond challenge opens one forced public re-review round; later objections need no slot because the proposal is already non-actionable and cannot bypass that round. After the window, anyone may re-review. Approval sends the single bond to a neutral sink, never the maintainer; blocked/inconclusive re-review lets the triggering challenger withdraw once. A second deadline permits anyone to settle a stalled round into that refund state. `is_actionable()` explicitly requires an active boundary, unpaused contract, reviewed approval, no active challenge, no held bond, and the finalization delay. Review artefacts are textual UTF-8: SHA-256 is calculated over raw fetched bytes first, then only verified bytes are decoded for semantic review.

Deployment capacity is deliberately finite: 128 boundaries and 1,024 changes. Audit history is retained rather than deleted.

## Studionet deployment evidence

The canonical deployment is [Greneal at `0x0B33f933C664E651841270941eaF5F496c994547`](https://explorer-studio.genlayer.com/address/0x0B33f933C664E651841270941eaF5F496c994547). It was deployed from commit [`bf8712f`](https://github.com/Bibidee/Greneal/commit/bf8712f6405cb5a9e2b11de03fd16b275bb29fd0) in [deployment transaction `0x2e5ce4…3ea6f`](https://explorer-studio.genlayer.com/tx/0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f), finalized `SUCCESS` with majority agreement.

Exact source retrieval parity was checked after finalization. Local and deployed SHA-256 are both `ee5d00c9cd0322b15b8e5abd53b67b1f531fbfc5df2efc642c1cf3eb03a2b4fa` (byte-for-byte match).

The release gate passed: 13 Direct Mode tests, GenVM lint for the sole deployable source, and ABI schema generation. Live state setup is also finalized: [boundary creation](https://explorer-studio.genlayer.com/tx/0x72949ba130e1eb1c3d31525fc06a1aa8be534c882e231a6e27cb7a8ddc3bf778) and [safe proposal creation](https://explorer-studio.genlayer.com/tx/0xfac2654f938224f506f590cc13de815b297b5a407b5d5feba244fa0c688fe7b3).

The initial live semantic reviews used an external baseline page and finalized without state mutation because that evidence dependency was unavailable. This is the designed retryable path: the proposal remains `proposed`; no verdict, challenge bond, or actionable permission was fabricated. The replacement live boundary uses a versioned, public baseline document in this repository; the approved/blocked verdict paths and challenge expiry/refund route remain covered by the Direct Mode matrix.
