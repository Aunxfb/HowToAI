---
title: Nanobot Skills
description: Covers nanobot-specific skill features including the SkillsLoader, MCP server pairing, metadata payload format, runtime support matrix, and skill configuration.
status: active
tags: [nanobot, skills, skillsloader, mcp, agent-framework]
last_verified: 2026-08-13
layer: warm
applies_to: nanobot, agent skills, SKILL.md
---

# Nanobot Skills

## Overview

This guide covers nanobot-specific skill features: the SkillsLoader, MCP server pairing, `metadata` payload format, the runtime support matrix, and nanobot-specific skill configuration.

---

## How nanobot Manages Skills

In nanobot, skills are managed as specialized workspace modules rather than being hardcoded into the agent logic.

* **The SkillsLoader:** nanobot uses a component called `SkillsLoader` (`nanobot/agent/skills.py`) to discover and parse skills.
* **File-Based Structure:** Custom agent skills are structured as individual markdown files named **`SKILL.md`** and stored within specific subdirectories in your workspace skills path (e.g., `~/.nanobot/workspace/skills/<skill-name>/SKILL.md`).
* **Format:** Each skill contains valid **YAML frontmatter** at the top (enclosed between `---` delimiters) which defines metadata like the name, description, and required configurations. The markdown body contains the semantic instructions that explicitly teach the agent how and when to use specific workflows.
* **On-Demand Loading:** Based on the user prompt or explicit intent, nanobot reads these files and dynamically injects the skill metadata and instructions into the model's active system prompt context.

* **Skills Summary (Progressive Loading):** `SkillsLoader.build_skills_summary()` builds a compact list of all available skills with their descriptions and availability status. The agent reads this summary and requests full skill content via `read_file` when triggered.

* **Availability Filtering:** `list_skills(filter_unavailable=True)` (default) hides skills whose `requires.bins`/`env` are not met. Use `filter_unavailable=False` to see all skills with `(unavailable: ...)` annotations.

---

## Strict Rules for the YAML Header

**name:** Must be lowercase letters, numbers, and hyphens only (e.g., `data-sync`, not `Data_Sync`). No slashes, dots, or spaces. It must match the name of the folder the skill lives in.

**description:** This is the most critical part. Make it highly descriptive about when nanobot should trigger it, using the pattern **"Use this skill when/if ..."**. The LLM relies on this semantic text to choose the skill. Avoid descriptions like "This skill teaches..." — focus on the trigger condition.

**metadata:** An optional nested object that supports `nanobot` or `openclaw` sub-payloads. The `always` and `requires` flags can live here instead of (or alongside) the top-level. This enables compatibility with both nanobot and OpenClaw frameworks from a single `SKILL.md`.

**[Copy-Safe]**
```yaml
---
name: skill-name
description: what the skill does and when to use it
metadata:
  always: true
  requires:
    bins:
      - python3
    env:
      - GITHUB_TOKEN
---
```

**requires:** A map with two optional keys: `bins` (CLI commands checked via `shutil.which()`) and `env` (environment variable names checked via `os.environ.get()`). If any listed bin is missing from PATH or any env var is unset, the skill is filtered from `list_skills(filter_unavailable=True)` and marked as `(unavailable: ...)` in the skills summary.

**disabled_skills** (config): In `~/.nanobot/config.json`, a `disabled_skills` set suppresses named skills from discovery. This is useful for temporarily disabling built-in or workspace skills without deleting them.

---

## Defining Skills that Pair with MCP Servers

nanobot converts connected MCP capabilities into tools that the model can interact with. nanobot maps MCP primitives (Tools, and newly exposed Resources & Prompts) as active structural options for the model.

Because MCP servers inherently expose raw, atomic functional endpoints (e.g., "execute this query" or "write this file"), the model can sometimes hallucinate or hesitate to call them properly. To pair a custom skill effectively with an MCP server, use the following rules:

### 1. Match the Directory & Frontmatter Configuration

Your `SKILL.md` must be placed correctly, and its frontmatter should acknowledge the tools or runtime requirements.

**[Copy-Safe]**
```markdown
---
name: database-analytics
description: Use this skill when the user wants to query any PostgreSQL database, preferably using the PostgreSQL MCP server tools.
---

## Guidelines
```

### 2. Provide Clear "Execution Guards"

A common issue highlighted in the project's tracker is models "pretending" to execute a skill or speculating on feedback rather than actually firing the underlying MCP tool. To prevent this, your `SKILL.md` body should contain explicit behavioral instructions telling the agent exactly when to stop reasoning and execute the underlying MCP tool.

> **Example Pattern for `SKILL.md`:**
>
> * If the user explicitly asks to fetch data or process an execution, perform the requested MCP tool action immediately.
> * Do not speculate or guess the output; run the command and use the actual response.

### 3. Account for Protocol Name Formats

