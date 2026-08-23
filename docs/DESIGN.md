# Greneal design

## v0.3.0 hardening model

Each baseline, payload, and evidence response is hashed over exact raw bytes, limited to 12,000 bytes, decoded strictly as UTF-8, and then presented in full to semantic review. Oversized input is rejected rather than truncated, eliminating any committed but semantically hidden tail.

Authorization and state transitions are deterministic. Only independently fetched, hash-verified artefacts and semantic safety classification enter GenLayer consensus. A boundary commits a HTTPS baseline URL and SHA-256 hash; a proposal commits payload URL/hash and evidence URL/hash. Validators fetch raw bytes with `gl.nondet.web.get`, SHA-256 the exact bytes, and fail closed if any commitment differs before decoding verified UTF-8 text. The LLM receives the verified payload, baseline, and evidence; it never decides payload binding. Binary/non-UTF-8 artefacts are intentionally unsupported and fail closed without approving or mutating the proposal.

### Challenge lifecycle

`reviewed/approved` changes accept one exact triggering bond. That first challenge changes state to `challenged` immediately and forces the proposal through a public re-review round; additional people need no participant slot to obtain protection because no proposal can bypass the round. Re-review is callable by anyone only after the original window closes. An approved re-review records a fresh `reviewed_at`, enforces a fresh finalization delay, and transfers the bond exactly once to the deployment's neutral challenge sink—not to the maintainer. Blocked/inconclusive re-review opens one exact refund claim for the triggering challenger. If nobody completes re-review by the second deadline, anyone can settle to the same refund state. Pause and closure never prevent settlement or withdrawal; the held value is zeroed before transfer so it cannot be paid twice.

`challenge_count` remains `1` after re-review as audit history. It does not gate eligibility. One canonical `_actionable(change, boundary)` predicate drives both the public view and `consume_change`: contract unpaused, boundary active, `reviewed/approved`, no held challenge bond, and the latest `reviewed_at` plus finalization delay elapsed. This prevents view/write divergence and makes a successfully re-approved proposal actionable only after its fresh delay.

The default sink is the fixed dead address. A custom constructor sink is an observable deployment-time configuration but cannot be proven neutral solely from its address; production deployers must choose an independently governed or otherwise demonstrably neutral sink.

### Consensus and capacity

Validators independently observe and classify five safety-critical dimensions. The deciding categorical dimensions must agree exactly; rationale is excluded from equivalence, while confidence is validated and used deterministically in verdict derivation. This can produce retryable disagreement, intentionally: uncertainty never approves. Audit history remains bounded at 128 boundaries and 1,024 changes per deployment; it is not deleted to regain capacity.

## Core model

A boundary is an immutable safety mandate for one governed resource. It names an owner, a maintainer, a baseline URL/hash commitment, and a concise safety policy. A change proposal carries payload and evidence URL/hash commitments, a declared summary, and the hash of the exact payload that an integrator must later verify before execution.

## Consensus decision

Validators independently inspect the complete accepted baseline, payload, and evidence artefacts. They produce a structured decision over scope preservation, access expansion, economic-risk increase, reversibility, compatibility, confidence, and explanatory rationale. Only exact agreement on the load-bearing categorical fields, together with the deterministically derived verdict, is accepted. Fetch, HTTP, emptiness, hash, size, UTF-8, and malformed-model failures are fail-closed observation failures: `review_change()` does not approve or mutate the proposal, so the proposal remains unmodified and can be retried when the failure is genuinely transient.

## Lifecycle

`create_boundary` -> `propose_change` -> `review_change` -> challenge window -> `consume_change`

A proposal can instead be blocked, inconclusive, cancelled, or challenged for one re-review. Bonds use the same liveness rule as the rest of the system: if re-review cannot complete before the timeout, a public settlement route must return the held challenger bond and cancel the proposal.

## Integration

Greneal is an authorization signal, not an executor. Before acting, an integrator must check `is_actionable`, verify the resource identifier, and compute SHA-256 over the exact raw payload bytes in the same representation that was committed. The resulting lowercase `0x`-prefixed 32-byte digest must equal the proposal's committed `payload_hash`.

## Threat model

Greneal addresses lying summaries, mutable or mismatched artefacts, hidden semantic tails, unsafe scope/access/economic expansion, irreversibility, incompatibility, challenge bypass, replay, and double settlement. It mitigates but cannot eliminate prompt injection attempts, correlated validator mistakes, semantic ambiguity, temporary source outages, or later source disappearance. It does not execute payloads, prove external statements objectively true, or make URLs permanently available. Consensus is not objective truth; integrators must verify the exact SHA-256 payload commitment before execution.
