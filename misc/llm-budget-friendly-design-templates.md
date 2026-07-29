---
title: LLM Budget-Friendly Design Templates
description: Design guidance and YAML templates for AI framework components — state models, phase contracts, skills, agents, prompts, and supporting template examples.
status: active
tags: [llm, design, templates, yaml, state-model, phase-contracts, skills, agents]
last_verified: 2026-07-29
layer: warm
applies_to: AI framework implementors
---

# LLM Budget-Friendly Design Templates

## Overview

This document provides practical design guidance for the intermediate components of an AI framework — state models, phase contracts, skills, agents, and prompts — along with reusable YAML templates for each component. Use this document when you have completed the core design procedure (state machine, decomposition, classification, eligibility test) and need to codify the resulting design.

---

## Create the State Model

Before creating agents, define what must survive between sessions.

Typical state:

```text
workflow_state
phase_state
decision_history
artifacts
logs
checkpoints
```

Recommended layout:

```text
workspace/
  state/
    workflow.json
    current_phase.json
  inputs/
  artifacts/
  outputs/
  logs/
```

---

## Define Phase Contracts

A phase is a bounded unit of work.

Every phase defines:

```text
Input
Process
Output
Validation
Next State
```

Example:

```yaml
Phase:
  name: Threat Analysis
  Input: architecture.md
  Process: Analyze security risks
  Output: threats.md
  Validation: threats.md exists
  Next: review_pending
```

---

## Design Skills

A skill exists when:
- a capability is reusable
- external access is required
- deterministic execution is preferred

Ask:

```text
Can this be a script?
Can this be reused?
Does this need AI?
```

Bad: `general_file_skill` — too broad.

Better:

```text
read_file()
search_files()
write_file()
```

---

## Design Agents

Create an agent only when reasoning is required.

An agent needs:

```text
Purpose
Inputs
Allowed skills
Decision responsibility
Outputs
Completion condition
```

An agent should not:
- manage workflow state
- format files
- validate schemas
- perform mechanical operations

---

## Design Prompts Last

A prompt is an adapter. It should not contain the entire system.

A good prompt contains:

```text
Current state
Goal
Available artifacts
Available skills
Output requirement
```

Example:

```text
Current phase: threat_review
Read: architecture.md
Create: threats.md
Use: security_analysis skill
```

---

## Phase Template

```yaml
phase:
  name:
  purpose:

  entry_state:

  exit_state:

  inputs:
    -

  outputs:
    -

  required_skills:
    -

  agent:

  validation:
    -

  failure_state:

  retry_policy:
```

Example:

```yaml
phase:
  name: security_review
  purpose:
    Identify security risks.

  entry_state:
    architecture_complete

  exit_state:
    security_review_complete

  inputs:
    - architecture.md
    - dependencies.json

  outputs:
    - threats.md
    - risk.json

  required_skills:
    - dependency_scan

  agent:
    threat_reviewer

  validation:
    - risk.json exists
    - schema valid

  failure_state:
    security_review_failed
```

---

## Agent Template

```yaml
agent:
  name:

  purpose:

  reasoning_required:
    true

  inputs:
    -

  outputs:
    -

  skills:
    -

  decisions:
    -

  constraints:
    -

  context:
    required_files:
      -
    forbidden_files:
      -

  success_condition:

  failure_condition:
```

Example:

```yaml
agent:
  name:
    architecture_reviewer

  purpose:
    Evaluate system design.

  reasoning_required:
    true

  inputs:
    - architecture.md

  outputs:
    - review.md

  decisions:
    - identify tradeoffs
    - recommend improvements

  success_condition:
    review.md created
```

---

## Skill Template

```yaml
skill:
  name:

  purpose:

  deterministic:

  inputs:

  outputs:

  side_effects:

  errors:

  cost:

  examples:
```

Example:

```yaml
skill:
  name:
    search_repository

  purpose:
    Find files matching a pattern.

  deterministic:
    true

  inputs:
    path:
      string
    pattern:
      string

  outputs:
    files:
      list[string]

  side_effects:
    none

  errors:
    invalid_path
    permission_denied
```

---

## Workflow State Template

```yaml
workflow:
  id:

  current_phase:

  status:

  completed_phases:

  artifacts:

  errors:

  next_action:
```

Example:

```yaml
workflow:
  id:
    project_alpha

  current_phase:
    implementation

  status:
    running

  completed_phases:
    - requirements
    - architecture

  artifacts:
    - design.md
    - api_spec.md

  next_action:
    run_tests
```

---

## Decision Template

```yaml
decision:
  question:
  options:
  constraints:
  chosen:
  reasoning:
  confidence:
  reversible:
```

---

## Skill Quality Checklist

```text
Does it reduce reasoning burden?
Does it have deterministic behavior?
Does it expose useful metadata?
Can it fail safely?
Can it be tested without an LLM?
```

---

## Related Documents

- [LLM Budget-Friendly Design Appendix](./llm-budget-friendly-design-appendix.md) — core design procedure and conceptual principles
- [LLM Budget-Friendly Reference Architecture](./llm-budget-friendly-design-arch.md) — reference architecture for budget-friendly AI frameworks
- [Reference File Standards](./reference-standards.md) — standards governing all reference files in this repository
- [LLM Budget-Friendly Design](./llm-budget-friendly-design.md) — core principles document
