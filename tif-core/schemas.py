"""Pydantic data models for the TIF Core workflow."""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


class EvidenceRef(BaseModel):
    """A traceable reference to one retrieved evidence chunk."""

    source_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    claim: str = Field(min_length=1)


class InterventionConstraints(BaseModel):
    """Simple constraints that an intervention must respect."""

    mandatory: bool
    cost_level: str = Field(min_length=1)
    opt_out: bool


class Target(BaseModel):
    """An actionable problem discovered from domain evidence."""

    target_id: str = Field(min_length=1)
    target_statement: str = Field(min_length=1)
    target_type: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    expected_outcomes: list[Annotated[str, Field(min_length=1)]] = Field(
        min_length=1
    )
    priority_reason: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    uncertainties: list[Annotated[str, Field(min_length=1)]] = Field(
        default_factory=list
    )


class Intervention(BaseModel):
    """A candidate action linked to a target and supporting evidence."""

    intervention_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    message: str = Field(min_length=1)
    delivery_channel: str = Field(min_length=1)
    trigger_condition: str = Field(min_length=1)
    implementation_steps: list[Annotated[str, Field(min_length=1)]] = Field(
        min_length=1
    )
    evidence: list[EvidenceRef] = Field(min_length=1)
    expected_outcomes: list[Annotated[str, Field(min_length=1)]] = Field(
        min_length=1
    )
    constraints: InterventionConstraints
    risks: list[Annotated[str, Field(min_length=1)]] = Field(min_length=1)
    verification_questions: list[
        Annotated[str, Field(min_length=1)]
    ] = Field(min_length=1)


class HumanFeedback(BaseModel):
    """Structured review of a target and one intervention candidate."""

    target_id: str = Field(min_length=1)
    target_decision: Literal["accept", "revise", "reject"]
    target_relevance: int = Field(ge=1, le=5)
    target_priority: int = Field(ge=1, le=5)
    target_evidence_support: int = Field(ge=1, le=5)

    intervention_id: str = Field(min_length=1)
    intervention_decision: Literal["accept", "revise", "reject"]
    evidence_grounding: int = Field(ge=1, le=5)
    context_fit: int = Field(ge=1, le=5)
    actionability: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    autonomy: int = Field(ge=1, le=5)
    risk_control: int = Field(ge=1, le=5)

    field_to_modify: str | None = Field(default=None, min_length=1)
    requested_change: str | None = Field(default=None, min_length=1)
    reviewer_role: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_revision_details(self) -> "HumanFeedback":
        """Require field-level instructions when an intervention is revised."""

        if self.intervention_decision == "revise":
            if not self.field_to_modify or not self.requested_change:
                raise ValueError(
                    "Revising an intervention requires field_to_modify "
                    "and requested_change."
                )
        return self
