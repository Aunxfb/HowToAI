---
title: LLM Budget-Friendly Reference Architecture
description: Reference architecture for budget-friendly AI frameworks — system overview, project structure, runtime loop, context loading, multi-agent communication, failure handling, and model replacement.
status: active
tags: [llm, architecture, reference, runtime, state-machine, agents, workflow]
last_verified: 2026-07-29
layer: warm
applies_to: AI framework architects and implementors
---

# LLM Budget-Friendly Reference Architecture

## Overview

This document describes the reference architecture for a budget-friendly AI framework — the system diagram, recommended project layout, runtime loop, context loading strategy, multi-agent communication patterns, failure handling, model replacement strategy, and the final architecture rule. Use this document as a blueprint when implementing the framework defined by the design procedure and templates.

---

## System Overview

A budget-friendly AI framework:

```text
                         User
                           |
                           v
                   Workflow Controller
                           |
                           v
                  State Machine Engine
                           |
           +---------------+---------------+
           |                               |
           v                               v
  Deterministic Runtime                LLM
  Scripts                              Reasoning
  Validators                           Decisions
  Serializers                          Analysis
           |                               |
           +---------------+---------------+
                           |
                           v
                  Artifact Storage
```

---

## Recommended Project Structure

```text
ai_framework/
    agents/
        planner.yaml
        reviewer.yaml

    phases/
        requirements.yaml
        design.yaml
        implementation.yaml

    skills/
        filesystem.yaml
        search.yaml
        compiler.yaml

    scripts/
        serializer.py
        validator.py

    state/
        workflow.json

    workspace/
        inputs/
        outputs/
        artifacts/

    prompts/
        system.md

    logs/
```

---

## Runtime Loop

The runtime should look like:

```text
while workflow.running:
    load_state()
    determine_current_phase()
    validate_inputs()
    execute_deterministic_steps()
    invoke_LLM_if_required()
    validate_outputs()
    save_artifacts()
    update_state()
    transition_phase()
```

The LLM is one operation inside the workflow. Not the workflow itself.

---

## Context Loading Strategy

Never:

```text
Load entire history.
```

Never:

```text
Load entire repository.
```

Prefer:

```text
workflow state
+
current phase
+
required artifacts
+
skill results
```

Context should be assembled. Not accumulated.

---

## Multi-Agent Communication

Agents communicate through artifacts.

Example:

```text
research_agent
   |
   v
research.md
   |
   v
analysis_agent
   |
   v
analysis.md
```

Not:

```text
Agent A explains everything to Agent B through conversation.
```

---

## Failure Handling

Every phase must define:

```text
failure state
retry policy
rollback method
human escalation point
```

Example:

```text
implementation_failed
   |
   +---- retry
   |
   +---- request_review
   |
   +---- rollback
```

---

## Model Replacement

The framework should survive model changes.

```text
Local 7B model
   |
same framework
   |
Cloud 70B model
```

The architecture should not depend on a specific model.

A better model improves decisions. It does not repair bad design.

---

## Final Architecture Rule

When designing an AI framework:

1. Define states.
2. Define transitions.
3. Move deterministic work into software.
4. Create artifacts.
5. Create skills.
6. Create agents.
7. Write prompts last.
8. Measure failures.
9. Reduce complexity.

The best AI systems are not giant autonomous agents. They are deterministic systems that use AI exactly where deterministic software cannot replace judgement.

---

## Human Approval Boundary

Not everything should be autonomous.

Architecture:

```text
                 Workflow Engine
                       |
                Decision Point
                       |
           +-------------+-------------+
           |                           |
           v                           v
        Auto Execute             Human Review
```

Define for each phase whether a human decision gate is required before proceeding.

---

## Related Documents

- [LLM Budget-Friendly Design Appendix](./llm-budget-friendly-design-appendix.md) — core design procedure and conceptual principles
- [LLM Budget-Friendly Design Templates](./llm-budget-friendly-design-templates.md) — design templates for state models, phase contracts, skills, agents, and prompts with YAML examples
- [Reference File Standards](./reference-standards.md) — standards governing all reference files in this repository
- [LLM Budget-Friendly Design](./llm-budget-friendly-design.md) — core principles document
