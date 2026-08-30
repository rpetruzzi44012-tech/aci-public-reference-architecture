from aci import AuditStatus, CycleStatus, OutputType
from examples.run_minimal_cycle import (
    build_example_results,
    state_summary,
    structured_result,
)


def test_example_runner_covers_four_representative_cycles():
    results = build_example_results()

    assert tuple(results) == (
        "committed",
        "escalated_qualified",
        "governance_blocked",
        "aborted",
    )
    assert results["committed"].status is CycleStatus.COMMITTED
    assert (
        results["committed"].output.output_type
        is OutputType.QUALIFIED_RESPONSE
    )
    assert results["escalated_qualified"].status is CycleStatus.COMMITTED
    assert (
        results["escalated_qualified"].output.output_type
        is OutputType.ESCALATION_NOTICE
    )
    assert results["governance_blocked"].status is CycleStatus.COMMITTED
    assert (
        results["governance_blocked"].output.output_type
        is OutputType.NO_OUTPUT
    )
    assert results["aborted"].status is CycleStatus.ABORTED
    assert results["aborted"].output is None


def test_example_artifacts_preserve_final_audit_and_pending_escalation():
    results = build_example_results()

    for label in (
        "committed",
        "escalated_qualified",
        "governance_blocked",
    ):
        result = results[label]
        assert result.audit_record.status is AuditStatus.COMMITTED
        assert result.output.audit_finalized
        assert result.output.audit_ref == result.audit_record.audit_id
        assert result.audit_record.state_delta is not None

    escalated = structured_result(results["escalated_qualified"])
    assert [
        event["escalation_id"]
        for event in escalated["pending_escalations"]
    ] == ["escalation-prior-001"]
    assert (
        escalated["output_object"]["pending_escalation_ids"]
        == ["escalation-prior-001"]
    )

    aborted = structured_result(results["aborted"])
    assert aborted["audit_record"]["status"] == "audit.aborted"
    assert aborted["state_delta"] is None
    assert aborted["output_object"] is None


def test_example_state_summary_keeps_five_graph_domains_visible():
    summary = state_summary(build_example_results()["committed"])

    assert set(summary["graph_counts"]) == {
        "memory",
        "evidence",
        "coherence",
        "scale",
        "authority",
    }
    assert summary["audit_statuses"] == ["audit.committed"]
