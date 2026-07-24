"""Framework-facing Evidence-to-Action Skill wrapper for TIF Core."""

import json
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, ValidationError

from core import (
    discover_targets,
    generate_interventions,
    validate_intervention,
)
from schemas import EvidenceRef, Intervention, Target


SKILL_NAME = "evidence_to_action"
SKILL_VERSION = "0.1.0"
SKILL_DESCRIPTION = (
    "Transform retrieved domain evidence and contextual constraints "
    "into actionable targets, intervention candidates, validation "
    "results, traceability information, and a human-review package."
)


class SkillInput(BaseModel):
    """Generic input contract for the Evidence-to-Action Skill."""

    case_id: str | None = Field(default=None, min_length=1)
    task: str = Field(min_length=1)
    context: dict[str, Any]
    constraints: list[Annotated[str, Field(min_length=1)]]
    evidence: list[EvidenceRef] = Field(min_length=1)


class ValidationResult(BaseModel):
    """Result returned by the existing deterministic business validator."""

    intervention_id: str = Field(min_length=1)
    passed: bool
    checks: dict[str, bool]


class ReviewPackage(BaseModel):
    """Questions and decisions that a host should present to a human."""

    human_review_required: bool
    review_dimensions: list[str]
    review_questions: list[str]
    allowed_decisions: list[Literal["accept", "revise", "reject"]]
    feedback_note: str = Field(min_length=1)


class Traceability(BaseModel):
    """Mappings from generated results back to supporting evidence."""

    used_evidence_ids: list[str]
    target_to_evidence: dict[str, list[str]]
    intervention_to_evidence: dict[str, list[str]]
    uncertainties: list[str]
    limitations: list[str]


class SkillOutput(BaseModel):
    """Stable output contract returned to a framework or host application."""

    skill_name: str
    skill_version: str
    case_id: str | None
    targets: list[Target] = Field(min_length=1)
    interventions: list[Intervention] = Field(min_length=1)
    validations: list[ValidationResult] = Field(min_length=1)
    review_package: ReviewPackage
    traceability: Traceability


def _evidence_id(evidence: EvidenceRef) -> str:
    """Create one readable source/chunk identifier."""

    return f"{evidence.source_id}:{evidence.chunk_id}"


def _unique_strings(values: list[str]) -> list[str]:
    """Remove duplicate strings while preserving their original order."""

    return list(dict.fromkeys(values))


