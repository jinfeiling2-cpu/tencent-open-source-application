"""Run the deterministic TIF Core demonstration."""

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from core import (
    collect_feedback,
    discover_targets,
    generate_interventions,
    validate_intervention,
)


def print_json(title: str, data: Any) -> None:
    """Print a workflow section as readable JSON."""

    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main() -> int:
    """Load the example, run the workflow, and save one complete record."""

    project_directory = Path(__file__).resolve().parent
    case_path = project_directory / "examples" / "building_case.json"
    output_path = project_directory / "demo_result.json"

    try:
        with case_path.open("r", encoding="utf-8") as case_file:
            case_data = json.load(case_file)

        case_id = case_data["case_id"]
        context = case_data["context"]
        evidence = case_data["evidence"]

        print(f"Running TIF Core case: {case_id}")
        print_json("Input Context", context)
        print_json("Input Evidence", evidence)

        targets = discover_targets(context, evidence)
        print_json(
            "Discovered Targets",
            [target.model_dump() for target in targets],
        )

        interventions = []
        validations = []

        for target in targets:
            target_interventions = generate_interventions(
                target, context, evidence
            )

            for intervention in target_interventions:
                interventions.append(intervention)
                print_json(
                    f"Intervention {intervention.intervention_id}",
                    intervention.model_dump(),
                )

                validation = validate_intervention(intervention)
                validations.append(validation)
                print_json(
                    f"Validation {intervention.intervention_id}",
                    validation,
                )

        # One example review is enough to demonstrate structured feedback.
        feedback = collect_feedback(targets[0], interventions[0])
        print_json("Human Feedback", feedback.model_dump())

        complete_record = {
            "case_id": case_id,
            "context": context,
            "evidence": evidence,
            "targets": [target.model_dump() for target in targets],
            "interventions": [
                intervention.model_dump() for intervention in interventions
            ],
            "validations": validations,
            "feedback": feedback.model_dump(),
        }

        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(
                complete_record,
                output_file,
                indent=2,
                ensure_ascii=False,
            )

        print(f"\nComplete record saved to: {output_path}")
        return 0

    except FileNotFoundError as error:
        print(f"Case file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Case file contains invalid JSON: {error}")
    except ValidationError as error:
        print(f"Generated data failed Pydantic validation:\n{error}")
    except Exception as error:
        print(f"Unexpected error: {error}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
