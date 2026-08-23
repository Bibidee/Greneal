# Greneal — Semantic Change-Control Firewall

**Category:** GenLayer Intelligent Contracts  
**Current version:** v0.2.3  
**Current contract:** [`0xf67E7f09355e4859384F1F81c26D83C9dB44a524`](https://explorer-studio.genlayer.com/address/0xf67E7f09355e4859384F1F81c26D83C9dB44a524)  
**Deployment transaction:** [`0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5`](https://explorer-studio.genlayer.com/tx/0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5)  
**Source commit:** [`402356ffb3356aab2198e6d8be1fc1e7c4120803`](https://github.com/Bibidee/Greneal/commit/402356ffb3356aab2198e6d8be1fc1e7c4120803)  
**Evidence commit:** [`9bec43a81a0326e382ef324c839d47fb3da0cfd7`](https://github.com/Bibidee/Greneal/commit/9bec43a81a0326e382ef324c839d47fb3da0cfd7)  
**Source SHA-256:** `b7cd0ac27b0b9d8be073581b6acd90b97b744c385b8bc11dbf81fe82575d498c`

## Purpose

Greneal is a reusable semantic change-control firewall. An owner establishes an immutable safety boundary for a governed resource. A maintainer commits a payload and supporting evidence, but the change cannot become actionable until cryptographic integrity checks, independent GenLayer semantic consensus, deterministic verdict rules, and the challenge delay all pass.

## Why GenLayer consensus is necessary

Whether an upgrade preserves scope, expands authority, increases economic risk, remains reversible, or preserves compatibility cannot be decided safely by hashes or keyword matching alone. Validators independently fetch hash-pinned baseline, payload, and evidence artefacts, verify SHA-256 over raw bytes, and classify those semantic dimensions. Exact agreement is required on the deciding categories; rationale is non-equivalent, and uncertainty never approves.

## Security model

Authorization, storage bounds, hashes, structured-result validation, verdict derivation, challenge timing, bond accounting, settlement, replay protection, and actionability are deterministic. A valid challenge makes the proposal non-actionable and forces a public re-review lifecycle. Stalled review has a public timeout/refund route; successful approved re-review slashes the bond to the neutral sink. Downstream integrators must verify the executable payload against the returned committed payload hash.

## Live proof

- Safe review: [`APPROVED`, confidence 93](https://explorer-studio.genlayer.com/tx/0x25dddf5250cac60e7bf50b6a738e973035f6d39ba6223ae0804ca0aafd56f00f).
- Risky review: [`BLOCKED`, confidence 100](https://explorer-studio.genlayer.com/tx/0x7ffe88f047807711c5ed790a4dbc593729983cdba14c76b5a89819f85219506b).
- Timeout/refund: [challenge](https://explorer-studio.genlayer.com/tx/0xb16619774ebc530d26ccc35d605634da18465d94e225ed8f61b8d52247e1a6e1), [public settlement](https://explorer-studio.genlayer.com/tx/0x13021aed4e52db3c8e471f7fbc093d26f650d3bafe87fc2897e0ec130427e303), and [withdrawal](https://explorer-studio.genlayer.com/tx/0x10671ccd9f37d1684af0a8ab72560631388aec7ebdcf968904bde62aa3d934c4).
- Successful re-review/slash: [`APPROVED`, confidence 100](https://explorer-studio.genlayer.com/tx/0x034e2767d0b157303dac4612840a2000692e75adf6b331173b38fe5d1c333c12), held amount zero.
- Double-settlement protection: post-slash [timeout](https://explorer-studio.genlayer.com/tx/0x0bfb67a860b17af959e70f70c64c4e1f7ae00a82fcf91a4e7ac6efa5e47a9ee1) and [withdrawal](https://explorer-studio.genlayer.com/tx/0x07bdbbc6ff4df8425fd7fe2dd666015816931dc9f090a67b989ab28f1bf32320) reverted.

## Validation and limitations

Release gates pass: 27 Direct Mode tests, 16 preflight invariants, GenVM lint 3/3, ABI schema generation, and exactly one deployable source.

External artefact availability affects liveness; validator disagreement can prevent approval; review artefacts are bounded textual UTF-8; deployment capacity is 128 boundaries and 1,024 changes; and a custom challenge sink is a deployment-time trust choice. These constraints fail closed and are documented rather than hidden.