def evidence_to_action(skill_input: SkillInput) -> SkillOutput:
    """
    Transform retrieved domain evidence and contextual constraints
    into actionable targets, intervention candidates, validation
    results, and a structured human-review package.
    """

    # model_validate also supports callers that pass compatible dictionary data.
    validated_input = SkillInput.model_validate(skill_input)

    # Existing core functions expect evidence text in simple dictionaries.
    core_evidence = [
        {
            "source_id": item.source_id,
            "chunk_id": item.chunk_id,
            "text": item.claim,
        }
        for item in validated_input.evidence
    ]

    # Keep task and constraints available to future core implementations.
    core_context = dict(validated_input.context)
    core_context["task"] = validated_input.task
    core_context["constraints"] = validated_input.constraints

    targets = discover_targets(core_context, core_evidence)
    if not targets:
        raise ValueError("The core workflow did not produce a target.")

    interventions: list[Intervention] = []
    validations: list[ValidationResult] = []

    for target in targets:
        target_interventions = generate_interventions(
            target, core_context, core_evidence
        )

        for intervention in target_interventions:
            if intervention.target_id != target.target_id:
                raise ValueError(
                    f"Intervention {intervention.intervention_id} refers to "
                    f"target {intervention.target_id}, not {target.target_id}."
                )

            raw_validation = validate_intervention(intervention)
            validation = ValidationResult.model_validate(raw_validation)

            if validation.intervention_id != intervention.intervention_id:
                raise ValueError(
                    "Validation result does not match its intervention."
                )

            interventions.append(intervention)
            validations.append(validation)

    if not interventions:
        raise ValueError("The core workflow did not produce an intervention.")

    target_ids = {target.target_id for target in targets}
    for intervention in interventions:
        if intervention.target_id not in target_ids:
            raise ValueError(
                f"Intervention {intervention.intervention_id} has no "
                "matching target."
            )

    target_to_evidence = {
        target.target_id: [
            _evidence_id(item) for item in target.evidence
        ]
        for target in targets
    }
    intervention_to_evidence = {
        intervention.intervention_id: [
            _evidence_id(item) for item in intervention.evidence
        ]
        for intervention in interventions
    }

    used_evidence_ids = _unique_strings(
        [
            evidence_id
            for evidence_ids in target_to_evidence.values()
            for evidence_id in evidence_ids
        ]
        + [
            evidence_id
            for evidence_ids in intervention_to_evidence.values()
            for evidence_id in evidence_ids
        ]
    )
    uncertainties = _unique_strings(
        [
            uncertainty
            for target in targets
            for uncertainty in target.uncertainties
        ]
    )

    review_package = ReviewPackage(
        human_review_required=True,
        review_dimensions=[
            "evidence grounding",
            "context fit",
            "actionability",
            "clarity",
            "autonomy",
            "risk control",
        ],
        review_questions=[
            "Does the evidence support the identified target?",
            "Does each intervention fit the provided context and constraints?",
            "Are the implementation steps practical and understandable?",
            "Are important risks, limitations, or missing conditions recorded?",
        ],
        allowed_decisions=["accept", "revise", "reject"],
        feedback_note=(
            "The Skill prepares candidates for review. A human reviewer or "
            "host application remains responsible for the final decision."
        ),
    )

    traceability = Traceability(
        used_evidence_ids=used_evidence_ids,
        target_to_evidence=target_to_evidence,
        intervention_to_evidence=intervention_to_evidence,
        uncertainties=uncertainties,
        limitations=[
            "Outputs are candidate actions requiring domain and human review.",
            "Validation checks structural and predefined business requirements "
            "only; it does not establish real-world effectiveness, safety, or "
            "ethical approval.",
            "The current underlying generation logic is a deterministic mock "
            "for the included example.",
        ],
    )

    return SkillOutput(
        skill_name=SKILL_NAME,
        skill_version=SKILL_VERSION,
        case_id=validated_input.case_id,
        targets=targets,
        interventions=interventions,
        validations=validations,
        review_package=review_package,
        traceability=traceability,
    )


def _load_example(example_path: Path) -> SkillInput:
    """Load and normalize the existing example for the Skill demonstration."""

    with example_path.open("r", encoding="utf-8") as example_file:
        case_data = json.load(example_file)

    original_context = case_data["context"]
    context = {
        key: value
        for key, value in original_context.items()
        if key != "constraints"
    }
    evidence = [
        EvidenceRef(
            source_id=item["source_id"],
            chunk_id=item["chunk_id"],
            claim=item["text"],
        )
        for item in case_data["evidence"]
    ]

    return SkillInput(
        case_id=case_data.get("case_id"),
        task=(
            "Identify an actionable issue and propose reviewable interventions."
        ),
        context=context,
        constraints=original_context.get("constraints", []),
        evidence=evidence,
    )


def main() -> int:
    """Run a small demonstration without affecting imports of this module."""

    example_path = (
        Path(__file__).resolve().parent
        / "examples"
        / "building_case.json"
    )

    try:
        skill_input = _load_example(example_path)
        skill_output = evidence_to_action(skill_input)
        print(json.dumps(skill_output.model_dump(), indent=2, ensure_ascii=False))
        return 0
    except FileNotFoundError as error:
        print(f"Example file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Example file contains invalid JSON: {error}")
    except ValidationError as error:
        print(f"Skill data failed Pydantic validation:\n{error}")
    except ValueError as error:
        print(f"Skill workflow error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
