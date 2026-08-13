---
title: Skills Best Practices for AI Assistants
description: Guidelines for creating, reviewing, and maintaining Skills that make AI assistants more reliable at repeatable tasks through focused instructions and clear workflow guidance.
status: active
tags: [skills, best-practices, skill-design, agent-instructions]
last_verified: 2026-08-13
layer: cold
applies_to: SKILL.md, agent skills, skill authors
---

# Skills Best Practices for AI Assistants

## Overview

Use this guide when creating, reviewing, or maintaining Skills. A Skill should make an AI assistant more reliable at a specific repeatable task by providing focused instructions, reusable resources, and clear workflow guidance.

A Skill should not be a general knowledge dump. It should encode non-obvious, task-specific behavior that improves execution.

---

## Philosophy

A good `SKILL.md` is **not documentation**.

It is an operational specification that teaches an AI agent:

* **When** to use the skill
* **What** the skill is responsible for
* **How** to perform the task
* **What not** to do
* **What success looks like**

Think of it as writing instructions for an extremely capable new teammate who has no prior knowledge of your project's conventions.

A useful mental model is:

> **A great `SKILL.md` is less like a README and more like a standard operating procedure (SOP) for an AI agent.**

---

## Core Principles

### One Skill = One Responsibility

Skills should solve exactly one repeatable problem.

Good:

* Docker deployment
* SQL migration review
* Python performance profiling
* API documentation generation

Bad:

* General programming
* Software engineering
* Everything about Kubernetes
* Complete DevOps workflow

Single-purpose skills compose much better than large monolithic ones.

### Keep `SKILL.md` Compact

Treat `SKILL.md` as the control plane for the Skill.

It should include:

* YAML frontmatter
* Core task instructions
* Required workflow steps
* Critical constraints
* Pointers to supporting files

Aim for **100–300 lines** as the ideal range, and stay under **~500 lines**. If the file grows large, move details into `references/`, `scripts/`, or `assets/`.

### Use YAML Frontmatter

Every `SKILL.md` should begin with:

**[Copy-Safe]**
```yaml
---
name: skill-name
description: what the skill does and when to use it
---
```

Required fields:

* `name`
* `description`

Optional fields:

* `always` — set to `true` for skills that should load on every interaction (global/supervisory tasks)
* `requires` — system prerequisites (CLI binaries and environment variables)
* `compatibility` — version constraints (e.g., `python>=3.11`)
* `license` — license identifier
* `metadata` — additional structured data (version, author, etc.)

Example with all fields:

**[Copy-Safe]**
```yaml
---
name: python-performance-review
description: >
  Analyze Python code for runtime performance,
  algorithmic complexity, unnecessary allocations,
  profiling opportunities, and optimization strategies.
  Use whenever optimizing Python execution speed.
always: false
requires:
  bins:
    - python3
  env:
    - GITHUB_TOKEN
license: MIT
compatibility: python>=3.11
metadata:
  version: "1.2.0"
  author: ACME
---
```

### Make the Description Trigger-Friendly

The `description` is the most critical field — it determines whether the agent loads the skill. Put trigger conditions in the description, not only in the body.

A good description states:

* What the Skill does
* The specific tasks it supports
* The contexts or user requests that should trigger it
* Any key file types, tools, connectors, or domains involved
* Important trigger keywords the user might naturally say

Weak description:

**[Conceptual]**
```yaml
description: Helps with Python.
```

Good description:

**[Copy-Safe]**
```yaml
description: Review Python code for performance bottlenecks, algorithmic complexity, memory allocation issues, vectorization opportunities, and profiling recommendations. Use whenever optimizing Python performance.
```

The description should maximize discoverability. The LLM relies on this semantic text to choose the skill.

---

## Recommended File Structure

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── analyze.py
│   └── helper.sh
├── references/
│   ├── api.md
│   ├── style-guide.md
│   └── architecture.md
└── assets/
    ├── template.md
    └── example.json
