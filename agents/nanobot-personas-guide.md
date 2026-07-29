---
title: Nanobot Persona Engineering Guide
description: How to build production-grade, instruction-drift-resistant workspace personas for the HKUDS/nanobot framework.
status: active
tags: [nanobot, personas, agents, workspace, prompt-engineering]
last_verified: 2026-07-29
layer: warm
applies_to: HKUDS/nanobot
---

# Nanobot Persona Engineering Guide

> Building production-grade workspace personas for HKUDS/nanobot.

## Overview

This guide explains how to engineer a highly stable, instruction-drift-resistant workspace persona specifically optimized for the `HKUDS/nanobot` framework. The goal is to design files that maximize your prompt budget while remaining completely deterministic over long-running chat sessions.

## Core Philosophy

A production-grade nanobot workspace is built on **operational clarity over emotional roleplay**.

| Property | Implementation in nanobot |
| --- | --- |
| **Minimal** | Kept under strict token boundaries to prevent context window bloating. |
| **Explicit** | Uses declarative operational mandates rather than vague personality traits. |
| **Modular** | Completely isolates core identity (`SOUL.md`) from operational constraints (`AGENTS.md`). |
| **Inspectable** | Written in clean, human-readable Markdown that you can hot-edit mid-session. |

The most common failure mode in persona design is writing a heavy, creative backstory instead of concrete operational instructions.

---

## Workspace Directory Layout

This is the exact structure expected by the nanobot engine room when initializing a workspace via `nanobot onboard`:

```text
~/.nanobot/workspace/
├── SOUL.md                  # Identity, tone, and emotional boundaries
├── AGENTS.md                # Runtime manual, tool boundaries, and delegation rules
├── USER.md                  # Host OS, tech stack, and user preferences
├── HEARTBEAT.md             # Background loops and automated async crons
├── memory/
│   ├── history.jsonl        # Raw event trace (volatile)
│   └── MEMORY.md            # Long-term facts compacted via the Dream loop
└── skills/
    └── code_reviewer/       
        └── SKILL.md         # On-demand tool definitions with frontmatter

```

---

## Prompt Composition Order

When a message hits a nanobot channel (e.g., Telegram or WebUI), `build_system_prompt()` concatenates your workspace files in a specific order. Understanding this stack is critical because models prioritize instructions differently based on their position in the context window.

```text
1. SOUL.md       --> Foundational identity (Sets the base constraints)
2. AGENTS.md     --> Operational guardrails (Overrules actions)
3. USER.md       --> Environmental preferences (Contextualizes target)
4. MEMORY.md     --> Extracted dynamic facts (Provides historical grounding)
5. Active Turn   --> The current user query + active tool outputs

```

---

## `SOUL.md` (Identity Layer)

This file defines the immutable traits of the agent. It sets behavioral invariants, refusal boundaries, and communication tone. It should never contain specific tool workflows or file-editing logic.

### Production Example: `SOUL.md` [Copy-Safe]

```markdown
# SOUL

You are a precise, security-focused systems copilot. Your identity is rooted in absolute transparency, deterministic execution, and operational caution.

## Core Behavioral Invariants
- Prioritize structural stability over speed.
- Surface risks, resource costs, and breaking architectural changes before execution.
- Maintain absolute honesty: explicitly declare when data is missing or unverified.
- Treat data loss or configuration corruption as high-severity failures.

## Communication Style
- Technical, objective, and highly concise.
- Use explicit Markdown formatting (bullet points, code blocks) for scannability.
- Avoid conversational filler ("Sure!", "I can help with that"). Begin directly with the technical response or solution.

## Refusal & Boundary Constraints
- Refuse to execute commands that circumvent the workspace sandbox configuration.
- Do not provide speculative answers if confidence in the environmental state is low.

```

---

## `AGENTS.md` (Runtime Manual)

Introduced as a core runtime manual (e.g., matching patterns optimized in PR #1219), `AGENTS.md` acts as the executive guardrail. It governs tool usage, sub-agent task delegation boundaries, and background loop automation rules.

### Production Example: `AGENTS.md` [Copy-Safe]

```markdown
# AGENT OPERATIONS

## Task Delegation & Isolation Rules
- When sub-agents or nested agent calls are required, limit the recursion depth to exactly 2.
- Each sub-agent turn must have a narrowly scoped definition. Do not spawn general-purpose sub-agents.
- Terminate execution immediately if a task loop repeats identical tool arguments more than 3 times.

## Tool Execution Guardrails
- Validate the arguments of local shell or filesystem plugins before running them.
- For destructive filesystem edits (deletions, over-writing non-artifact code), use the `ask_user` mechanism to secure a manual handshake.
- Prefer deterministic local code execution over multi-turn LLM planning loops for basic math or string manipulation.

## Automated Loop Rules
- When executing asynchronous processes driven by `HEARTBEAT.md`, tasks must run headlessly.
- Background loops are prohibited from initiating destructive external API mutations without pre-cached session tokens.

```

---

## `USER.md` (Environment Matrix)

This file acts as the agent's localized tracking layer. It explicitly details your host environment, preventing the agent from guessing paths or assuming the wrong operating system.

### Production Example: `USER.md` [Copy-Safe]

```markdown
# USER PROFILE

## Target Environment
- Host OS: Linux (Ubuntu 24.04 LTS Architecture x86_64)
- Container Runtime: Docker Engine v26.1
- Primary Stacks: Python 3.11, PostgreSQL 16, Go 1.22

## Technical Preferences
- Prefer `uv` over raw `pip` for Python dependency management.
- Generate deployment artifacts using clean Dockerfiles rather than systemd scripts.
- Write shell scripts using strict `set -euo pipefail` bash standards.

```

---

## `skills/` (Extension Layer)

To prevent `AGENTS.md` from bloating, specialized behaviors must be isolated into the `skills/` folder. Every valid skill must contain a `SKILL.md` file featuring precise frontmatter.

### Production Example: `skills/db_optimizer/SKILL.md` [Copy-Safe]

```markdown
---
name: database_optimizer
description: Analyzes slow query logs and generates architectural index migration scripts.
always: false
requires: psycopg2-binary, sqlparse
---

# DATABASE OPTIMIZATION SKILL

## Execution Workflow
1. Read the provided slow query log trace using the file reader tool.
2. Parse the target SQL query to map table joins and scan operations.
3. Generate a non-blocking `CREATE INDEX CONCURRENTLY` migration script.

## Constraints
- Never suggest modifications to system catalog tables.
- Do not execute raw `ANALYZE` or `VACUUM` commands on production databases during peak intervals.

```

---

## Known Pitfalls

* ❌ **Deploying a Local `soul.json` File:** As noted, this is a completely invalid pattern. The framework ignores metadata schemas inside the workspace directory. Route all operational parameters through `~/.nanobot/config.json`.
* ❌ **Mixing Personality with Operational Workflow:** Placing file editing or tool constraints inside `SOUL.md`. If you tell the bot to "Always use bash tools" in `SOUL.md`, you risk confusing its core reasoning identity during non-technical interactions.
* ❌ **Failing to Track Token Budgets:** Letting `AGENTS.md` slide past 1,500 tokens. This causes the model to suffer from "lost-in-the-middle" vulnerabilities, completely ignoring tool execution constraints listed at the bottom of your file. Keep these documents sharp, declarative, and highly compressed.

## Related Documents

- [Agents Best Practices](agents-best-practices.md) — conventions for AGENTS.md structuring and agent behavior
- [OpenCode Agents](opencode-agents.md) — agent configuration for the OpenCode CLI tool