---
title: OpenCode Best Practices Guide
description: Optimal formats, structures, and constraints for designing OpenCode configurations, agents, and skills to maximize efficiency and reduce token waste.
status: active
tags: [opencode, best-practices, agents, skills, configuration]
last_verified: 2026-08-13
layer: hot
applies_to: opencode configuration files
---

# OpenCode Best Practices Guide

## Overview

Outlines the optimal formats, structures, and constraints for designing OpenCode configurations, agents, and skills. Adhering to these practices ensures maximum efficiency, reduced token waste, and reliable agent behavior.

## Configuration

### AGENTS.md (Project Rules)

The `AGENTS.md` file (or `CLAUDE.md` fallback) is the project-level system prompt.

- **Structure**: table of contents approach, not an encyclopedia.
- **Ideal Length**: under ~2,500 tokens.
- **Content Strategy**: include only hidden knowledge — custom auth patterns, protected folders, or non-obvious build steps. Use `@filename` syntax to link to deeper context files.
- **Hierarchy**: in monorepos, use nested `AGENTS.md` files. The agent prioritizes the one closest to the file it is editing.

### SKILL.md (Custom Skills)

Skills are repeatable knowledge modules for complex tasks.

- **Format**: a folder named `skill-name/` containing a `SKILL.md` file.
- **Frontmatter**: `name` (max 64 chars, kebab-case), `description` (max 1024 chars, front-load trigger words).
- **Structure**: boundaries → structural overview → workflows → if/then rules.
- **Token Optimization**: skills cost 0 tokens when idle. Full instructions only load when triggered.

### Custom Tools (TypeScript/JavaScript)

Tools are functional extensions that allow the AI to execute code.

- **Location**: `.opencode/tools/` for local, `~/.config/opencode/tools/` for global.
- **Naming**: filename determines the tool name.
- **Type Safety**: use the `tool()` helper from `@opencode-ai/plugin` for schema validation and descriptions.
- **Multi-Language Support**: TypeScript for definition; `execute()` can invoke Python, Bash, or Rust.

### Configuration File (Permissions and Settings)

- **Schema**: always include `"$schema": "https://opencode.ai/config.json"` for IDE validation.
- **Permission Mapping**: use `allow`, `ask`, or `deny`. Use wildcards for groups (e.g., `"deploy-*": "ask"`).
- **Formatters**: disable by default; enable specifically for languages you want auto-cleaned.
