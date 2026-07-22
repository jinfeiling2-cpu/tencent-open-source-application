# Project Application Proposal

## 1. Applicant & Target Project

**Applicant:** Feiling Jin  
**Affiliation:** Ph.D. Candidate, The University of Hong Kong  
**Target Project:** WeKnora  

## 2. Proposed Direction

I propose to develop a lightweight prototype named **TIF Core** for domain RAG systems.

Many RAG systems stop at question answering. TIF Core explores a small extension from retrieved evidence to actionable outcomes:

**Evidence → Target Discovery → Intervention Generation → Human-in-the-Loop Feedback**

The prototype will identify actionable targets from retrieved evidence, generate structured intervention candidates, and collect field-level human feedback for later refinement.

TIF Core will first run as an independent Python tool with a local example and mock evidence input. It may then be connected to WeKnora through a lightweight API or MCP interface. The project will not modify WeKnora’s Go core or attempt to build a complete building intervention system.

Expected outputs include:

- structured target, intervention, and feedback schemas;
- a runnable end-to-end demonstration;
- saved human-feedback records;
- a lightweight WeKnora integration guide or adapter skeleton.

## 3. Time Plan

Through this project, I expect to:

- understand WeKnora’s RAG and Agent workflows;
- learn how retrieved evidence and citations can support structured actions;
- gain practical experience with human-in-the-loop feedback;
- complete at least one meaningful Issue, documentation contribution, example, or small Pull Request.

The main technologies and modules I expect to explore include:

- WeKnora document retrieval and citation outputs;
- structured LLM generation;
- JSON schema validation;
- target and intervention modeling;
- field-level human feedback;
- REST API and possible MCP integration.

The detailed implementation schedule is provided in [weekly-plan.md](weekly-plan.md).

## 4. Open-Source Experience

I do not yet have extensive formal open-source contribution experience.

My relevant experience includes:

- Python-based research prototyping;
- LLM and RAG workflow design;
- structured schema and prompt design;
- graph and spatio-temporal modeling concepts;
- human-in-the-loop evaluation;
- interdisciplinary research involving AI, human behavior, and the built environment.

My planned contribution path is:

1. read the WeKnora documentation and contribution guidelines;
2. reproduce the basic local RAG workflow;
3. complete the TIF Core prototype;
4. connect retrieved evidence to the prototype;
5. submit an example, documentation improvement, Issue, or small Pull Request.

## 5. Additional Materials

- [Public Profile](public-profile.md)
- [Weekly Plan](weekly-plan.md)
- [TIF Core Prototype](tif-core/README.md)
- GitHub: https://github.com/jinfeiling2-cpu
- Email: jinfeiling@connect.hku.hk

I hope to use a small but complete TIF Core prototype as the starting point for sustainable open-source contribution. Rather than building only a domain question-answering demo, I aim to explore a reusable **Knowledge-to-Action** workflow and gradually contribute examples, evaluation materials, documentation, or code improvements to the WeKnora community.
