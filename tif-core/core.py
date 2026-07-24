"""Deterministic core workflow functions for TIF Core.

These functions use simple mock logic so the prototype runs without an LLM.
Their inputs and outputs can remain the same when mock logic is replaced later.
"""

from typing import Any

from schemas import EvidenceRef, HumanFeedback, Intervention, Target


def _evidence_reference(
    evidence: list[dict[str, str]], source_id: str, chunk_id: str
) -> EvidenceRef:
    """Find one input evidence item and convert it to a traceable reference."""

    for item in evidence:
        if item["source_id"] == source_id and item["chunk_id"] == chunk_id:
            return EvidenceRef(
                source_id=item["source_id"],
                chunk_id=item["chunk_id"],
                claim=item["text"],
            )

    raise ValueError(f"Evidence {source_id}:{chunk_id} was not found.")


def discover_targets(
    context: dict[str, Any], evidence: list[dict[str, str]]
) -> list[Target]:
    """Create one deterministic actionable target from the example evidence."""

    source = _evidence_reference(evidence, "doc_01", "chunk_01")

    target = Target(
        target_id="T001",
        target_statement=(
            "Reduce unnecessary simultaneous window opening and mechanical cooling."
        ),
        target_type="behavioral_operational_conflict",
        evidence=[source],
        expected_outcomes=[
            "Reduced avoidable cooling energy use",
            "Maintained occupant comfort",
        ],
        priority_reason=(
            "The issue has a clear operational consequence and can be addressed "
            "with a lightweight, non-mandatory intervention."
        ),
        # This is a fixed mock value, not a statistical probability.
        confidence=0.82,
        uncertainties=[
            "Outdoor temperature and air-quality conditions are not fully known."
        ],
    )

    return [target]


def generate_interventions(
    target: Target,
    context: dict[str, Any],
    evidence: list[dict[str, str]],
) -> list[Intervention]:
    """Create two deterministic intervention candidates for one target."""

    energy_evidence = _evidence_reference(evidence, "doc_01", "chunk_01")
    feedback_evidence = _evidence_reference(evidence, "doc_02", "chunk_02")
    autonomy_evidence = _evidence_reference(evidence, "doc_03", "chunk_03")
    ventilation_evidence = _evidence_reference(evidence, "doc_04", "chunk_04")

    reminder = Intervention(
        intervention_id="I001",
        target_id=target.target_id,
        title="Context-aware window-HVAC reminder",
        mechanism="decision_information",
        message=(
            "Cooling is active while this window is open. Consider closing the "
            "window when outdoor conditions do not require ventilation."
        ),
        delivery_channel="digital_display",
        trigger_condition=(
            "A window is open while HVAC cooling is active; outdoor temperature "
            "and air-quality conditions must also be considered before deployment."
        ),
        implementation_steps=[
            "Detect simultaneous window opening and mechanical cooling.",
            "Check whether outdoor conditions make window ventilation necessary.",
            "Display a short and transparent reminder.",
            "Allow occupants to ignore or dismiss the reminder.",
        ],
        evidence=[
            energy_evidence,
            feedback_evidence,
            autonomy_evidence,
            ventilation_evidence,
        ],
        expected_outcomes=target.expected_outcomes,
        constraints={
            "mandatory": False,
            "cost_level": "low",
            "opt_out": True,
        },
        risks=[
            "The reminder may be inappropriate when outdoor ventilation is needed.",
            "Repeated reminders may cause notification fatigue.",
        ],
        verification_questions=[
            "Does the reminder explain why it appears?",
            "Can occupants easily ignore or dismiss it?",
            "Does the trigger account for relevant outdoor conditions?",
        ],
    )

    consequence_feedback = Intervention(
        intervention_id="I002",
        target_id=target.target_id,
        title="Energy consequence feedback",
        mechanism="feedback",
        message=(
            "An open window during mechanical cooling may increase avoidable "
            "cooling demand. Review outdoor conditions before choosing an action."
        ),
        delivery_channel="dashboard_or_mobile_notification",
        trigger_condition=(
            "A window and mechanical cooling remain active at the same time for "
            "a defined monitoring period."
        ),
        implementation_steps=[
            "Detect the window-HVAC conflict.",
            "Estimate and describe the likely operational consequence without "
            "claiming an exact energy saving.",
            "Send the feedback through the dashboard or mobile notification.",
            "Let occupants dismiss the message without penalty.",
        ],
        evidence=[
            energy_evidence,
            feedback_evidence,
            autonomy_evidence,
            ventilation_evidence,
        ],
        expected_outcomes=target.expected_outcomes,
        constraints={
            "mandatory": False,
            "cost_level": "low",
            "opt_out": True,
        },
        risks=[
            "A general consequence message may overstate impact in some conditions.",
            "Notifications may be ignored if they are too frequent.",
        ],
        verification_questions=[
            "Is the consequence stated without unsupported numerical claims?",
            "Is the message understandable and non-mandatory?",
            "Can the user opt out of future notifications?",
        ],
    )

    return [reminder, consequence_feedback]


def validate_intervention(intervention: Intervention) -> dict[str, object]:
    """Apply simple business checks beyond Pydantic schema validation."""

    checks = {
        "has_target_id": bool(intervention.target_id),
        "has_evidence": bool(intervention.evidence),
        "has_trigger_condition": bool(intervention.trigger_condition),
        "has_implementation_steps": bool(intervention.implementation_steps),
        "has_risks": bool(intervention.risks),
        "has_verification_questions": bool(intervention.verification_questions),
        "is_non_mandatory": intervention.constraints.mandatory is False,
        "allows_opt_out": intervention.constraints.opt_out is True,
    }

    return {
        "intervention_id": intervention.intervention_id,
        "passed": all(checks.values()),
        "checks": checks,
    }


def collect_feedback(
    target: Target, intervention: Intervention
) -> HumanFeedback:
    """Create one deterministic example review for the first candidate."""

    # The MVP reviews only I001 to keep the human-feedback example concise.
    return HumanFeedback(
        target_id=target.target_id,
        target_decision="accept",
        target_relevance=5,
        target_priority=4,
        target_evidence_support=4,
        intervention_id=intervention.intervention_id,
        intervention_decision="revise",
        evidence_grounding=4,
        context_fit=3,
        actionability=5,
        clarity=4,
        autonomy=5,
        risk_control=3,
        field_to_modify="trigger_condition",
        requested_change=(
            "Explicitly include outdoor temperature and air-quality conditions."
        ),
        reviewer_role="facility_manager",
    )
