---
title: "LLM Budget-Friendly Design \u2014 Operating"
description: Operations and governance principles for workflow state separation, recoverability, token budgeting, framework complexity, and preferring reversible AI actions.
status: active
tags: [llm, design, operations, governance, workflows, recoverability]
last_verified: 2026-07-29
layer: cold
applies_to: AI system operations, workflow governance, production AI pipelines, risk management
---

# LLM Budget-Friendly Design — Operating

## Overview

This document covers the operations and governance principles for running LLM-based systems in production. It addresses workflow state separation, recoverability, token allocation, framework complexity management, and the preference for reversible operations.

It is the third part of the LLM Budget-Friendly Design series. Read the [core philosophy and principles](llm-budget-friendly-design.md) first. For detailed patterns and implementation guidance, see [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md).

---

## Separate Workflow State and Reasoning State

Two different types of information exist and must never be mixed.

### Framework State

Deterministic. Examples:

```text
phase
status
retry_count
artifacts
permissions
```

### AI Reasoning State

Probabilistic. Examples:

```text
hypotheses
ideas
tradeoffs
recommendations
analysis
```

### Never mix them

The framework controls execution. The LLM provides intelligence.

---

## Make Everything Recoverable

A good AI workflow survives:

- crashes
- context loss
- session interruption
- model changes

Important information must exist outside the conversation.

### Required infrastructure

```text
checkpoints
artifacts
logs
state files
```

---

## Spend Tokens Only Where They Matter

### High-value token usage

- reasoning
- planning
- architecture
- evaluation
- risk analysis

### Low-value token usage

- formatting
- syntax
- copying
- validation
- conversion

Move low-value work into software.

---

## Framework Complexity Budget

A common failure mode:

```text
Need an AI assistant?
  Build:
    agent framework
    plugin architecture
    workflow engine
    memory layer
    skill registry
    monitoring system
```

...before solving the actual problem.

### Rule

```text
One working workflow first.
Extract abstractions second.
Build framework third.
```

The framework itself also needs a budget.

---

## AI Actions Should Prefer Reversible Operations

LLMs are probabilistic. Therefore workflows should minimize irreversible mistakes.

### Prefer

```text
analyze
preview
approve
apply
verify
```

### Over

```text
decide
execute
```

### Bad

```text
delete_user()
```

### Better

```text
disable_user()
  review()
  delete()
```

### Bad

```text
rewrite_database()
```

### Better

```text
generate_migration()
  validate()
  apply()
```

---

## Final Design Principle

> A good architecture makes the model's work smaller but more important.

> Build deterministic systems that create a safe operating environment for probabilistic intelligence. Give the LLM maximum freedom where judgement is required, and minimum responsibility where correctness can be guaranteed.

```text
Less execution.    More judgement.
Less memory.       More state.
Less syntax.       More meaning.
Less prompting.    More engineering.
```

---

## Related Documents

- [LLM Budget-Friendly Design](llm-budget-friendly-design.md) — core philosophy and actionable principles (read this first)
- [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md) — detailed patterns and implementation guidance for externalizing memory, file-based state passing, skills design, and more
- [Reference File Standards](reference-standards.md) — the structural standards that apply to all reference files in this repository
