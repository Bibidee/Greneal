# Greneal design

## Core model

A boundary is an immutable safety mandate for one governed resource. It names an owner, a maintainer, a baseline-evidence URL, and a concise safety policy. A change proposal carries a public evidence URL, a declared summary, and the hash of the exact change payload that an integrator must later execute.

## Consensus decision

Validators independently inspect both evidence documents. They produce a structured decision over scope preservation, access expansion, economic-risk increase, reversibility, compatibility, evidence quality, and confidence. Only exact agreement on the load-bearing fields is accepted. Missing or malformed evidence fails closed as `inconclusive`; it never becomes approval.

## Lifecycle

`create_boundary` -> `propose_change` -> `review_change` -> challenge window -> `consume_change`

A proposal can instead be blocked, inconclusive, cancelled, or challenged for one re-review. Bonds use the same liveness rule as the rest of the system: if re-review cannot complete before the timeout, a public settlement route must return the held challenger bond and cancel the proposal.

## Integration

Greneal is an authorization signal, not an executor. Before acting, an integrator must check `is_actionable`, verify the resource identifier, and verify that `keccak256(actual_payload)` equals the committed change digest.

