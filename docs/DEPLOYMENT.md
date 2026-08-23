# Greneal v0.1.3 deployment record (legacy)

This record applies only to the v0.1.3 code at the listed address. Do not represent that legacy deployment as containing v0.2.1 protections; the separate v0.2.1 record below is the current hardened deployment.

## v0.2.1 Studionet deployment

- Contract: [`0xdD3a172D1da5E7661Cf74F5ee472B3411FB2b211`](https://explorer-studio.genlayer.com/address/0xdD3a172D1da5E7661Cf74F5ee472B3411FB2b211)
- Deployment transaction: [`0xcd33a5a10ab067de84c27216b36f110a2368b38bc15cf322ec3c50bd14a82796`](https://explorer-studio.genlayer.com/tx/0xcd33a5a10ab067de84c27216b36f110a2368b38bc15cf322ec3c50bd14a82796)
- Source commit: [`0a5aad7`](https://github.com/Bibidee/Greneal/commit/0a5aad78a1be289266e80178d905ab3ddafd194c)
- Local SHA-256: `5ba891d42c07f75dc87a6c307570dfcff1189ff273df04c670f74038ae887b03`
- Retrieved deployed-source SHA-256: `5ba891d42c07f75dc87a6c307570dfcff1189ff273df04c670f74038ae887b03`
- Parity: exact byte-for-byte match after finalized deployment.

This deployment resolves the legacy-source gap. External web availability remains intentionally fail-closed and retryable: the contract cannot safely make a remote artifact permanently available, but it verifies its exact SHA-256 before every semantic review and never fabricates an approval when retrieval fails.

- Network: Studionet
- Contract: [`0x0B33f933C664E651841270941eaF5F496c994547`](https://explorer-studio.genlayer.com/address/0x0B33f933C664E651841270941eaF5F496c994547)
- Deployment transaction: [`0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f`](https://explorer-studio.genlayer.com/tx/0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f)
- Source commit: [`bf8712f`](https://github.com/Bibidee/Greneal/commit/bf8712f6405cb5a9e2b11de03fd16b275bb29fd0)
- Retrieved-source SHA-256: `ee5d00c9cd0322b15b8e5abd53b67b1f531fbfc5df2efc642c1cf3eb03a2b4fa`
- Local-source SHA-256: `ee5d00c9cd0322b15b8e5abd53b67b1f531fbfc5df2efc642c1cf3eb03a2b4fa`
- Parity: exact byte-for-byte match

## Finalized live transactions

| Scenario | Transaction | Outcome |
| --- | --- | --- |
| Deployment | [`0x2e5ce4…3ea6f`](https://explorer-studio.genlayer.com/tx/0x2e5ce4e66969897ca86758074f1039d0a72db20d3cbe2bc1b4aaa4571043ea6f) | `SUCCESS`, majority agree |
| Boundary creation | [`0x72949b…f778`](https://explorer-studio.genlayer.com/tx/0x72949ba130e1eb1c3d31525fc06a1aa8be534c882e231a6e27cb7a8ddc3bf778) | `SUCCESS`, boundary active |
| Safe proposal | [`0xfac265…e7b3`](https://explorer-studio.genlayer.com/tx/0xfac2654f938224f506f590cc13de815b297b5a407b5d5feba244fa0c688fe7b3) | `SUCCESS`, proposal recorded |
| Semantic review | [`0x4fca58…208b`](https://explorer-studio.genlayer.com/tx/0x4fca58c84ccb8d880e961d8cc11f02957bfbc83183cfe1008f5f9fa8ff87208b) | finalized retryable execution; proposal unchanged |

## Scenario coverage

Direct Mode confirms approved and blocked verdicts, unavailable-review non-mutation, exact-bond enforcement, re-review refund, expiry refund, early and duplicate expiry-settlement rejection, pause/closure survivability, and replay/consumption guards. The live review above did not produce a verdict, so it is not represented as an approval or rejection. A held bond cannot exist in that live record, because `challenge_change` only accepts a reviewed, non-blocked proposal.
