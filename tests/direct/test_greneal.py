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
    assert row["challenge_settlement"] == "slashed" and row["challenge_bond_held"] == "0" and row["challenge_count"] == 1
    with direct_vm.expect_revert("refund unavailable"):
        contract.withdraw_challenge_bond("change-1")
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")
    warp_to(direct_vm, "2026-08-23T08:02:02Z")
    contract.consume_change("change-1")
    assert not contract.is_actionable("change-1")["actionable"]
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")


def test_view_and_consume_share_post_challenge_eligibility(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    direct_vm.value = BOND; contract.challenge_change("change-1"); direct_vm.value = 0
    warp_to(direct_vm, "2026-08-23T08:01:01Z"); mock_review(direct_vm); contract.review_change("change-1")
    assert contract.get_change("change-1")["challenge_count"] == 1
    assert not contract.is_actionable("change-1")["actionable"]
    with direct_vm.expect_revert("not actionable"):
        contract.consume_change("change-1")
    warp_to(direct_vm, "2026-08-23T08:02:02Z")
    assert contract.is_actionable("change-1")["actionable"]
    contract.consume_change("change-1")
    assert contract.get_change("change-1")["status"] == "consumed"


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


def test_challenge_remains_available_during_global_pause(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    contract.set_paused(True)
    assert not contract.is_actionable("change-1")["actionable"]
    direct_vm.value = BOND
    with direct_vm.prank(direct_alice): contract.challenge_change("change-1")
    direct_vm.value = 0
    state = contract.get_change("change-1")
    assert state["status"] == "challenged" and state["verdict"] == ""
    assert state["challenge_count"] == 1 and int(state["challenge_bond_held"]) == BOND
    assert not contract.is_actionable("change-1")["actionable"]


def test_pause_does_not_extend_expired_challenge_window(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    contract.set_paused(True); warp_to(direct_vm, "2026-08-23T08:01:01Z"); direct_vm.value = BOND
    with direct_vm.expect_revert("Challenge window closed"): contract.challenge_change("change-1")
    direct_vm.value = 0


def test_paused_challenge_rereview_preserves_fresh_delay(direct_vm, direct_deploy, direct_alice):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract); mock_review(direct_vm); contract.review_change("change-1")
    contract.set_paused(True); direct_vm.value = BOND
    with direct_vm.prank(direct_alice): contract.challenge_change("change-1")
    direct_vm.value = 0; warp_to(direct_vm, "2026-08-23T08:01:01Z"); mock_review(direct_vm); contract.review_change("change-1")
    state = contract.get_change("change-1")
    assert state["verdict"] == "approved" and int(state["challenge_bond_held"]) == 0
    assert not contract.is_actionable("change-1")["actionable"]
    contract.set_paused(False)
    assert not contract.is_actionable("change-1")["actionable"]
    warp_to(direct_vm, "2026-08-23T08:02:02Z")
    assert contract.is_actionable("change-1")["actionable"]


def test_raw_hashing_preserves_non_utf8_integrity_input(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy)
    module = direct_vm._greneal_module
    assert module.content_hash(b"\xff\x00") != module.content_hash(b"\x00")


def test_fetch_verified_production_helper_accepts_exact_bytes_and_rejects_mismatch(direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    value, target = b"verified utf-8 evidence\n", "https://evidence.example/fixture"
    expected = module.content_hash(value)
    direct_vm.mock_web(target, {"status": 200, "body": value})
    assert module.fetch_verified(target, expected) == value.decode("utf-8")
    direct_vm.clear_mocks(); direct_vm.mock_web(target, {"status": 200, "body": value})
    with pytest.raises(ValueError): module.fetch_verified(target, "0x" + "00" * 32)


def test_artifact_exact_maximum_is_accepted(direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    raw, target = b"a" * module.MAX_ARTIFACT_BYTES, "https://evidence.example/max"
    direct_vm.mock_web(target, {"status": 200, "body": raw})
    assert module.fetch_verified(target, module.content_hash(raw)) == raw.decode("utf-8")


@pytest.mark.parametrize("label", ["baseline", "payload", "evidence"])
def test_each_oversized_artifact_is_rejected(label, direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    raw, target = b"a" * (module.MAX_ARTIFACT_BYTES + 1), f"https://evidence.example/{label}"
    direct_vm.mock_web(target, {"status": 200, "body": raw})
    with pytest.raises(ValueError, match="artifact_too_large"):
        module.fetch_verified(target, module.content_hash(raw))


def test_empty_and_invalid_utf8_are_classified(direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    empty, invalid = "https://evidence.example/empty", "https://evidence.example/invalid"
    direct_vm.mock_web(empty, {"status": 200, "body": b""})
    with pytest.raises(ValueError, match="empty_response"):
        module.fetch_verified(empty, module.content_hash(b""))
    direct_vm.clear_mocks(); raw = b"\xff\xfe"
    direct_vm.mock_web(invalid, {"status": 200, "body": raw})
    with pytest.raises(ValueError, match="invalid_utf8"):
        module.fetch_verified(invalid, module.content_hash(raw))


def test_complete_accepted_artifacts_reach_semantic_prompt_without_truncation(direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    urls = ["https://evidence.example/base", "https://evidence.example/payload", "https://evidence.example/evidence"]
    bodies = [b"baseline", b"s" * 11900 + b"MALICIOUS_TAIL", b"evidence"]
    for target, raw in zip(urls, bodies): direct_vm.mock_web(target, {"status": 200, "body": raw})
    captured = {}
    def prompt(value, response_format=None):
        captured["value"] = value
        return {"scope_preserved": "no", "access_expansion": "yes", "economic_risk": "yes", "reversibility": "no", "compatibility": "no", "confidence": 100, "rationale": "Tail changes the security result."}
    module.gl.nondet.exec_prompt = prompt
    result = module.observe("policy", urls[0], module.content_hash(bodies[0]), urls[1], module.content_hash(bodies[1]), urls[2], module.content_hash(bodies[2]), "summary")
    assert result["kind"] == "analysis"
    assert "MALICIOUS_TAIL" in captured["value"]
    assert bodies[1].decode("utf-8") in captured["value"]


def test_semantic_categories_are_canonicalized_before_verdict_and_storage(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    mock_review(direct_vm, scope=" YES ", access="No", economic="NO", reversible="Yes", compatible=" YES ")
    contract.review_change("change-1")
    state = contract.get_change("change-1")
    assert state["verdict"] == "approved"
    assert (state["scope_preserved"], state["access_expansion"], state["compatibility"]) == ("yes", "no", "yes")


def test_equivalence_ignores_rationale_but_rejects_each_category_disagreement(direct_vm, direct_deploy):
    deploy(direct_vm, direct_deploy); module = direct_vm._greneal_module
    base = {"scope_preserved": "yes", "access_expansion": "no", "economic_risk": "no", "reversibility": "yes", "compatibility": "yes", "confidence": 90, "rationale": "first"}
    other = dict(base); other["rationale"] = "different"
    assert module.equivalent(base, other)
    opposites = {"scope_preserved": "no", "access_expansion": "yes", "economic_risk": "yes", "reversibility": "no", "compatibility": "no"}
    for key, value in opposites.items():
        changed = dict(base); changed[key] = value
        assert not module.equivalent(base, changed)


@pytest.mark.parametrize("failure", ["hash_mismatch", "artifact_too_large", "invalid_utf8", "empty_response"])
def test_integrity_observation_errors_are_deterministic_and_non_mutating(failure, direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    direct_vm._greneal_module.observe = lambda *args: {"kind": "observation_error", "class": failure}
    with direct_vm.expect_revert("Artifact integrity failure"):
        contract.review_change("change-1")
    assert contract.get_change("change-1")["status"] == "proposed"


def test_malformed_semantic_output_is_distinct_and_non_mutating(direct_vm, direct_deploy):
    contract = deploy(direct_vm, direct_deploy); create(contract); propose(direct_vm, contract)
    direct_vm._greneal_module.observe = lambda *args: {"kind": "observation_error", "class": "malformed_model_output"}
    with direct_vm.expect_revert("Malformed semantic output"):
        contract.review_change("change-1")
    assert contract.get_change("change-1")["status"] == "proposed"
