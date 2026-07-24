# TIF Core

TIF Core is a small Python prototype that turns retrieved domain evidence into
actionable targets, candidate interventions, and structured human feedback.

It demonstrates a **Knowledge-to-Action** workflow:

```text
Evidence
→ Target Discovery
→ Intervention Generation
→ Validation
→ Human Feedback
→ Reusable JSON Record
```

The first example concerns building operation, but the data models and workflow
are intended to be domain-independent.

The current implementation focuses on the protocol rather than the discovery
algorithm.

## MVP Features

This deterministic first version:

- loads context and evidence from one JSON case;
- creates one structured target;
- creates two intervention candidates;
- validates each intervention with simple business rules;
- creates one field-level human feedback record;
- saves the complete workflow to `demo_result.json`.

The same input always produces the same output. No API key or network access is
required.

## What This Prototype Does Not Do

TIF Core is not a complete RAG system, an autonomous decision-maker, or an
ethical approval system. It does not parse documents, search vectors, rerank
results, train models, or modify WeKnora.

Its outputs are candidate interventions. A human reviewer remains responsible
for accepting, revising, or rejecting them. The demo does not claim real-world
intervention effectiveness.

## Install and Run

Python 3.10 or newer is recommended.

```bash
cd tif-core
python -m pip install -r requirements.txt
python app.py
```

On systems where Python is named `python3`, use `python3` in the same commands.

The program prints each workflow stage and creates:

```text
tif-core/demo_result.json
```

The output contains the input case, discovered target, two interventions,
validation results, and one structured feedback record.

## Relationship with WeKnora

WeKnora may later provide retrieved evidence and citations:

```text
WeKnora: documents → retrieval → evidence and citations
TIF Core: evidence → targets → interventions → human feedback
```

The current MVP uses local evidence so it remains easy to run and explain.

## Evidence-to-Action Skill Wrapper

TIF Core remains the underlying workflow. `skill.py` adds one stable public
interface, `evidence_to_action()`, without duplicating or replacing the core
target-discovery, intervention-generation, or validation logic.

The Skill accepts generic context, constraints, and retrieved evidence. It
returns targets, intervention candidates, validation results, evidence
traceability, and a package of questions for human review. Human acceptance,
revision, rejection, and field-level feedback remain outside the first Skill
call. The included building case is only an example.

```bash
python app.py
python skill.py
```

- `app.py` demonstrates the complete original TIF workflow, including mock
  human feedback and a saved JSON record.
- `skill.py` demonstrates the reusable, framework-facing Skill interface.

The Skill remains deterministic and requires no API key. It could later be
exposed through a REST API, MCP tool, or Agent framework.

## Future Extensions

- Replace deterministic mock generation with an LLM.
- Receive evidence from the WeKnora REST API.
- Expose target discovery and intervention generation as MCP tools.
- Add interactive command-line human feedback.
- Regenerate only the field requested by the reviewer.
- Add another non-building example.