nanobot registers capabilities from connected servers by combining strings (e.g., `mcp_<server_name>_tool_<tool_name>`). When documenting workflows inside your skill's markdown body, explicitly reference these generated tool names so the agent maps your written rules perfectly to the active MCP server tools exposed in its context window.

---

## Skill Attributes: `always` & `requires` Summary

### The `always` Attribute (Activation Mode)

Controls **when and how** a skill is loaded into the bot's context window.

* **`always: false` (Default / Conditional)**
    * **Behavior:** The skill remains passive (lazy-loaded). It is only fully activated when triggered by user intent or requested by another skill.
    * **Use Case:** Specialized tasks (e.g., `calculate-invoice`, `translate-text`) to save system resources and token usage.
* **`always: true` (Permanent)**
    * **Behavior:** The skill is active for every single interaction, running continuously in the background.
    * **Use Case:** Global or supervisory tasks (e.g., `safety-filter`, `tone-checker`, `logging`).

The `always` flag is checked at two levels in the frontmatter: the top-level key, and also inside the nested `metadata` object (which supports both `nanobot` and `openclaw` sub-payloads).

### The `requires` Attribute (System Requirements)

Defines **environmental prerequisites** that must be met before a skill is considered available. This is not skill-to-skill chaining — it checks for CLI tools and environment variables.

**[Copy-Safe]**
```yaml
requires:
  bins:
    - python3
    - git
  env:
    - GITHUB_TOKEN
    - AWS_SECRET_ACCESS_KEY
```

* **`requires.bins`** — list of CLI commands that must be found in PATH (`shutil.which()`). If any are missing, the skill is marked unavailable.
* **`requires.env`** — list of environment variable names that must be set. If any are missing, the skill is marked unavailable.

Missing requirements appear in the skills summary as `(unavailable: CLI: <name>)` or `(unavailable: ENV: <name>)`.

---

## Runtime Support Matrix

| Attribute | Framework Support Status | Technical Behavior |
| :--- | :--- | :--- |
| **`always`** | **Fully Supported** | Handled by `SkillsLoader.get_always_skills()`. Skills flagged true are included in every interaction's context. |
| **`requires`** | **Fully Supported** | `SkillsLoader._check_requirements()` validates `bins` (CLI in PATH) and `unavailable` (env vars set). Skilled filtered from `list_skills()` when unmet. |
| **`metadata`** | **Fully Supported** | Nested `nanobot` or `openclaw` payload parsed from frontmatter. Supports `always` and `requires` as sub-keys. |
| **`disabled_skills`** | **Fully Supported** | A set of skill names in `config.json` that `SkillsLoader.list_skills()` filters out. |

## Skill Sources

Skills can come from two locations:

| Source | Location | Override Behavior |
| :--- | :--- | :--- |
| **Workspace** | `~/.nanobot/workspace/skills/<name>/` | Takes priority — if a workspace skill and a builtin skill share the same name, the workspace version wins. |
| **Builtin** | `nanobot/skills/<name>/` (installed with nanobot) | Ship with the package; provide baseline functionality. |

The `source` field on each skill entry tracks where it was loaded from.

---

## Writing Effective Skill Instructions

When you write instructions within a skill, you should address the agent as **"You"**.

### Why "You" is the Best Practice

**Direct Integration into System Prompts:** When nanobot dynamically loads a skill based on a user's request, the contents of your SKILL.md are appended directly into the agent's active system prompt or instruction context. Because the core system prompt tells the LLM "You are a helpful assistant...", carrying the "You" perspective into the skill maintains a consistent narrative voice for the model.

**Framework Standard:** The Agent Skills standard (originally open-sourced by Anthropic and adopted by frameworks like nanobot) treats the agent as the direct recipient of the instructions.

### Recommended Style vs. Anti-Patterns

| Correct (Use This) | Incorrect / Anti-Patterns | Why? |
|---|---|---|
| "You" — *When the user asks for data, you must format it as a markdown table.* | "nanobot" — *nanobot should format the data as a table.* | Third-person language can confuse the LLM, making it think "nanobot" is an external entity it needs to talk about or interact with. |
| Direct Imperative — *Search the workspace files before answering.* | Third-person passive — *The Agent will search the files.* | "The agent" creates a layer of abstraction that weakens the instruction's authority inside the LLM's context window. |

### Quick Example: SKILL.md Structure

**[Copy-Safe]**
```markdown
---
name: weather-analyst
description: Use this skill when the user wants a detailed breakdown of local weather trends.
requires:
  bins:
    - curl
---

## Instructions

1. You must use the fetch tool to get the latest weather payload.
2. Do not report raw JSON; you should translate the data into a clean, bulleted summary.
3. If the data is missing, you must politely ask the user for their zip code.
```

By sticking to **"You"** or **direct command verbs** ("Search", "Format", "Verify"), you ensure that nanobot executes the workflow seamlessly without any identity confusion.

## Related Documents

- [Skills Best Practices](../skills/skills-best-practices.md) — general guidelines for creating and maintaining AI agent skills
