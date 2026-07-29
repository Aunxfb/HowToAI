---
title: OpenCode Official Documentation References
description: Central index of OpenCode official documentation links for AI agents and developers configuring OpenCode agents, skills, tools, and permissions.
status: active
tags: [opencode, documentation, references, index, configuration]
last_verified: 2026-07-29
layer: hot
applies_to: opencode configuration
---

# OpenCode Official Documentation References

## Overview

Central index of OpenCode (by Zen.ai) official documentation. AI agents should use these links to understand system architecture, design patterns, and best practices for creating personas, skills, and custom tools.

## Core Documentation

- **Main Documentation Hub**: [https://opencode.ai/docs](https://opencode.ai/docs) — general overview, installation, and project initialization.
- **Models & Providers**: [https://opencode.ai/docs/models/](https://opencode.ai/docs/models/) — configuring Zen.ai models and external LLM providers in `opencode.json`.

## Agents and Personas

- **Agent Definitions**: [https://opencode.ai/docs/agents/](https://opencode.ai/docs/agents/) — use `.opencode/agents/<name>.md` with frontmatter for `mode` (primary/subagent) and tool permissions.
- **Format**: concise system instructions with headings separating "Capabilities" and "Constraints."

## Skills and Custom Tools

- **Skills System**: [https://opencode.ai/docs/skills/](https://opencode.ai/docs/skills/) — each skill requires a `.opencode/skills/<name>/SKILL.md` file. Keep `description` in frontmatter between 1-1024 characters.
- **Custom Tools**: [https://opencode.ai/docs/custom-tools/](https://opencode.ai/docs/custom-tools/) — defining how the agent interacts with external APIs or local scripts.
- **Built-in Tools**: [https://opencode.ai/docs/tools/](https://opencode.ai/docs/tools/) — native capabilities like filesystem access and terminal execution.

## Connectivity and Integration

- **MCP Servers**: [https://opencode.ai/docs/mcp-servers/](https://opencode.ai/docs/mcp-servers/) — Model Context Protocol (MCP) integration for external data sources.

## Security and Governance

- **Permissions Framework**: [https://opencode.ai/docs/permissions/](https://opencode.ai/docs/permissions/) — define granular `allow`/`ask`/`deny` rules in `opencode.json`.

## Related Documents

- [OpenCode Best Practices](../misc/opencode-best-practices.md) — optimal formats and constraints for OpenCode configurations.
- [Reference Standards](../misc/reference-standards.md) — the conventions this document follows.