```

Use supporting folders only when they materially improve the Skill.

---

## What Belongs in `SKILL.md`

Include:

* Required behavior
* Step-by-step workflow
* Decision rules
* Validation checks
* Output formatting rules
* Instructions for when to consult supporting files
* Tool or connector usage guidance, if needed

Avoid:

* Long background explanations
* Full API documentation
* Large schemas
* General writing advice
* Repeated examples
* Information the base model already knows

---

## Detailed Section Guide

The following sections produce consistently reliable skill behavior.

### Overview

Start with a concise explanation.

**[Conceptual]**
```text
This skill performs structured Python performance
analysis using static inspection and profiling.
```

Avoid marketing language. Avoid background theory.

### When to Use

Explicitly define triggers.

Example:

* optimize Python
* improve runtime
* reduce memory
* profiling
* slow code
* benchmark
* performance regression

Agents perform much better with explicit trigger language.

### When NOT to Use

One of the most overlooked sections. Boundaries reduce accidental activation.

Example:

Do NOT use for:

* bug fixing
* architecture reviews
* style formatting
* linting
* security reviews

### Required Inputs

Specify required information.

Required:

* source files
* Python version

Optional:

* profiler output
* benchmarks
* hardware information

If required information is missing: request it, do not guess.

### Workflow

Use numbered steps.

1. Read all supplied files.
2. Identify hot paths.
3. Estimate algorithmic complexity.
4. Detect excessive allocations.
5. Identify unnecessary copies.
6. Recommend improvements.
7. Rank recommendations by expected impact.

Sequential workflows outperform large paragraphs.

### Decision Rules

Instead of vague advice:

> Optimize code.

Write deterministic rules.

**[Copy-Safe]**
```text
If complexity exceeds O(n log n)
recommend algorithm redesign.

If repeated allocations occur
recommend reuse.

If loops contain Python object creation
recommend vectorization or caching.
```

Rules outperform prose.

### Output Format

Always specify the output.

**[Copy-Safe]**
```text
Summary
Major Issues
Evidence
Recommendations
Expected Performance Gains
Risks
Next Steps
```

Never leave output formatting implicit.

### Examples

Examples are one of the strongest improvements you can make.

Input:

**[Conceptual]**
```text
Optimize this NumPy code.
```

Output:

**[Conceptual]**
```text
Summary
Issue 1
Issue 2
Recommendation
Estimated speedup
```

Concrete examples anchor behavior.

### Edge Cases

Document unusual situations.

* incomplete repository
* generated code
* conflicting benchmarks
* unsupported language version

Explain expected behavior.

### Failure Handling

Specify what to do if the task cannot proceed.

If profiling data is unavailable:

* explain limitations
* continue with static analysis
* clearly distinguish estimates from measured results

Graceful degradation is preferable to failure.

### References

Instead of embedding hundreds of lines:

**[Copy-Safe]**
```text
See:
references/style-guide.md
references/api.md
references/examples.md
```

Load large context only when necessary.

---

## Progressive Loading

Design Skills so the assistant loads only what it needs.

Use `SKILL.md` for navigation:

**[Copy-Safe]**
```md
For invoice field definitions, see `references/invoice-schema.md`.
For deterministic PDF extraction, run `scripts/extract_invoice.py`.
For branded output templates, use files in `assets/`.
```

Do not place every detail in `SKILL.md`.

### References

Use `references/` for detailed guidance that may not be needed every time.

Good reference files include:

* Domain rules
* Schemas
* API notes
* Output examples
* Compliance language
* Edge-case handling
* Team-specific conventions

For reference files longer than 100 lines, include a short table of contents.

### Scripts

Use `scripts/` when repeatable operations need accuracy or consistency.

Good script use cases:

* Parsing structured files
* Validating outputs
* Transforming spreadsheets
* Extracting data from PDFs
* Running deterministic calculations
* Packaging or formatting artifacts

If a script is included, the Skill should clearly explain when to run it and what inputs and outputs to expect.

### Assets

Use `assets/` for files used in final outputs.

Examples:

* Templates
* Logos
* Example workbooks
* Boilerplate documents
* Style assets
* Static configuration files

Do not use assets as hidden instructions. Put reasoning guidance in `SKILL.md` or `references/`.

---

## Tool and Connector Guidance

Reference tools, connectors, or MCP servers only when the Skill depends on them.

Prefer capability-level instructions:

**[Conceptual]**
```md
Retrieve the latest customer notes from the CRM connector before summarizing renewal risk.
```

Avoid brittle low-level instructions unless necessary:

**[Conceptual]**
```md
Call `crm.search_records` with this exact JSON payload.
```

Include:

* When to use the tool
* What information to retrieve
* How to validate the result
* What to do if the tool is unavailable or incomplete

---

## Writing Style

Use:

* imperative voice
* short sentences
* bullet lists
* numbered procedures
* deterministic wording

Avoid:

* essays
* storytelling
* long explanations
* repeated information
* conversational filler

Treat the file like executable instructions.

---

## Instructions — Good and Bad

Good instructions are:

* Specific
* Actionable
* Concise
* Opinionated where needed
* Focused on behavior
* Written for another AI assistant to execute

Use imperative wording:

**[Copy-Safe]**
```md
Ask for the target audience before drafting the report.
Validate all extracted totals against the source spreadsheet.
Use the approved tone examples in `references/style-guide.md`.
```

Avoid instructions that are too broad:

**[Conceptual]**
```md
Be helpful and accurate.
Write clearly.
Use good judgment.
```

Avoid dumping generic background:

**[Conceptual]**
```md
Marketing is the process of promoting products and services...
```

Avoid hiding trigger rules only in the body:

**[Conceptual]**
```md
## When to Use This Skill
Use this Skill for...
```

Trigger rules belong primarily in the YAML `description`.

---

## Common Mistakes

### Too Broad

Bad:

**[Conceptual]**
```text
Expert software engineer.
```

Good:

**[Copy-Safe]**
```text
Review PostgreSQL query plans and recommend
index improvements.
```

### Missing Trigger Conditions

Bad:

**[Conceptual]**
```text
This helps write SQL.
```

Good:

**[Copy-Safe]**
```text
Use whenever optimizing PostgreSQL queries,
EXPLAIN plans, indexes, joins, or slow queries.
```

### Ambiguous Workflow

Bad:

**[Conceptual]**
```text
Analyze the code.
```

Good:

**[Copy-Safe]**
```text
1. Parse repository
2. Locate entry point
3. Inspect dependencies
4. Identify bottlenecks
5. Produce ranked recommendations
```

### No Output Specification

Never assume the model will choose a useful format. Always define it.

### Huge Monolithic Files

Don't place API docs, architecture docs, coding standards, or templates inside `SKILL.md`. Reference them.

### Mixing Multiple Skills

Bad (single file covering everything):

**[Conceptual]**
```text
Deployment
Testing
Monitoring
Security
Documentation
```

Create independent skills instead.

---

## Security

Never include:

* API keys
* passwords
* secrets
* production credentials
* internal tokens

Avoid instructions that encourage unsafe execution. Prefer explicit validation before destructive operations.

---

## Validation Checklist

Before packaging a Skill, check that:

* `SKILL.md` exists
* YAML frontmatter has `name` and `description`; `always`, `requires`, `compatibility`, `license`, and `metadata` are optional
* Skill name is lowercase and hyphenated (matches folder name)
* Description clearly states trigger conditions
* `requires.bins` entries are real CLI tools; `requires.env` entries are real env var names
* `always` is only `true` for global/supervisory skills
* `SKILL.md` is compact and focused
* Large details are moved into references
* Scripts are tested
* Example placeholder files are removed
* Assets are necessary and not oversized
* The Skill can be understood by another AI without external explanation
* Single responsibility
* Explicit non-goals defined
* Required inputs defined
* Deterministic workflow
* Output format specified
* Examples included
* Edge cases handled
* Failure behavior defined
* No secrets
* Minimal duplication
* Concise writing

---

## Canonical Template

**[Copy-Safe]**
```markdown
---
name: skill-name
description: >
  What this skill does.
  When it should be used.
  Important trigger keywords.
