# Greneal — Semantic Change-Control Firewall

**Category:** GenLayer Intelligent Contracts

**Current version:** v0.3.0

**Current contract:** [`0x60797a1368C093DB8609Ca301c0d13fC81f5a239`](https://explorer-studio.genlayer.com/address/0x60797a1368C093DB8609Ca301c0d13fC81f5a239)

**Deployment:** [`0x76c9c4d24e949483a8d025af6c1cb2fc467541cd764184d57c4714a7aab2aa78`](https://explorer-studio.genlayer.com/tx/0x76c9c4d24e949483a8d025af6c1cb2fc467541cd764184d57c4714a7aab2aa78)

**Source commit:** [`93e53d7`](https://github.com/Bibidee/Greneal/commit/93e53d7)

**Source SHA-256:** `6a7d3f721dc53e7616bccb83b2450f9bee6cce8e29862787ee0cebdc2f5e26a6` (exact deployed/local parity)

## Fresh v0.3.0 live proof

- Safe review: [`APPROVED`](https://explorer-studio.genlayer.com/tx/0x792d5203ce3fe1d5e38814a29c1ed157d275d21740092fe5461037d3ad0d33dc).
- Risky review: [`BLOCKED`](https://explorer-studio.genlayer.com/tx/0x4494022dabed4da0c48740237c545e27077d3628109c0f3b30063068bd5de70e).
- Integrity mismatch: [review rolled back](https://explorer-studio.genlayer.com/tx/0x8d65b51abac395e2dbb11ec43bebfc3f1a99ea98e99df94608ad401dcf69b80a) with proposal unchanged.
- Bonded challenge: [`0xbd63a649…`](https://explorer-studio.genlayer.com/tx/0xbd63a6495cc208c08b9c1a5b90083d82d6e395df30a1b5d5b5a58a9848f4c227).
- Successful approved re-review/slash: [`0x3641b21c…`](https://explorer-studio.genlayer.com/tx/0x3641b21cd0596b735de87bba39a3097f3d955a9076159f7e49e09139c52690f8), held bond zero.

## Purpose

Greneal is a reusable semantic change-control firewall. An owner establishes an immutable safety boundary for a governed resource. A maintainer commits a payload and supporting evidence, but the change cannot become actionable until cryptographic integrity checks, independent GenLayer semantic consensus, deterministic verdict rules, and the challenge delay all pass.

## Why GenLayer consensus is necessary

Whether an upgrade preserves scope, expands authority, increases economic risk, remains reversible, or preserves compatibility cannot be decided safely by hashes or keyword matching alone. Validators independently fetch hash-pinned baseline, payload, and evidence artefacts, verify SHA-256 over exact raw bytes, and classify those semantic dimensions. Exact agreement is required on the deciding categorical fields and the deterministically derived verdict; rationale is explanatory only, and uncertainty never approves.

## Security model

Authorization, storage bounds, SHA-256 commitments, structured-result validation, verdict derivation, challenge timing, bond accounting, settlement, replay protection, and actionability are deterministic. Each accepted baseline, payload, and evidence artefact is limited to 12,000 raw bytes, decoded strictly as UTF-8, and reviewed in full rather than truncated. Fetch, HTTP, empty-response, hash, size, UTF-8, and malformed-model failures fail closed: they do not approve or mutate the proposal. A valid challenge makes the proposal non-actionable and forces a public re-review lifecycle. Stalled review has a public timeout/refund route; successful approved re-review slashes the bond to the neutral sink. Downstream integrators must compute SHA-256 over the exact raw executable payload bytes and compare the resulting lowercase `0x`-prefixed digest with the committed `payload_hash` before execution.

## Legacy v0.2.3 supporting proof

The following transactions are retained only as historical evidence for lifecycle branches that were already demonstrated on the superseded v0.2.3 deployment. They are not the canonical v0.3.0 deployment evidence above.

- Safe review: [`APPROVED`, confidence 93](https://explorer-studio.genlayer.com/tx/0x25dddf5250cac60e7bf50b6a738e973035f6d39ba6223ae0804ca0aafd56f00f).
- Risky review: [`BLOCKED`, confidence 100](https://explorer-studio.genlayer.com/tx/0x7ffe88f047807711c5ed790a4dbc593729983cdba14c76b5a89819f85219506b).
- Timeout/refund: [challenge](https://explorer-studio.genlayer.com/tx/0xb16619774ebc530d26ccc35d605634da18465d94e225ed8f61b8d52247e1a6e1), [public settlement](https://explorer-studio.genlayer.com/tx/0x13021aed4e52db3c8e471f7fbc093d26f650d3bafe87fc2897e0ec130427e303), and [withdrawal](https://explorer-studio.genlayer.com/tx/0x10671ccd9f37d1684af0a8ab72560631388aec7ebdcf968904bde62aa3d934c4).
- Successful re-review/slash: [`APPROVED`, confidence 100](https://explorer-studio.genlayer.com/tx/0x034e2767d0b157303dac4612840a2000692e75adf6b331173b38fe5d1c333c12), held amount zero.
- Double-settlement protection: post-slash [timeout](https://explorer-studio.genlayer.com/tx/0x0bfb67a860b17af959e70f70c64c4e1f7ae00a82fcf91a4e7ac6efa5e47a9ee1) and [withdrawal](https://explorer-studio.genlayer.com/tx/0x07bdbbc6ff4df8425fd7fe2dd666015816931dc9f090a67b989ab28f1bf32320) reverted.

## Validation and limitations

Release gates pass: 33 Direct Mode tests, 16 preflight invariants, GenVM lint 3/3, ABI schema generation, and exactly one deployable source.

External artefact availability can affect liveness and validator semantic disagreement can prevent approval or require retry; both conditions preserve fail-closed safety. Review artefacts are bounded textual UTF-8. Each deployment has finite capacity of 128 boundaries and 1,024 changes. A custom challenge sink is a deployment-time trust/configuration choice rather than a consensus property; the canonical deployment should use an appropriately neutral sink.
