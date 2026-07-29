---
title: Nanobot Best Practices for AI Customization
description: Practical guide for designing, customizing, and operating high-quality nanobot agents using the HKUDS framework, covering file-based cognition, memory, skills, and security.
status: active
tags: [nanobot, agents, best-practices, customization, hkuds]
last_verified: 2026-07-29
layer: warm
applies_to: nanobot agent framework
---

# Nanobot Best Practices for AI Customization

## Overview

Practical guide for designing, customizing, and operating high-quality nanobot agents using the HKUDS framework. Covers the file-first cognitive architecture, system prompt optimization, memory management, skills engineering, and security guardrails.

## Architecture Philosophy: File-Based Cognition

Nanobot is an ultra-lightweight personal AI agent framework (~4,000 lines of Python core). It delegates agent behavior to a **file-first cognitive architecture** in your workspace, using a central `config.json` strictly for routing APIs, chat channels (Telegram, Discord, Slack, WebUI), and tool sandboxing.

The best nanobots are:

- **Narrowly scoped**: driven by concise, highly declarative markdown files.
- **Context-disciplined**: using on-demand skill loading to prevent token bloat.
- **Operationally isolated**: utilizing per-session execution tracks so parallel requests do not overlap.

## System Prompt Equation

At every chat turn, `build_system_prompt()` dynamically stitches together core workspace markdown files to create the agent's context. Keeping these core files lean is critical to avoid token inflation and instruction drift.

### Workspace File Reference Guide

| File | Target Size | Role |
|---|---|---|
| `AGENTS.md` | 300–400 words | Active runtime manual: tool execution rules, multi-agent delegation, background loops |
| `SOUL.md` | 250–450 words | Identity and persona: character traits, communication style, behavioral values |
| `USER.md` | 150–300 words | User profile and environment: OS, coding environment, preferences |
| `HEARTBEAT.md` | 200–350 words | Scheduled automation: cron rules and periodic tasks |

- **Protect the core file layer**: never inject fluid facts or temporary project updates here. Offload active summaries to `memory/MEMORY.md` or modularize workflows into `skills/`.

## Memory Best Practices

Nanobot splits memory into two pipelines:

1. **Raw Logs**: active turn interaction logs stream into `history.jsonl` or `memory/HISTORY.md`, hard-capped (typically last 50 entries up to 32k characters).
2. **Dream Loop**: background process reads raw log traces, runs pattern analysis, extracts durable insights, and consolidates them into `memory/MEMORY.md`.

- **Auto-Compaction**: let the engine handle micro-compaction. Set `memoryWindow` in `config.json` (e.g., 50) and let background coroutines manage token pressure.

## Skills Engineering

Do not write complex workflows into `AGENTS.md`. Use the native Skill System:

```
~/.nanobot/workspace/skills/
  └── stock-analysis/
      └── SKILL.md
```

### Best Practices for SKILL.md

- **Clear Frontmatter**: declare metadata for the `SkillsLoader` to catalog efficiently.
- **On-Demand Compounding**: set `always: false` for hyper-specific workflows. The full manual is only read into context when the agent triggers the skill.
- **Idempotent Tools**: guarantee repeated calls are safe. For destructive actions, mandate a dry-run block or use `ask_user` for confirmation.

## Configuration and Platform Fine-Tuning

### Multi-Provider Resiliency

Design a heterogeneous provider stack with fallback:

```json
"agents": {
  "defaults": {
    "model": "anthropic/claude-3-5-sonnet",
    "fallbackModel": "openai/gpt-4o-mini",
    "temperature": 0.3,
    "maxToolIterations": 20
  }
}
```

### Granular Channel Interface Controls

Fine-tune `channels` settings per platform. Turn progress indicators off for chat platforms to minimize spam while keeping them on for WebUI.

## Security and Isolation Guardrails

- **Isolate Pathing**: keep `"tools": { "restrictToWorkspace": true }` active in production.
- **Sandbox the Shell**: never run `nanobot gateway` as root. In multi-user setups, enforce sandboxing with Docker and restricted volume mappings.
- **Audit Traces**: monitor runtime session logs for overlapping tool calls or race conditions, especially with `HEARTBEAT.md` background loops.

## Anti-Patterns

- Monolithic prompt packing — shoving 2,000 lines into `AGENTS.md` instead of using on-demand Skills.
- Open-ended loop definitions — high `maxToolIterations` without strict stop criteria.
- Unprotected global inbound channels — enabling Telegram or Discord without populating `allowFrom`.
- Over-agentification — creating sub-agents for minor linear tasks a single model turn could solve directly.

## Related Documents

- [Reference Standards](../misc/reference-standards.md) — the conventions this document follows.
- [OpenCode Best Practices](../misc/opencode-best-practices.md) — comparable practices for OpenCode agents.