license: MIT
compatibility: python>=3.12
metadata:
  version: "1.0.0"
---

# Overview

Brief purpose.

# When to Use

- trigger
- trigger
- trigger

# When NOT to Use

- non-goal
- non-goal

# Inputs

Required:

Optional:

# Workflow

1. Step one
2. Step two
3. Step three

# Decision Rules

- Rule A
- Rule B
- Rule C

# Output

Specify exact structure.

# Examples

Input:

Output:

# Edge Cases

- case
- case

# Failure Handling

Describe graceful fallback.

# References

- references/guide.md
- references/examples.md
```

---

## Final Takeaways

The highest-quality `SKILL.md` files share consistent traits:

* Narrow, single-purpose scope.
* Excellent descriptions that clearly signal when to activate.
* Deterministic, step-by-step workflows instead of vague prose.
* Explicit boundaries describing when **not** to use the skill.
* Well-defined output formats.
* Practical examples.
* Reference large documentation externally rather than embedding it.
* Concise, operational language that reads like executable instructions rather than human-facing documentation.

A Skill is successful when it helps the assistant perform a repeatable task better than it would from general instructions alone. Keep the Skill small, specific, and reusable.

## Related Documents

- [Nanobot Skills](nanobot-skills.md) — nanobot-specific skill features built on these practices
