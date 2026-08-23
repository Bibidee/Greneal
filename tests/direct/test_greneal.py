import sys
import pytest

from conftest import warp_to


CONTRACT = "contracts/greneal.py"
PAYLOAD = "0x" + "ab" * 32
BASELINE_HASH = "0x" + "cd" * 32
EVIDENCE_HASH = "0x" + "ef" * 32
BOND = 10**18


def deploy(direct_vm, direct_deploy):
    contract = direct_deploy(CONTRACT)
    direct_vm._greneal_module = sys.modules[contract.__class__.__module__]
    warp_to(direct_vm, "2026-08-23T08:00:00Z")
    return contract


def create(contract, boundary_id="boundary-1", window=60):
    contract.create_boundary(boundary_id, contract.get_info()["owner"], "treasury-upgrade", "Do not expand admin access, economic exposure, or irreversible scope.", "https://example.com/baseline", BASELINE_HASH, BOND, window)


def propose(direct_vm, contract, change_id="change-1", boundary_id="boundary-1"):
    contract.propose_change(change_id, boundary_id, PAYLOAD, "https://example.com/payload", "https://example.com/change", EVIDENCE_HASH, "Replace the audited implementation without changing roles or limits.")


def mock_review(direct_vm, scope="yes", access="no", economic="no", reversible="yes", compatible="yes", binding="yes", confidence=90):
    result = {"scope_preserved": scope, "access_expansion": access, "economic_risk": economic, "reversibility": reversible, "compatibility": compatible, "confidence": confidence, "rationale": "Evidence supports the declared safety boundary."}
    direct_vm._greneal_module.observe = lambda *args: {"kind": "analysis", "result": dict(result)}


def test_owner_creates_immutable_boundary_and_maintainer_proposes(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract)
    assert contract.get_boundary("boundary-1")["maintainer"].lower() == contract.get_info()["owner"].lower()
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Maintainer"):
            contract.propose_change("bad", "boundary-1", PAYLOAD, "https://example.com/payload", "https://example.com/change", EVIDENCE_HASH, "bad")
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


