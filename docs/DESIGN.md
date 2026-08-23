# Greneal design

## v0.2 hardening model

Authorization and state transitions are deterministic. Only independently fetched, hash-verified artefacts and semantic safety classification enter GenLayer consensus. A boundary commits a HTTPS baseline URL and SHA-256 hash; a proposal commits payload URL/hash and evidence URL/hash. Validators fetch raw content with `gl.nondet.web.get`, SHA-256 it, and fail closed if any commitment differs. The LLM receives the verified payload, baseline, and evidence; it never decides payload binding.

### Challenge lifecycle

`reviewed/approved` changes accept up to eight unique bonded challengers for the complete challenge window. A first challenger cannot occupy the only slot: other unique challengers may join until the window closes. The change is `challenged` and never actionable during that period. Re-review occurs after the window. An approved re-review deterministically slashes the aggregate pool to the maintainer; blocked/inconclusive re-review opens an exact withdrawal claim for every challenger. If nobody completes re-review by the second deadline, anyone can settle to the same refund state. Pause and closure never prevent settlement or withdrawal; each claim is zeroed before transfer so it can be withdrawn only once.

### Consensus and capacity

Validators independently observe and classify five safety-critical dimensions. Their exact categorical verdict must agree; rationale is excluded from equivalence. This can produce retryable disagreement, intentionally: uncertainty never approves. Audit history remains bounded at 128 boundaries and 1,024 changes per deployment; it is not deleted to regain capacity.

## Core model

A boundary is an immutable safety mandate for one governed resource. It names an owner, a maintainer, a baseline-evidence URL, and a concise safety policy. A change proposal carries a public evidence URL, a declared summary, and the hash of the exact change payload that an integrator must later execute.

## Consensus decision

Validators independently inspect both evidence documents. They produce a structured decision over scope preservation, access expansion, economic-risk increase, reversibility, compatibility, evidence quality, and confidence. Only exact agreement on the load-bearing fields is accepted. Missing or malformed evidence fails closed as `inconclusive`; it never becomes approval.

## Lifecycle

`create_boundary` -> `propose_change` -> `review_change` -> challenge window -> `consume_change`

A proposal can instead be blocked, inconclusive, cancelled, or challenged for one re-review. Bonds use the same liveness rule as the rest of the system: if re-review cannot complete before the timeout, a public settlement route must return the held challenger bond and cancel the proposal.

## Integration

Greneal is an authorization signal, not an executor. Before acting, an integrator must check `is_actionable`, verify the resource identifier, and verify that `keccak256(actual_payload)` equals the committed change digest.
