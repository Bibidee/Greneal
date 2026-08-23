import sys

from conftest import warp_to


CONTRACT = "contracts/greneal.py"
PAYLOAD = "0x" + "ab" * 32
BOND = 10**18


def deploy(direct_vm, direct_deploy):
    contract = direct_deploy(CONTRACT)
    direct_vm._greneal_module = sys.modules[contract.__class__.__module__]
    warp_to(direct_vm, "2026-08-23T08:00:00Z")
    return contract


def create(contract, boundary_id="boundary-1", window=60):
    contract.create_boundary(boundary_id, contract.get_info()["owner"], "treasury-upgrade", "Do not expand admin access, economic exposure, or irreversible scope.", "https://example.com/baseline", BOND, window)


def propose(direct_vm, contract, change_id="change-1", boundary_id="boundary-1"):
    contract.propose_change(change_id, boundary_id, PAYLOAD, "https://example.com/change", "Replace the audited implementation without changing roles or limits.")


def mock_review(direct_vm, scope="yes", access="no", economic="no", reversible="yes", compatible="yes", binding="yes", confidence=90):
    result = {"scope_preserved": scope, "access_expansion": access, "economic_risk": economic, "reversibility": reversible, "compatibility": compatible, "payload_binding": binding, "confidence": confidence, "rationale": "Evidence supports the declared safety boundary."}
    direct_vm._greneal_module.observe = lambda *args: {"kind": "analysis", "result": dict(result)}


def test_owner_creates_immutable_boundary_and_maintainer_proposes(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract)
    assert contract.get_boundary("boundary-1")["maintainer"].lower() == contract.get_info()["owner"].lower()
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Maintainer"):
            contract.propose_change("bad", "boundary-1", PAYLOAD, "https://example.com/change", "bad")
    propose(direct_vm, contract)
    assert contract.get_change("change-1")["status"] == "proposed"


def test_consensus_approval_requires_all_safety_dimensions(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    assert contract.get_change("change-1")["verdict"] == "approved"
    assert contract.is_actionable("change-1")["actionable"] is False
    warp_to(direct_vm, "2026-08-23T08:01:01Z")
    assert contract.is_actionable("change-1")["actionable"] is True


def test_risky_semantic_result_fails_closed(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm, access="yes")
    contract.review_change("change-1")
    assert contract.get_change("change-1")["verdict"] == "blocked"
    assert contract.is_actionable("change-1")["actionable"] is False


def test_review_unavailable_does_not_mutate_proposal(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    direct_vm._greneal_module.observe = lambda *args: {"kind": "observation_error", "class": "transient_fetch"}
    with direct_vm.expect_revert("Review unavailable"):
        contract.review_change("change-1")
    assert contract.get_change("change-1")["status"] == "proposed"