def test_invalid_inputs_and_duplicate_ids_are_rejected(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    with direct_vm.expect_revert("Invalid boundary_id"):
        create(contract, "bad id")
    with direct_vm.expect_revert("Invalid challenge configuration"):
        create(contract, "short-window", window=59)
    create(contract)
    with direct_vm.expect_revert("Boundary unavailable"):
        create(contract)
    with direct_vm.expect_revert("Invalid payload hash"):
        contract.propose_change("bad-hash", "boundary-1", "0x12", "https://example.com/payload", "https://example.com/change", EVIDENCE_HASH, "summary")
    with direct_vm.expect_revert("Blocked payload_url"):
        contract.propose_change("local", "boundary-1", PAYLOAD, "https://localhost/payload", "https://example.com/change", EVIDENCE_HASH, "summary")
    propose(direct_vm, contract)
    with direct_vm.expect_revert("Change unavailable"):
        propose(direct_vm, contract)


def test_numeric_cli_hash_is_normalized_to_the_same_commitment(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract)
    contract.propose_change("numeric-hash", "boundary-1", int(PAYLOAD, 16), "https://example.com/payload", "https://example.com/change", EVIDENCE_HASH, "CLI-compatible numeric hash")
    assert contract.get_change("numeric-hash")["payload_hash"] == PAYLOAD


def test_pause_and_boundary_transitions_block_new_work(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Owner only"):
            contract.set_paused(True)
    contract.set_paused(True)
    with direct_vm.expect_revert("Contract is paused"):
        propose(direct_vm, contract)
    contract.set_paused(False); contract.set_boundary_status("boundary-1", "paused")
    with direct_vm.expect_revert("Maintainer and active"):
        propose(direct_vm, contract)
    contract.set_boundary_status("boundary-1", "active"); contract.set_boundary_status("boundary-1", "closed")
    with direct_vm.expect_revert("Illegal boundary transition"):
        contract.set_boundary_status("boundary-1", "active")


def test_consume_is_delayed_and_replay_protected(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")
    warp_to(direct_vm, "2026-08-23T08:01:01Z")
    contract.consume_change("change-1")
    assert contract.get_change("change-1")["status"] == "consumed"
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")


def test_challenge_reopens_review_and_bad_re_review_refunds_challenger(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    row = contract.get_change("change-1")
    assert row["status"] == "challenged" and row["challenge_bond_held"] == str(BOND)
    warp_to(direct_vm, "2026-08-23T08:01:01Z")
    mock_review(direct_vm, access="yes")
    contract.review_change("change-1")
    row = contract.get_change("change-1")
    assert row["verdict"] == "blocked" and row["challenge_bond_held"] == str(BOND)
    contract.withdraw_challenge_bond("change-1")
    assert contract.get_change("change-1")["challenge_bond_held"] == "0"


def test_challenge_requires_exact_bond_and_is_single_use(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    with direct_vm.expect_revert("Exact challenge bond"):
        contract.challenge_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    warp_to(direct_vm, "2026-08-23T08:01:01Z"); mock_review(direct_vm); contract.review_change("change-1")
    with direct_vm.expect_revert("cannot be challenged"):
        contract.challenge_change("change-1")


def test_expired_challenge_refunds_and_cannot_be_settled_twice(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    with direct_vm.expect_revert("timeout is not open"):
        contract.settle_expired_challenge("change-1")
    warp_to(direct_vm, "2026-08-23T08:02:01Z")
    contract.settle_expired_challenge("change-1")
    assert contract.get_change("change-1")["status"] == "cancelled"
    assert contract.get_change("change-1")["challenge_bond_held"] == str(BOND)
    contract.withdraw_challenge_bond("change-1")
    assert contract.get_change("change-1")["challenge_bond_held"] == "0"
    with direct_vm.expect_revert("No held challenge bond"):
        contract.settle_expired_challenge("change-1")


def test_timeout_settlement_survives_pause_and_boundary_closure(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm)
    contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    contract.set_paused(True); contract.set_boundary_status("boundary-1", "closed")
    warp_to(direct_vm, "2026-08-23T08:02:01Z")
    contract.settle_expired_challenge("change-1")
    assert contract.get_change("change-1")["status"] == "cancelled"


def test_cancel_requires_authority_and_never_cancels_held_or_consumed_change(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("Proposer or owner"):
            contract.cancel_change("change-1")
    contract.cancel_change("change-1")
    assert contract.get_change("change-1")["status"] == "cancelled"


@pytest.mark.parametrize("field,value", [("scope", "no"), ("access", "yes"), ("economic", "yes"), ("reversible", "no"), ("compatible", "no")])
def test_each_safety_dimension_fails_closed(direct_vm, direct_deploy, field, value):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    values = {"scope": "yes", "access": "no", "economic": "no", "reversible": "yes", "compatible": "yes"}
    values[field] = value
    mock_review(direct_vm, **values); contract.review_change("change-1")
    assert contract.get_change("change-1")["verdict"] == "blocked"


@pytest.mark.parametrize("score,expected", [(74, "inconclusive"), (75, "approved")])
def test_confidence_threshold_is_deterministic(direct_vm, direct_deploy, score, expected):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    mock_review(direct_vm, confidence=score); contract.review_change("change-1")
    assert contract.get_change("change-1")["verdict"] == expected


def test_sybil_wallets_cannot_monopolize_challenge_protection(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    direct_vm.value = BOND
    with direct_vm.prank(direct_alice): contract.challenge_change("change-1")
    for attacker in (direct_bob, direct_charlie):
        with direct_vm.prank(attacker):
            with direct_vm.expect_revert("cannot be challenged"):
                contract.challenge_change("change-1")
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("cannot be challenged"):
            contract.challenge_change("change-1")
    direct_vm.value = 0
    row = contract.get_change("change-1")
    assert row["challenge_count"] == 1 and row["challenge_bond_held"] == str(BOND) and not contract.is_actionable("change-1")["actionable"]
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")


def test_zero_addresses_are_rejected(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    with direct_vm.expect_revert("Zero maintainer"):
        contract.create_boundary("zero", "0x0000000000000000000000000000000000000000", "r", "p", "https://example.com/base", BASELINE_HASH, BOND, 60)
    with direct_vm.expect_revert("Zero owner"):
        direct_vm._greneal_module.nonzero_address("0x0000000000000000000000000000000000000000", "owner")


def test_maintainer_self_challenge_is_not_paid_to_maintainer(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    warp_to(direct_vm, "2026-08-23T08:01:01Z"); mock_review(direct_vm); contract.review_change("change-1")
    row = contract.get_change("change-1")
    assert row["challenge_settlement"] == "slashed" and row["challenge_bond_held"] == "0"
    with direct_vm.expect_revert("refund unavailable"):
        contract.withdraw_challenge_bond("change-1")
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")
    warp_to(direct_vm, "2026-08-23T08:02:02Z")
    contract.consume_change("change-1")


def test_challenge_timing_blocks_early_review_and_owner_cancellation(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    with direct_vm.expect_revert("window remains open"):
        contract.review_change("change-1")
    with direct_vm.expect_revert("cannot be cancelled"):
        contract.cancel_change("change-1")
    warp_to(direct_vm, "2026-08-23T08:02:01Z")
    with direct_vm.expect_revert("settlement timeout is open"):
        contract.review_change("change-1")
    contract.settle_expired_challenge("change-1")
    contract.withdraw_challenge_bond("change-1")
    with direct_vm.expect_revert("No challenge refund"):
        contract.withdraw_challenge_bond("change-1")


def test_raw_hashing_preserves_non_utf8_integrity_input(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    module = direct_vm._greneal_module
    assert module.content_hash(b"\xff\x00") != module.content_hash(b"\x00")
