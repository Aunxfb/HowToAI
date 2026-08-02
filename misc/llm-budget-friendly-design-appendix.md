---
title: LLM Budget-Friendly Design Appendix
description: Practical engineering procedure for designing AI frameworks — state machine first, task decomposition, operation classification, LLM eligibility, evaluation, and avoiding overengineering.
status: active
tags: [llm, design, procedure, state-machine, task-decomposition, evaluation]
last_verified: 2026-07-29
layer: cold
applies_to: AI framework designers and architects
---

# LLM Budget-Friendly Design Appendix

## Overview

This appendix converts the principles from `llm_budget_friendly_design.md` into practical engineering procedures. It defines how to design AI frameworks, how to decide what becomes a script, skill, or agent, how to design phases and state machines, how to define agent contracts and skill interfaces, and how to structure an AI runtime.

The goal is: given any AI task, systematically determine where intelligence belongs and where software should take over.

---

## Design the State Machine First

The most common mistake in AI framework design is starting with:

> "What should my agent prompt say?"

Do not start there.

Start with:

> "What states exist, and how does information move between them?"

A workflow should first be represented as:

```text
State A
   |
   | transition
   v
State B
   |
   | transition
   v
State C
```

Each state defines:
- what information exists
- what actions are allowed
- what outputs are required
- what determines completion

Example — software development workflow:

```text
requirements_pending
   |
   v
requirements_complete
   |
   v
architecture_pending
   |
   v
architecture_complete
   |
   v
implementation_pending
   |
   v
testing_complete
```

The workflow engine manages movement. The LLM only helps complete individual states.

---

## Task Decomposition Procedure

Given a task:

> Build an AI security review assistant.

Do not immediately create a `security_agent`. First decompose.

Ask:

```text
What information must be collected?
What transformations are deterministic?
What decisions require judgement?
What outputs are needed?
```

Example decomposition:

```text
Repository scanning
   |
   v
Script
   |
   v
Dependency extraction
   |
   v
Script
   |
   v
Risk interpretation
   |
   v
LLM
   |
   v
Report generation
   |
   v
Script
```

---

## Classify Every Operation

Every operation belongs to one of three categories.

### Deterministic

No AI required.

Characteristics:
- same input produces same output
- rules are known
- correctness can be tested

Examples: parse JSON, calculate hash, sort files, validate schema, convert formats, generate reports, run tests

Implementation: script, library, database, API

### Capability

Requires external systems.

Examples: search internet, read database, execute command, access repository, send email

Implementation: skill, tool, service

### Reasoning

Requires intelligence.

Examples: "Which design is better?", "Is this a security risk?", "What caused this failure?", "What should we prioritize?"

Implementation: LLM agent

---

## The LLM Eligibility Test

Before using an LLM, ask:

```text
Does this task require:
- interpretation?
- uncertainty handling?
- judgement?
- tradeoff analysis?
- creativity?
```

If no: use software.

**Should use LLM:**

```text
Evaluate whether this architecture is maintainable.
```

**Should not use LLM:**

```text
Convert YAML to JSON.
```

---

## Evaluate the Architecture

Before deployment, ask:

```text
Can the model be smaller?
Can more work become code?
Can context be reduced?
Can state be clearer?
Can skills become higher level?
Can failures recover automatically?
```

---

## Do Not Overengineer Checkpoint

Before creating an agent, skill, or phase, ask:

```text
Is this abstraction solving a repeated problem?
Does this reduce complexity?
Would the system be simpler without it?
```

---

## Related Documents

- [LLM Budget-Friendly Design Templates](./llm-budget-friendly-design-templates.md) — design templates for state models, phase contracts, skills, agents, and prompts with YAML examples
- [LLM Budget-Friendly Reference Architecture](./llm-budget-friendly-design-arch.md) — reference architecture for budget-friendly AI frameworks covering system overview, project structure, runtime loop, and failure handling
- [Reference File Standards](./reference-standards.md) — standards governing all reference files in this repository
- [LLM Budget-Friendly Design](./llm-budget-friendly-design.md) — core principles document
