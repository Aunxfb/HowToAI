---
title: LLM Budget-Friendly Design Patterns
description: Detailed patterns and implementation guidance for externalizing memory, file-based state passing, context boundary splitting, skills design, and interfaces optimized for AI consumption.
status: active
tags: [llm, design, patterns, implementation, skills, interfaces]
last_verified: 2026-07-29
layer: cold
applies_to: AI system design, LLM-based architectures, agent skill interfaces, memory management
---

# LLM Budget-Friendly Design Patterns

## Overview

This document provides detailed implementation patterns for building LLM-based systems that minimize unnecessary token consumption and maximize reliability. It covers memory externalization, file-based communication, context boundary decomposition, skill API design, interface optimization, prompt minimization, software-enforced rules, and weak-model-first design.

It is the second part of the LLM Budget-Friendly Design series. Read the [core philosophy and principles](llm-budget-friendly-design.md) first. For operations and governance, see [LLM Budget-Friendly Design — Operating](llm-budget-friendly-design-operating.md).

---

## Externalize Memory

Conversation is temporary. Files are persistent.

Do not rely on:

- previous chat messages
- hidden memory
- model recall

Store important information externally.

### File structure example

```text
workspace/
  state/
    workflow.json
    phase.json
  artifacts/
    analysis.md
    decisions.md
    results.md
  logs/
```

### Benefits

- resumable
- debuggable
- versionable
- inspectable
- transferable between models

---

## File-Based State Passing

Agents should communicate through artifacts, not conversations.

### Bad

```text
Agent A tells Agent B:
"Here is what happened earlier..."
```

### Good

```text
Agent A
  writes:
    research.md

Agent B
  reads:
    research.md
```

### Benefits

- no hidden context
- easy recovery
- model replacement
- auditing
- parallel execution

---

## Split by Context Boundaries, Not Task Names

The important unit is not the agent. The important unit is the context boundary.

### Bad splitting

```text
database_agent
api_agent
frontend_agent
backend_agent
```

when all need the same architecture context.

### Good splitting

```text
requirements_phase
implementation_phase
security_review_phase
```

because each has different:

- information
- goals
- evaluation criteria

### The right question

Not: "Can this be another agent?"

But: "Does this have a different context boundary?"

---

## Skills Are APIs, Not Documentation

A skill is a capability interface. It should expose:

- purpose
- inputs
- outputs
- constraints

Nothing more.

### Bad

```text
This skill carefully analyzes files by recursively traversing...
```

### Good

```text
search_files(path, pattern)

Returns:
  matching file paths

Side effects:
  none
```

The model needs to know: "When should I use this?" Not: "How does this work internally?"

### Finding the right abstraction level

Skills should be high-level enough to reduce planning, but low-level enough to preserve control.

Too low:

```text
read_file()
write_file()
execute_shell()
```

The model must orchestrate everything.

Too high:

```text
solve_problem()
```

The system becomes opaque.

Sweet spot:

```text
analyze_repository()
generate_report()
run_security_scan()
prepare_release()
```

---

## Skills Should Hide Complexity

Small models perform better when complexity is hidden.

### Bad — too many steps exposed

```text
read_file()
parse_file()
validate_file()
transform_file()
save_file()
```

### Better — single meaningful operation

```text
process_document()
```

### Bad — procedural steps exposed

```text
download()
extract()
verify()
move()
configure()
```

### Better — single meaningful operation

```text
install_package()
```

Good skills remove decisions from the model.

### Observability requirement

Skills hide complexity from the LLM, but never hide execution details from the system.

A skill should expose:

```text
result
metadata
artifacts
logs
errors
```

Bad:

```text
compile_project()
Success.
```

Good:

```text
compile_project()
status: success
warnings: 3
artifact: build/output.bin
duration: 32s
```

---

## AI-Friendly Interfaces

Interfaces should be designed for machines, not only humans.

### Bad — human-oriented naming

```text
final_version_latest_REAL.md
```

### Good — predictable naming

```text
result.md
```

### Bad — narrative output

```text
The operation completed successfully.
```

### Good — machine-parseable output

```text
STATUS=SUCCESS
FILE=/output/result.txt
```

Predictability is more valuable than readability.

---

## Keep Prompts Minimal

Every instruction consumes attention.

Avoid:

- personality text
- unnecessary explanations
- repeated rules
- motivational language
- excessive examples

### Prefer

```text
Read task.md.
Create plan.md.
Do not modify source files.
Return DONE.
```

Every sentence should change behavior.

---

## Put Rules in Software

Prompt rules are suggestions. Software rules are guarantees.

### Bad — prompt-based rule

```text
Never overwrite files.
```

### Better — software-enforced rule

```text
safe_write()
```

### Bad — prompt-based rule

```text
Always validate JSON.
```

### Better — software-enforced rule

```text
schema_validator()
```

The best instruction is a system that prevents mistakes.

---

## Design for Weak Models First

Assume:

- small context
- weak planning
- occasional hallucination
- poor syntax generation
- limited memory

If a design works on a 3B model, stronger models become upgrades, not requirements.

### Model capability scaling

The architecture should degrade gracefully downward and improve gracefully upward.

Same workflow:

```text
3B model:
  simple classification

13B model:
  basic planning

70B model:
  complex reasoning
```

The architecture stays unchanged. Only the reasoning quality changes.

---

## Related Documents

- [LLM Budget-Friendly Design](llm-budget-friendly-design.md) — core philosophy and actionable principles (read this first)
- [LLM Budget-Friendly Design — Operating](llm-budget-friendly-design-operating.md) — operations and governance principles for workflow state separation, recoverability, token budgeting, and reversible actions
- [Reference File Standards](reference-standards.md) — the structural standards that apply to all reference files in this repository
