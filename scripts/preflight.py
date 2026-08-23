"""Release gate: test and lint the sole deployable Greneal contract."""

import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = list((ROOT / "contracts").glob("*.py"))
if len(CONTRACTS) != 1 or CONTRACTS[0].name != "greneal.py":
    raise SystemExit("Expected exactly one deployable source: contracts/greneal.py")

source = CONTRACTS[0].read_text(encoding="utf-8")
ast.parse(source)
required = [
    "class Greneal", "run_nondet_unsafe", "equivalent", "valid_analysis",
    "settle_expired_challenge", "challenge_bond_held", "challenged_at",
    "is_actionable", "payload_binding", "MIN_CONFIDENCE = 75", "def address(value)",
]
missing = [item for item in required if item not in source]
if missing:
    raise SystemExit(f"Missing Greneal safety invariants: {missing}")

artifacts = ROOT / "artifacts"
artifacts.mkdir(exist_ok=True)
linter = str(Path(sys.executable).with_name("genvm-lint.exe"))
checks = [
    [sys.executable, "-m", "pytest", "tests/direct", "-q"],
    [linter, "check", str(CONTRACTS[0]), "--json"],
    [linter, "schema", str(CONTRACTS[0]), "--output", str(artifacts / "greneal.abi.json")],
]
for command in checks:
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
print(f"Greneal preflight passed: {len(required)} invariants, Direct Mode, lint, and schema")
