# Greneal — Semantic Change-Control Firewall

**Category:** GenLayer Intelligent Contracts

**Current version:** v0.3.0

**Current contract:** [`0xFa8bfa84889c347201A6D37026A45d65429827cE`](https://explorer-studio.genlayer.com/address/0xFa8bfa84889c347201A6D37026A45d65429827cE)

**Deployment:** [`0x046de466f0ba0402c6c5c4758dcb07643f26f9e48387bb3eb330cf2467bf0573`](https://explorer-studio.genlayer.com/tx/0x046de466f0ba0402c6c5c4758dcb07643f26f9e48387bb3eb330cf2467bf0573)

**Source commit:** [`09ef7cc`](https://github.com/Bibidee/Greneal/commit/09ef7cc)

**Source SHA-256:** `6f6540edbd80341c0abd694c5512a2b2e4990d9ed50165798e29fc5990e467c2` (exact deployed/local parity)

## Fresh v0.3.0 live proof

- Safe review: [`APPROVED`](https://explorer-studio.genlayer.com/tx/0x6731b6bd5b928359a0f66990472a9c52b35c0416ae3d29d3f33f4d5c87c4f3e8); early actionability false, delayed actionability true.
- Risky review: [`BLOCKED`](https://explorer-studio.genlayer.com/tx/0x64cb2273f92960705fe35034265d048400c3778ae9902fe5392d5ceba36bd29d).
- Integrity mismatch: [deterministic integrity rollback](https://explorer-studio.genlayer.com/tx/0x5e161bf900d032fc5d1e709dde72dfa3b752f26953ca97625215b0122da7f31c) with proposal unchanged.
- Approved re-review: [challenge](https://explorer-studio.genlayer.com/tx/0x0ce6a02a99a585c54ef4ff7446dd4449e2ff29f68016573839e4262c346f3dfd), [approved re-review/slash](https://explorer-studio.genlayer.com/tx/0x1e6c519c2cefb39da045cbe2b80e86b0e854b000c869fa77427730b2b573e93d), held bond zero and fresh delay enforced.
- Timeout/refund: [challenge](https://explorer-studio.genlayer.com/tx/0xb07e137c1bdb4fbc3fc8f59f905efa2b691a50b765d394c485a6cdc06de2c614), [public settlement](https://explorer-studio.genlayer.com/tx/0x54700b9c61b627895aad3f949228306549a46045c10960dcde4796ea3664a8db), and [withdrawal](https://explorer-studio.genlayer.com/tx/0xeccf05eab4977c024f83fb3ee90eca80fb220fc7c00b07cf419f9e24ca619cf5).
- Double settlement rejected: post-slash [timeout](https://explorer-studio.genlayer.com/tx/0x568972f43abb94d5048d23bde9186d1fd7286f24a99a2cdce67d9c899fc0107b) and [withdrawal](https://explorer-studio.genlayer.com/tx/0x63ddc4123366d5cf6f9cc7b81bfa202cd8d9910a4501e44c8a03b037cde36def); post-refund second [withdrawal](https://explorer-studio.genlayer.com/tx/0x415aea9120e0f7c63e73a2dd9dcae9759ddd723b9af03b1dd3ef1eb2f4c7663f) and [settlement](https://explorer-studio.genlayer.com/tx/0xd58bc7c9bbf115e5f2f5cd3651dec14b2541e97fbf3da01a77981442d3905425) all reverted.
- [Late challenge](https://explorer-studio.genlayer.com/tx/0x2d29335786f0d99dd443a9c123c425943dff7d413f63f231cd835a72525d5198) reverted after finalization.

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

Release gates pass: 40 Direct Mode tests, 21 preflight invariants, GenVM lint 3/3, ABI schema generation, and exactly one deployable source.

External artefact availability can affect liveness and validator semantic disagreement can prevent approval or require retry; both conditions preserve fail-closed safety. Review artefacts are bounded textual UTF-8. Each deployment has finite capacity of 128 boundaries and 1,024 changes. A custom challenge sink is a deployment-time trust/configuration choice rather than a consensus property; the canonical deployment should use an appropriately neutral sink.
