---
title: Codex Workspace Best Practices
description: Optimization blueprint for configuring OpenAI Codex workspace personas, execution guardrails, file inheritance rules, and AGENTS.md cascade hierarchy.
status: active
tags: [codex, workspace, best-practices, agents, configuration]
last_verified: 2026-07-29
layer: hot
applies_to: openai codex workspace configuration
---

# Codex Workspace Best Practices

## Overview

Optimization blueprint for configuring OpenAI Codex workspace personas, execution guardrails, and file inheritance rules. Covers document length metrics, file cascade architecture, and the five core design best practices.

## Background

**Key terms:** AGENTS.md — the primary rule file Codex reads at project root; AGENTS.override.md — per-directory override files for localized constraints.

**Context:** Codex merges instructions across multiple folder levels. Understanding the cascade hierarchy is essential to avoid rule conflicts and token waste.

## Document Scope and Length Metrics

### The 32 KiB Horizon

Codex scans up to a strict hard limit of **32 KiB** across its discovery path. Exceeding this cuts off rules abruptly.

### Target Length Metrics

- **Optimal Payload Size**: 8 KB – 15 KB (roughly 1,500 to 3,500 words).
- **Context Conservation**: keeping rules files lean saves context tokens for codebase reasoning.
- **Growth Buffer**: cap baseline documentation at ~12 KB to leave room for local overrides.

## File Architecture and Cascade Path

Codex merges instructions across multiple layers:

```
~/.codex/AGENTS.md                — Global developer habits (lowest priority)
+-- [Project Root]/AGENTS.md      — Project architecture and style standards
+-- [Sub-Folder]/AGENTS.override.md — Isolated constraints (highest priority)
```

1. **Global Level (`~/.codex/AGENTS.md`)**: permanent personal habits across all projects.
2. **Project Root (`/AGENTS.md`)**: main repository constraints — tech stack, directory layout, linting.
3. **Directory Level (`/[folder]/AGENTS.override.md`)**: localized overrides for sensitive folders.

## Core Design Best Practices

### Enforce Concrete Boundaries Over Abstract Advice

- **Vague**: "Write clean, performant React components."
- **Deterministic**: "Write components using functional React 19 style. Avoid type assertions (`as unknown`) and the `any` keyword."

### Establish a Strict Definition of Done (DoD)

Before signaling completion, Codex must:

1. Confirm the project compiles using `pnpm build`.
2. Run `pnpm lint` and resolve new warnings.
3. Update or create corresponding unit tests.

### Offload Context Using Documentation Anchors

Use clear pointers instead of copying documentation into rules files:

> "When editing database tables, follow the design principles in `docs/DB_STANDARDS.md` before creating migrations."

### Isolate Tool and File Permissions

Prevent modification of legacy files with explicit read/write rules:

> "You are strictly read-only within `/infra/terraform/`. Read for context but do not modify."

### Prevent Token Bloat With Code Signatures

Include only basic signatures or type outlines instead of pasting entire multi-line implementations.

## Related Documents

- [Reference Standards](../misc/reference-standards.md) — the conventions this document follows.
- [OpenCode Best Practices](../misc/opencode-best-practices.md) — comparable practices for OpenCode configuration.
