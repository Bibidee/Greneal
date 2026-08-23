# Greneal

Greneal is a standalone GenLayer semantic change-control firewall. It lets a system owner register an immutable safety boundary for a governed resource, then allows maintainers to propose a change only when deterministic rules and independent GenLayer consensus agree that the change stays inside that boundary.

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

`contracts/greneal.py` is the sole contract candidate. Tests, fixtures, deployment helpers, and documentation live outside `contracts/`. `scripts/preflight.py` lints that exact source path and fails if any other Python file enters the deployable directory. No GitHub Action is included.

## Status

Initial contract implementation and direct-mode tests are in progress. A Studionet deployment link will be added only after lint, tests, and deployed-source parity all pass.

