---
title: LLM Budget-Friendly Design
description: Core philosophy and actionable principles for designing efficient, reliable, and scalable AI systems that minimize unnecessary LLM usage.
status: active
tags: [llm, design, efficiency, architecture, principles]
last_verified: 2026-07-29
layer: warm
applies_to: AI system design, LLM-based architectures, workflow design
---

# LLM Budget-Friendly Design

> A good AI framework continuously moves deterministic work away from the LLM until the only thing left is making decisions under uncertainty.

## Overview

This document describes how to design efficient, reliable, and scalable AI systems that work well with local LLMs, small models (1B-13B parameters), limited context windows, limited reasoning capacity, expensive inference, and long-running autonomous workflows. It targets architects and developers building LLM-based systems where token cost, latency, and model capability are constrained.

The objective is not to make the LLM do more. The objective is to make the LLM responsible only for tasks that genuinely require intelligence. Everything else should be handled by deterministic systems.

For detailed patterns and implementation guidance, see [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md). For operations and governance principles, see [LLM Budget-Friendly Design — Operating](llm-budget-friendly-design-operating.md).

---

## Purpose

This document applies to:

- local LLMs
- small models (1B - 13B parameters)
- limited context windows
- limited reasoning capacity
- expensive inference
- long-running autonomous workflows

---

## Core Mental Model

An LLM is not a complete application. An LLM is a reasoning component.

### What the LLM is not

It should not be treated as:

- a database
- a workflow engine
- a parser
- a serializer
- a file manager
- a validator
- a calculator
- a compiler
- a memory system

Those are software responsibilities.

### What the LLM is for

- interpretation
- planning
- judgement
- ambiguity resolution
- risk analysis
- creative generation
- tradeoff evaluation

### System architecture

A reliable AI system looks like:

```text
             User
               |
               v
         Workflow Engine
               |
     +---------+---------+
     |                   |
     v                   v
Deterministic          LLM
Runtime                Reasoning

Scripts                Decisions
Validators             Analysis
Serializers

     |
     v
Artifact Storage
```

The LLM is not the system. The LLM is one component inside the system.

---

## Design Balance

### Determinism Is a Tool, Not a Goal

The purpose of determinism is to reduce unnecessary cognitive load, not to eliminate intelligence or create rigid workflows.

### Bad implementation

```text
Everything is a state machine.
Everything is a script.
LLM only fills forms.
```

This produces a glorified automation engine.

### Good implementation

```text
Deterministic system:
- controls execution
- stores state
- validates results

LLM:
- handles ambiguity
- makes decisions
- explores options
```

The goal is not less AI. The goal is better allocation of AI.

---

## First Principle: Deterministic Work Belongs in Software

### Rule

If software can perform a task reliably, do not spend AI tokens performing it.

### Software responsibilities

- JSON generation
- YAML generation
- XML generation
- parsing
- sorting
- searching
- filtering
- validation
- calculations
- file operations
- API requests
- authentication
- retries
- formatting
- compression
- conversion
- testing

### LLM responsibilities

- deciding what matters
- interpreting unclear information
- evaluating options
- reasoning about risks
- designing solutions
- resolving ambiguity

### Example

Bad:

```text
Read these 500 files and summarize the project structure.
```

Better:

```text
Script:
  scan_repository()
Output:
  repository_map.json
LLM:
  Analyze repository_map.json
```

The LLM receives information. It does not perform mechanical extraction.

---

## Reasoning Is the Scarce Resource

Tokens are not the only constraint. The most limited resource is reasoning capacity.

A small model can fail when forced to handle:

- instructions
- formatting
- memory
- planning
- syntax
- constraints
- decision making

at the same time.

### Example of overloaded workload

```text
Generate valid JSON.
Remember 20 rules.
Analyze security risks.
Create a deployment plan.
Explain your reasoning.
```

The model is not necessarily bad. The workload is badly designed.

### Design goal

Remove everything that does not require intelligence. The LLM should spend its capacity on:

- uncertainty
- judgement
- decisions

---

## The LLM Should Generate Meaning, Not Syntax

One of the biggest sources of wasted tokens and failures is asking LLMs to manually produce structured formats:

- JSON
- YAML
- XML
- CSV
- SQL
- HTML
- Markdown tables

These are serialization problems. Software already solves serialization.

### Bad approach

```text
Generate:
{
  "name":"Alice",
  "age":30,
  "active":true
}
```

The model must handle:

- brackets
- quotes
- commas
- escaping
- schema compliance

None of this requires intelligence.

### Better approach

LLM output:

```text
SET name Alice
SET age 30
SET active true
```

Software converts:

```text
semantic data
  |
  v
JSON/YAML/database/API
```

The LLM provides meaning. Software provides correctness.

---

## Use a Serialization Layer

Never rely on prompting the model:

- "always output valid JSON"
- "remember the schema"
- "escape strings correctly"

Move this into software.

### Architecture

```text
semantic_state.txt
  |
  v
serializer
  |
  v
json  yaml  toml  xml  csv
```

The model should not care about the final format.

---

## The Framework Owns State, Not the LLM

The LLM should never be responsible for remembering:

- workflow position
- completed steps
- previous sessions
- retries
- failures
- checkpoints

Those are framework concerns.

### Ownership boundaries

Framework owns:

```text
current phase
completed phases
artifact locations
permissions
retry count
failure state
```

LLM owns:

```text
analysis
hypotheses
recommendations
tradeoffs
decisions
```

### Bad

```text
AI: "I think we finished design and should start implementation."
```

### Good

```text
Framework:
  Current phase: implementation
AI:
  Determine implementation strategy.
```

---

## Complex Workflows Have Deterministic State Boundaries

Multi-phase AI systems should have deterministic state boundaries, while allowing intelligent decisions inside those boundaries.

### Example state machine

```text
requirements_pending
  |
  v
requirements_complete
  |
  v
design_pending
  |
  v
design_complete
  |
  v
implementation_pending
```

Each transition has:

- required inputs
- validation rules
- outputs
- failure states

The LLM operates inside a state. It does not manage the state machine.

### Framework role

The framework controls: `Can this transition happen?`

### LLM role

The LLM decides: `Which valid transition is best?`

### Example comparison

Bad — everything is hardcoded:

```text
STATE_A
  |
  | always
  v
STATE_B
```

Better — LLM chooses among valid transitions:

```text
STATE_A

LLM decides:
- continue
- request more information
- retry
- escalate

Framework validates transition.
```

---

## Related Documents

- [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md) — detailed patterns and implementation guidance for externalizing memory, file-based state passing, skills design, and more
- [LLM Budget-Friendly Design — Operating](llm-budget-friendly-design-operating.md) — operations and governance principles for workflow state separation, recoverability, token budgeting, and reversible actions
- [Reference File Standards](reference-standards.md) — the structural standards that apply to all reference files in this repository
