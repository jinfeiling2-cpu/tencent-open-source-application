# Weekly Plan

## Expected Growth

- Understand WeKnora’s basic RAG and Agent workflows.
- Learn how retrieval evidence and citations are returned and reused.
- Build an evidence-to-action workflow with structured human feedback.
- Complete one practical open-source contribution, such as an Issue, example, documentation improvement, or small Pull Request.

## Expected Technologies and Modules

- WeKnora document retrieval and citation outputs
- Structured LLM generation
- JSON schema validation
- Human-in-the-loop feedback
- REST API integration
- Possible MCP integration

---

## Week 1 — Understand WeKnora and Define the Interface

### Tasks

- Read the main documentation and contribution guidelines.
- Run the basic local RAG workflow.
- Inspect the format of retrieved evidence and citations.
- Define the input, output, and MVP boundaries of TIF Core.

### Deliverables

- Environment setup record
- Basic pipeline notes
- Initial `tif-core/README.md`
- Confirmed MVP scope

---

## Week 2 — Schemas and Target Discovery

### Tasks

- Define the Target, Intervention, and Feedback schemas.
- Prepare the first building-domain example.
- Implement `discover_targets()`.
- Convert evidence and context into one to three target cards.

### Deliverables

- `schemas.py`
- `examples/building_case.json`
- Runnable target-discovery example

---

## Week 3 — Intervention Generation and Validation

### Tasks

- Implement `generate_interventions()`.
- Generate two to three intervention candidates for each target.
- Require fields such as evidence, trigger, action steps, and risks.
- Implement basic validation for missing or invalid fields.

### Deliverables

- Structured intervention cards
- `validate_intervention()`
- Initial validation results

---

## Week 4 — Human Feedback and End-to-End Demo

### Tasks

- Add separate feedback for targets and interventions.
- Support field-level revision comments.
- Complete the full workflow in `app.py`.
- Save the final structured record as JSON.

### Deliverables

- Evidence → Target → Intervention → Feedback demo
- Human-feedback record
- Example output file

---

## Week 5 — WeKnora Integration and Community Contribution

### Tasks

- Add a mock knowledge provider.
- Prepare a WeKnora API adapter skeleton.
- Connect real retrieval results where feasible.
- Document the integration process and limitations.
- Prepare a relevant Issue or Draft Pull Request.

### Deliverables

- WeKnora integration notes
- Adapter skeleton or working connection
- Issue or Draft Pull Request link

---

## Week 6 — Refinement and Final Summary

### Tasks

- Improve documentation and error handling.
- Add basic tests.
- Add a second general-domain example where feasible.
- Organize the final repository and demonstration materials.
- Summarize future contribution directions.

### Deliverables

- Final repository
- Technical summary
- Demonstration materials
- Future contribution plan
