# Greneal deployment record

## v0.3.1 Studionet deployment (CURRENT)

- Contract: [`0x5807f5876771e887A3c3576a87Ca460f3F097b9c`](https://explorer-studio.genlayer.com/address/0x5807f5876771e887A3c3576a87Ca460f3F097b9c)
- Deployment: [`0x49493e40a0d08d68e25f7aed9b8e3f6256574772531dcd740d8ed7e8d3baa1aa`](https://explorer-studio.genlayer.com/tx/0x49493e40a0d08d68e25f7aed9b8e3f6256574772531dcd740d8ed7e8d3baa1aa)
- Source commit: `87db74d`
- Local/deployed SHA-256: `ca6a763bdc2f2bc331150d232f531d501053823b5d96d033f591423d1b33254a`
- Parity: exact byte-for-byte match

## v0.3.0 Studionet deployment (LEGACY / SUPERSEDED)

- Contract: [`0xFa8bfa84889c347201A6D37026A45d65429827cE`](https://explorer-studio.genlayer.com/address/0xFa8bfa84889c347201A6D37026A45d65429827cE)
- Deployment: [`0x046de466f0ba0402c6c5c4758dcb07643f26f9e48387bb3eb330cf2467bf0573`](https://explorer-studio.genlayer.com/tx/0x046de466f0ba0402c6c5c4758dcb07643f26f9e48387bb3eb330cf2467bf0573)
- Source commit: `09ef7cc`
- Local/deployed SHA-256: `6f6540edbd80341c0abd694c5512a2b2e4990d9ed50165798e29fc5990e467c2`
- Parity: exact byte-for-byte match

## v0.2.3 Studionet deployment (LEGACY / SUPERSEDED)

- Contract: [`0xf67E7f09355e4859384F1F81c26D83C9dB44a524`](https://explorer-studio.genlayer.com/address/0xf67E7f09355e4859384F1F81c26D83C9dB44a524)
- Deployment transaction: [`0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5`](https://explorer-studio.genlayer.com/tx/0x47f5b45443d86fa15ac0a4e6bfbc0cda99f5ca9df15e5be9c40bb85db6b61ee5)
- Source commit: [`402356f`](https://github.com/Bibidee/Greneal/commit/402356f)
- Local SHA-256: `b7cd0ac27b0b9d8be073581b6acd90b97b744c385b8bc11dbf81fe82575d498c`
- Retrieved deployed-source SHA-256: `b7cd0ac27b0b9d8be073581b6acd90b97b744c385b8bc11dbf81fe82575d498c`
- Parity: exact byte-for-byte match, 23,885 characters

The complete finalized transaction ledger, including approved, blocked, timeout-refund, successful re-review/slash, and expected duplicate-settlement rejection paths, is maintained in the README. All earlier deployments below are legacy.

## v0.1.3 deployment record (LEGACY / SUPERSEDED)

This record applies only to the v0.1.3 code at the listed address. Do not represent that legacy deployment as containing later protections.

## v0.2.1 Studionet deployment (LEGACY / SUPERSEDED)

- Contract: [`0xdD3a172D1da5E7661Cf74F5ee472B3411FB2b211`](https://explorer-studio.genlayer.com/address/0xdD3a172D1da5E7661Cf74F5ee472B3411FB2b211)
- Deployment transaction: [`0xcd33a5a10ab067de84c27216b36f110a2368b38bc15cf322ec3c50bd14a82796`](https://explorer-studio.genlayer.com/tx/0xcd33a5a10ab067de84c27216b36f110a2368b38bc15cf322ec3c50bd14a82796)
- Source commit: [`0a5aad7`](https://github.com/Bibidee/Greneal/commit/0a5aad78a1be289266e80178d905ab3ddafd194c)
- Local SHA-256: `5ba891d42c07f75dc87a6c307570dfcff1189ff273df04c670f74038ae887b03`
- Retrieved deployed-source SHA-256: `5ba891d42c07f75dc87a6c307570dfcff1189ff273df04c670f74038ae887b03`
- Parity: exact byte-for-byte match after finalized deployment.

This deployment resolves the legacy-source gap. External web availability remains intentionally fail-closed and retryable: the contract cannot safely make a remote artifact permanently available, but it verifies its exact SHA-256 before every semantic review and never fabricates an approval when retrieval fails.

The v0.2.1 deployment is superseded by v0.2.2 because its `is_actionable()` view used `challenge_count` while `consume_change()` did not.

## v0.2.2 Studionet deployment (LEGACY / SUPERSEDED)

- Contract: [`0x39a2128a55aa74753eBF0EC6f3392475E59D25B5`](https://explorer-studio.genlayer.com/address/0x39a2128a55aa74753eBF0EC6f3392475E59D25B5)
- Deployment transaction: [`0xcd3e918e19259144f776bf3cc39b8b061792f093675e230f8f536dd6afa2ea2b`](https://explorer-studio.genlayer.com/tx/0xcd3e918e19259144f776bf3cc39b8b061792f093675e230f8f536dd6afa2ea2b)
- Source commit: [`57648f7`](https://github.com/Bibidee/Greneal/commit/57648f7fc8661d7cf61a22a38f2f1317b1405693)
- Local SHA-256: `b6b15416cec71fcf6b35ca957d910efa2e531be1f5251bb575284098ca2c3a63`
- Retrieved deployed-source SHA-256: `b6b15416cec71fcf6b35ca957d910efa2e531be1f5251bb575284098ca2c3a63`
- Parity: exact byte-for-byte match after finalized deployment.

### Earlier Studionet deployment (LEGACY / SUPERSEDED)

- Network: Studionet
- Contract: [`0x0B33f933C664E651841270941eaF5F496c994547`](https://explorer-studio.genlayer.com/address/0x0B33f933C664E651841270941eaF5F496c994547)
- Deployment transaction: [`0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f`](https://explorer-studio.genlayer.com/tx/0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f)
- Source commit: [`bf8712f`](https://github.com/Bibidee/Greneal/commit/bf8712f6405cb5a9e2b11de03fd16b275bb29fd0)
- Retrieved-source SHA-256: `ee5d00c9cd0322b15b8e5abd53b67b1f531fbfc5df2efc642c1cf3eb03a2b4fa`
- Local-source SHA-256: `ee5d00c9cd0322b15b8e5abd53b67b1f531fbfc5df2efc642c1cf3eb03a2b4fa`
- Parity: exact byte-for-byte match

## Historical finalized live transactions (LEGACY / SUPERSEDED)

| Scenario | Transaction | Outcome |
| --- | --- | --- |
| Deployment | [`0x2e5ce4…3ea6f`](https://explorer-studio.genlayer.com/tx/0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f) | `SUCCESS`, majority agree |
| Boundary creation | [`0x72949b…f778`](https://explorer-studio.genlayer.com/tx/0x72949ba130e1eb1c3d31525fc06a1aa8be534c882e231a6e27cb7a8ddc3bf778) | `SUCCESS`, boundary active |
| Safe proposal | [`0xfac265…e7b3`](https://explorer-studio.genlayer.com/tx/0xfac2654f938224f506f590cc13de815b297b5a407b5d5feba244fa0c688fe7b3) | `SUCCESS`, proposal recorded |
| Semantic review | [`0x4fca58…208b`](https://explorer-studio.genlayer.com/tx/0x4fca58c84ccb8d880e961d8cc11f02957bfbc83183cfe1008f5f9fa8ff87208b) | finalized retryable execution; proposal unchanged |

## Scenario coverage

Direct Mode confirms approved and blocked verdicts, unavailable-review non-mutation, exact-bond enforcement, re-review refund, expiry refund, early and duplicate expiry-settlement rejection, pause/closure survivability, and replay/consumption guards. The live review above did not produce a verdict, so it is not represented as an approval or rejection. A held bond cannot exist in that live record, because `challenge_change` only accepts a reviewed, non-blocked proposal.
