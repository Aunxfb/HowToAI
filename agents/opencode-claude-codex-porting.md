---
title: Porting Agents and Skills Between Harnesses
description: Field guide for migrating agent and skill definitions between OpenCode, Claude Code, and OpenAI Codex. For developers maintaining multi-platform AI coding configurations.
status: active
tags: [agents, skills, porting, opencode, claude-code, codex, migration]
last_verified: 2026-07-29
layer: cold
applies_to: OpenCode, Claude Code, OpenAI Codex
---

# Porting Agents and Skills Between Harnesses

> A field guide for migrating agent and skill definitions between **OpenCode**, **Claude Code**, and **OpenAI Codex**.

## Overview

This document covers the architecture differences and conversion paths between three AI coding harnesses. It is for developers who need to port agent definitions, skill configurations, permissions, and AGENTS.md content across platforms.

## Architecture Overview

The three harnesses have fundamentally different execution models. Understanding this avoids fighting the platform.

| Concept | OpenCode | Claude Code | OpenAI Codex |
|---|---|---|---|
| **Main agent loop** | TUI with switchable primary agents | Single main conversation, delegates to subagents | Single main loop, uses AGENTS.md cascade and skills |
| **Agent definition format** | `opencode.json` or `.opencode/agents/<name>.md` | `.claude/agents/<name>.md` | `~/.codex/agents/<name>.toml` or `.codex/agents/<name>.toml` |
| **Skill definition** | `.opencode/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| **Discovery** | Walks up from CWD to git root | Walks up from CWD; also user/plugin scopes | Walks up from CWD to git root; also user/admin/system scopes |
| **Invocation** | `@mention` or automatic by primary agent | `@mention`, automatic delegation, or `--agent` flag | `$skill-name` (explicit or implicit by description match) |
| **Primary agent** | Build / Plan (switchable via Tab) | Default session (optionally `--agent <name>`) | The Codex main loop (no equivalent concept) |
| **Subagents** | Built-in: General, Explore, Scout. Custom via task tool | Built-in: Explore, Plan, General-purpose. Custom via Agent tool | Custom agents via TOML files; subagent workflows via `spawn_agents_on_csv` |
| **Multi-agent orchestration** | Primary agent spawns subagents via Task tool | Main conversation spawns subagents via Agent tool | Main loop routes to skills; subagent workflows for CSV/parallel batched work |

### Key insight

- **OpenCode** is a multi-primary-agent TUI: you switch between primary agents (Build, Plan) or `@mention` subagents. Subagents are spawned from the primary.
- **Claude Code** is a single-conversation model that delegates to subagents for isolation. The main thread is always the same agent type unless overridden via `--agent`.
- **Codex** has no "agent" concept — it uses a single main loop with a cascading `AGENTS.md` hierarchy. Specialized behavior comes from **skills** (loaded on-demand) and **custom agents** (TOML files for subagent/spawned use).

---

## Quick-Reference Conversion Tables

### Agent Mapping

| OpenCode | Claude Code | OpenAI Codex |
|---|---|---|
| **Primary agent** (mode: primary) | Main session (or `--agent <name>` with subagent file) | Root `AGENTS.md` + cascading overrides |
| **Subagent** (mode: subagent) in `.opencode/agents/*.md` | `.claude/agents/*.md` markdown agent | `.codex/agents/*.toml` custom agent |
| **`@mention`** subagent call | `@mention` (e.g. `@code-reviewer (agent)`) | Name the skill or agent in prompt |
| **Subagent system prompt** | Body of markdown file (after frontmatter) | `developer_instructions` field in TOML |

### Skill Mapping

| Concept | OpenCode | Claude Code | Codex |
|---|---|---|---|
| Directory | `.opencode/skills/<name>/` | `~/.claude/skills/<name>/` | `.agents/skills/<name>/` |
| Instruction file | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| Frontmatter format | YAML | YAML | YAML |
| Required fields | `name`, `description` | `name`, `description` | `name`, `description` |
| Name format | `^[a-z0-9]+(-[a-z0-9]+)*$` | lowercase-kebab | lowercase-kebab |
| Description max | 1024 chars | (same) | 1024 chars (but shortened if >2% of context) |
| Scripts dir | `scripts/` | `scripts/` | `scripts/` |
| References dir | `references/` | `references/` | `references/` |
| Plugin format | N/A | `.opencode/plugins/` | Plugin packaging |
| Extra metadata | N/A | N/A | `agents/openai.yaml` for UI metadata |

---

## Porting Agents

### 3.1 OpenCode -> Claude Code

**OpenCode agent (`.opencode/agents/review.md`):**

> **[Copy-Safe]** — OpenCode agent frontmatter template.

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

You are in code review mode. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations
```

**Claude Code equivalent (`.claude/agents/review.md`):**

```markdown
---
name: review
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
---

You are a code review specialist. Focus on:
- Code quality and best practices
- Potential bugs and edge cases
- Performance implications
- Security considerations
```

**Changes to make:**
1. Add `name` field (required in Claude Code) — use the filename without extension
2. Replace `permission: { edit: deny, bash: deny }` with `tools: Read, Grep, Glob` (allowlist)
3. Replace model ID `anthropic/claude-sonnet-4-20250514` with alias `sonnet` (or `opus`, `haiku`, `inherit`)
4. Remove `temperature` (not supported in Claude Code agent frontmatter) or keep if using provider-specific params
5. `mode: subagent` is implicit from file location — remove it

**Permission mapping (deny → tools allowlist):**

| OpenCode permission | Claude Code equivalent |
|---|---|
| `edit: deny` | Omit `Write`, `Edit` from `tools` list |
| `bash: deny` | Omit `Bash` from `tools` list |
| `read: deny` | Omit `Read` from `tools` list (rare) |
| `edit: ask` | Include `Edit`, `Write` in `tools` (permission handled by parent) |

### 3.2 Claude Code -> OpenCode

**Claude Code agent (`.claude/agents/code-improver.md`):**

```markdown
---
name: code-improver
description: Scans files and suggests improvements for readability, performance, and best practices.
tools: Read, Grep, Glob
model: sonnet
---

You are a code improvement specialist. For each issue you find, explain the problem, show the current code, and provide an improved version.
```

**OpenCode equivalent (`.opencode/agents/code-improver.md`):**

```markdown
---
description: Scans files and suggests improvements for readability, performance, and best practices.
mode: subagent
model: anthropic/claude-sonnet-4-20250514
permission:
  edit: deny
  bash: deny
---

You are a code improvement specialist. For each issue you find, explain the problem, show the current code, and provide an improved version.
```

**Changes to make:**
1. Remove `name` — OpenCode uses the filename as the agent name (no `name` field in frontmatter)
2. Add `mode: subagent`
3. Replace `tools: Read, Grep, Glob` with `permission: { edit: deny, bash: deny }` (or more granular)
4. Replace model alias `sonnet` with full provider/model ID, or omit to inherit
5. Remove `model` if you want to inherit the session model

**Tools → permissions mapping:**

| Claude Code tools | OpenCode permission equivalent |
|---|---|
| `Read` | (allowed by default, no explicit permission needed) |
| `Edit`, `Write` | `edit: allow` (or omit to inherit) |
| `Bash` | `bash: allow` (or omit to inherit) |
| `Grep`, `Glob` | (allowed by default) |
| Omit `Edit`, `Write` | `edit: deny` |
| Omit `Bash` | `bash: deny` |

### 3.3 Claude Code -> OpenAI Codex

Codex does not have a direct 1:1 agent concept. Instead, custom agents are TOML files for use in subagent workflows or spawned agents.

**Claude Code agent (`.claude/agents/code-improver.md`):**

```markdown
---
name: code-improver
description: Scans files and suggests improvements for readability, performance, and best practices.
tools: Read, Grep, Glob
model: sonnet
---

You are a code improvement specialist. For each issue you find, explain the problem, show the current code, and provide an improved version.
```

**Codex equivalent (`.codex/agents/code-improver.toml`):**

```toml
name = "code_improver"
description = "Scans files and suggests improvements for readability, performance, and best practices."
developer_instructions = """
You are a code improvement specialist. For each issue you find, explain the problem, show the current code, and provide an improved version.
"""
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
sandbox_mode = "read-only"
```

**Changes to make:**
1. Convert from YAML frontmatter + markdown body to TOML format
2. `name` → `name` (lowercase with underscores instead of hyphens)
3. `description` → `description`
4. Body → `developer_instructions` (TOML multi-line string)
5. `model` → `model` (use Codex model IDs)
6. `tools` → `sandbox_mode` (Codex uses sandbox, not tool allowlists)
7. Add `model_reasoning_effort` (maps to Claude Code's implicit reasoning)

**Tool restriction mapping (Claude Code tools -> Codex sandbox):**

| Claude Code | Codex equivalent |
|---|---|
| `tools: Read, Grep, Glob` (no Edit/Write/Bash) | `sandbox_mode = "read-only"` |
| Full tool access | `sandbox_mode = "workspace-write"` (default) |
| `tools: Read, Grep, Glob, Bash` | `sandbox_mode = "workspace-write"` (Bash is always available) |

### 3.4 OpenAI Codex -> OpenCode

**Codex agent (`.codex/agents/reviewer.toml`):**

```toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
```

**OpenCode equivalent (`.opencode/agents/reviewer.md`):**

```markdown
---
description: PR reviewer focused on correctness, security, and missing tests.
mode: subagent
model: openai/gpt-5.4
permission:
  edit: deny
  bash: deny
---

Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
```

**Changes to make:**
1. Convert from TOML to YAML frontmatter + markdown body
2. `name` → filename (OpenCode uses filename, remove `name` from frontmatter)
3. `developer_instructions` → body
4. `model` → full provider/model ID (`openai/gpt-5.4`)
5. `model_reasoning_effort` → `reasoningEffort` (pass-through to provider)
6. `sandbox_mode = "read-only"` → `permission: { edit: deny, bash: deny }`

### 3.5 OpenAI Codex -> Claude Code

**Codex agent (`.codex/agents/reviewer.toml`):**

```toml
name = "reviewer"
description = "PR reviewer focused on correctness, security, and missing tests."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"
nickname_candidates = ["Atlas", "Delta", "Echo"]
developer_instructions = """
Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
"""
```

**Claude Code equivalent (`.claude/agents/reviewer.md`):**

```markdown
---
name: reviewer
description: PR reviewer focused on correctness, security, and missing tests. Use proactively after code changes.
tools: Read, Grep, Glob
model: inherit
---

Review code like an owner.
Prioritize correctness, security, behavior regressions, and missing test coverage.
```

**Changes to make:**
1. Convert TOML to YAML frontmatter + markdown body
2. `name` → `name` (change underscores to hyphens)
3. `developer_instructions` → body
4. `model` → Claude model alias (`sonnet`, `opus`, `haiku`, or `inherit`)
5. `model_reasoning_effort` → not directly supported (Claude doesn't use reasoning_effort); you can set `effort` field
6. `sandbox_mode = "read-only"` → Omit `Edit`, `Write` from `tools` and add `tools: Read, Grep, Glob`
7. `nickname_candidates` → no direct equivalent (Claude doesn't have this)
8. Add `tools` allowlist

---

## Porting Skills

Skills use the same `SKILL.md` format across all three platforms with minor differences. The core structure is portable.

### 4.1 Universal Skill Structure

```
<name>/
├── SKILL.md
├── scripts/
│   ├── analyze.py
│   └── helper.sh
└── references/
    ├── api.md
    └── style-guide.md
```

### 4.2 Frontmatter Portability

```yaml
---
name: python-performance-review
description: >
  Analyze Python code for runtime performance,
  algorithmic complexity, and optimization opportunities.
license: MIT
compatibility: python>=3.11
metadata:
  version: "1.2.0"
---
```

All three platforms recognize:
- `name` (required) — lowercase-kebab, must match directory name
- `description` (required) — max 1024 chars
- `license` (optional)
- `compatibility` (optional)
- `metadata` (optional, string-to-string map)

**Portable skills** need no changes to `SKILL.md` or the directory structure. Only the *location* changes:

### 4.3 Skill Location Mapping

| Platform | Location |
|---|---|
| OpenCode | `.opencode/skills/<name>/SKILL.md` or `~/.config/opencode/skills/<name>/SKILL.md` |
| Claude Code | `.claude/skills/<name>/SKILL.md` or `~/.claude/skills/<name>/SKILL.md` |
| OpenAI Codex | `.agents/skills/<name>/SKILL.md` or `~/.agents/skills/<name>/SKILL.md` |

All three also support cross-compatible locations:
- `.claude/skills/<name>/SKILL.md` (loaded by Claude Code natively, and by OpenCode/Codex for compat)
- `.agents/skills/<name>/SKILL.md` (loaded by Codex natively, and by OpenCode/Claude Code for compat)

**Recommendation for portability:** Place skills under `.agents/skills/<name>/SKILL.md` — this works on all three platforms today.

### 4.4 Codex-Specific: agents/openai.yaml

Codex supports an optional `agents/openai.yaml` metadata file for UI presentation. This is ignored by OpenCode and Claude Code:

```yaml
interface:
  display_name: "Performance Review"
  short_description: "Analyze Python code performance"
  icon_small: "./assets/small-logo.svg"
  brand_color: "#3B82F6"

policy:
  allow_implicit_invocation: true
```

When porting **from** Codex to other platforms, omit this file (it's ignored). When porting **to** Codex, you may optionally add it.

### 4.5 OpenCode-Specific: Permission Overrides

OpenCode supports per-skill permission overrides in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

Claude Code and Codex handle skill permissions through their respective tool/permission models instead. When porting **from** OpenCode, convert skill-level permission rules to:
- **Claude Code:** `permissions.deny` in settings or subagent frontmatter
- **Codex:** `[[skills.config]]` entries in `~/.codex/config.toml` with `enabled = false`

---

## Porting Permissions and Tool Restrictions

Each platform handles permissions differently:

| Concept | OpenCode | Claude Code | Codex |
|---|---|---|---|
| **Model** | `permission` dict with allow/ask/deny per tool category | `tools` allowlist or `disallowedTools` denylist | `sandbox_mode` (enum: read-only, workspace-write, etc.) |
| **Granularity** | Tool category level (edit, bash, read, etc.) + bash command globs | Individual tool level + bash command patterns | Sandbox level; hooks for pre-validation |
| **Bash restrictions** | Glob patterns on command names | Permission mode (auto, acceptEdits, etc.) + hooks | Hooks / pre-validation scripts |
| **File edits** | `edit: allow/ask/deny` | `tools: Edit, Write` (include or omit) | `sandbox_mode` controls write access |
| **Wildcard support** | Yes, via `*` | Yes, via glob patterns | Yes, via `mcp__*` patterns |

### Conversion table for common permission patterns

| Intended behavior | OpenCode | Claude Code | Codex |
|---|---|---|---|
| Read-only agent | `permission: { edit: deny, bash: deny }` | `tools: Read, Grep, Glob` | `sandbox_mode = "read-only"` |
| Read + Bash (no edits) | `permission: { edit: deny, bash: allow }` | `tools: Read, Grep, Glob, Bash` | `sandbox_mode = "read-only"` (Bash is still available for reads) |
| Full access | No permissions set (all inherit) | No `tools` set (all tools) | `sandbox_mode = "workspace-write"` (default) |
| Allow git, deny other bash | `permission: { bash: { "*": "deny", "git *": "allow" } }` | Use `permissionMode: auto` or hooks | Use hooks (PreToolUse command) |
| Deny a single tool | `tools: { write: false }` (deprecated) | `disallowedTools: Write` | Not directly supported; use sandbox mode |

---

## Porting AGENTS.md

Codex uses a cascading `AGENTS.md` hierarchy that doesn't have a direct equivalent in OpenCode or Claude Code.

### Codex AGENTS.md cascade

```
~/.codex/AGENTS.md              ← Global developer habits (lowest priority)
<project>/AGENTS.md             ← Project architecture & standards
<project>/<subdir>/AGENTS.override.md  ← Localized constraints (highest priority)
```

### Porting Codex AGENTS.md to OpenCode/Claude Code

**Codex AGENTS.md** serves as a persistent system prompt layer. In OpenCode/Claude Code, this content should be distributed across:

| Codex AGENTS.md content | OpenCode destination | Claude Code destination |
|---|---|---|
| Global developer habits | `~/.config/opencode/rules/` or global agent prompt | `~/.claude/CLAUDE.md` |
| Project architecture & standards | Project root `AGENTS.md` | Project root `CLAUDE.md` |
| Directory-level constraints | Subdirectory `AGENTS.md` | Subdirectory `CLAUDE.md` or `CLAUDE.local.md` |

### Porting to Codex AGENTS.md from OpenCode/Claude Code

When moving **to** Codex:
1. Take your project-level `AGENTS.md` or `CLAUDE.md` content and place it in `AGENTS.md` at the project root
2. Organize into sections matching Codex conventions:
   - Project context & technical stack
   - Engineering & architecture conventions
   - Environment & execution commands
   - Operational guardrails & constraints
   - Definition of Done
3. Keep under ~15 KB (Codex's 32 KiB discovery limit)
4. Add directory-level `AGENTS.override.md` files for scoped rules

---

## Platform-Specific Frontmatter Field Maps

### 7.1 Agent Frontmatter: Claude Code <-> OpenCode

| Claude Code field | OpenCode field | Notes |
|---|---|---|
| `name` | (filename) | OpenCode uses filename; Claude uses `name` field |
| `description` | `description` | Same purpose |
| `tools` | `permission` | Allowlist vs. deny-model |
| `disallowedTools` | `permission` (deny entries) | Same intent, different syntax |
| `model` | `model` | Claude uses aliases; OpenCode uses provider/model-id |
| `permissionMode` | `permission` (per-tool allow/ask/deny) | Different model |
| `maxTurns` | `steps` | Same concept |
| `mcpServers` | `mcp_servers` (in `opencode.json`) | Same purpose |
| `skills` | (skill load via `skill` tool) | Claude preloads; OpenCode lazy-loads |
| `memory` | Not supported | No equivalent |
| `effort` | `reasoningEffort` (pass-through) | Similar concept |
| `background` | Not supported | No equivalent |
| `hooks` | Not supported | No equivalent |

### 7.2 Agent Frontmatter: Codex TOML <-> OpenCode

| Codex TOML field | OpenCode field | Notes |
|---|---|---|
| `name` | (filename) | Codex uses `name` field; OpenCode uses filename |
| `description` | `description` | Same |
| `developer_instructions` | (body) | Body of markdown file |
| `model` | `model` | Codex uses model ID; OpenCode uses provider/model-id |
| `model_reasoning_effort` | `reasoningEffort` (pass-through) | Pass-through to provider |
| `sandbox_mode` | `permission` | Enum vs. granular permissions |
| `nickname_candidates` | Not supported | No equivalent |
| `mcp_servers` | `mcp_servers` (in `opencode.json`) | Same concept |

### 7.3 Agent Frontmatter: Codex TOML <-> Claude Code

| Codex TOML field | Claude Code field | Notes |
|---|---|---|
| `name` | `name` | Underscores vs. hyphens |
| `description` | `description` | Same |
| `developer_instructions` | (body) | Body of markdown file |
| `model` | `model` | Codex model ID vs. Claude alias |
| `model_reasoning_effort` | `effort` | `high` -> `high`, etc. |
| `sandbox_mode` | `tools` / `disallowedTools` | Enum -> allowlist/denylist |
| `nickname_candidates` | Not supported | No equivalent |
| `mcp_servers` | `mcpServers` | Same concept |

---

## Dependency and Invocation Patterns

### 8.1 Skill referencing another skill

**Not supported** directly on any platform. Skills are independently loaded by the agent. To create a dependency:

1. **Name the dependency in the skill description** — e.g., "This skill requires the `database-setup` skill to be loaded first."
2. **Use scripts** — invoke the dependent skill's scripts directly as subprocesses
3. **Agent-level orchestration** — the agent decides which skills to load; instruction the agent in the skill body to load the dependency first

### 8.2 Agent invoking a skill

All three platforms support this through their respective tool systems:

| Platform | Agent invokes skill via |
|---|---|
| OpenCode | `skill` tool (agent calls `skill({ name: "..." })`) |
| Claude Code | `Skill` tool (agent discovers and loads skills) |
| Codex | `$skill-name` inline mention or implicit match by description |

### 8.3 Agent spawning another agent

| Platform | Mechanism |
|---|---|
| OpenCode | Primary agent uses `task` tool to spawn a subagent |
| Claude Code | Agent uses `Agent` tool to spawn a named subagent |
| Codex | Main loop delegates to skills; `spawn_agents_on_csv` for batch parallel work |

---

## Verification Checklist

After porting between platforms, verify:

### Directory structure
- [ ] Agent/skill files are in the correct location for the target platform
- [ ] `SKILL.md` is spelled in ALL CAPS with `.md` extension
- [ ] Directory name matches `name` field (skills) or convention (agents)

### Frontmatter
- [ ] All required fields are present (`name` + `description` for skills; platform-specific for agents)
- [ ] No unsupported fields that cause silent failures
- [ ] `name` follows target platform's naming rules (kebab-case, lengths, etc.)
- [ ] Model identifiers use the target platform's format (aliases vs. provider/model-id)

### Permissions
- [ ] Permission model converted correctly (allowlist vs. deny-list vs. sandbox enum)
- [ ] No overly permissive defaults that expose unwanted access

### Invocation
- [ ] Invocation mechanism works (`@mention`, `$skill`, or automatic delegation)
- [ ] Description is specific enough for implicit matching on the target platform

### Scripts & references
- [ ] Script paths are valid (relative to skill directory)
- [ ] Reference paths use portable relative references (not absolute or platform-specific)

### Testing
- [ ] Agent/skill loads without errors on target platform
- [ ] Expected behavior matches source platform behavior
- [ ] Permission restrictions work as intended

## Related Documents

- [Best Practices for AGENTS.md Files](agents-best-practices.md) — architecture, sizing, and production templates for AGENTS.md
- [OpenCode Agents](opencode-agents.md) — configuring and using agents in OpenCode
- [Claude Code Subagents](claude-code-subagents.md) — creating and managing subagents in Claude Code
- [Codex Subagents](codex-subagents.md) — subagent workflows and custom agents in OpenAI Codex
- [Codex Agent Conversion](codex-agent-conversion.md) — mapping OpenCode agents to Codex-compatible structure
