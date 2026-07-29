# OpenCode Best Practices Guide

This guide outlines the optimal formats, structures, and constraints for designing OpenCode configurations, agents, and skills. Adhering to these practices ensures maximum efficiency, reduced token waste, and reliable agent behavior.

## 1. AGENTS.md (Project Rules)
The `AGENTS.md` file (or `CLAUDE.md` fallback) is the project-level system prompt.
- **Structure**: Use a "Table of Contents" approach, not an encyclopedia.
- **Ideal Length**: Under **~2,500 tokens**.
- **Content Strategy**: 
    - **Ruthless Deletion**: Do not include information the model can infer (e.g., "This is a TypeScript project"). 
    - **Focus**: Detail "hidden" knowledge: custom auth patterns, protected folders, or non-obvious build steps.
    - **Links**: Use `@filename` syntax to link to deeper context files (e.g., `@docs/standards.md`) to save context space.
- **Hierarchy**: In monorepos, use nested `AGENTS.md` files. The agent always prioritizes the one closest to the file it is editing.

## 2. SKILL.md (Custom Skills)
Skills are repeatable "knowledge modules" for complex tasks.
- **Format**: A folder named `skill-name/` containing a `SKILL.md` file.
- **Frontmatter**:
    - `name`: Max 64 characters, lowercase-kebab-case.
    - `description`: Max 1024 characters. **Critical**: Front-load trigger words for implicit matching.
- **Structure**:
    1. **Boundaries**: Define when *not* to use the skill.
    2. **Structural Overview**: Define core objects or entry points first.
    3. **Workflows**: Use step-by-step instructions rather than feature lists.
    4. **If/Then Rules**: Provide explicit decision logic for multi-path tasks.
- **Token Optimization**: Skills cost 0 tokens when idle. Full instructions only load when triggered.

## 3. Custom Tools (TypeScript/JavaScript)
Tools are functional extensions that allow the AI to execute code.
- **Location**: `.opencode/tools/` for local, `~/.config/opencode/tools/` for global.
- **Naming**: The filename determines the tool name. 
- **Type Safety**: Use the `tool()` helper from `@opencode-ai/plugin` for schema validation and description.
- **Multi-Language Support**: Use TypeScript for the tool *definition*, but the `execute()` function can invoke scripts in Python, Bash, or Rust.

## 4. config.json (Permissions & Settings)
- **Schema**: Always include `"$schema": "https://opencode.ai/config.json"` for IDE validation.
- **Permission Mapping**: 
    - Use `allow`, `ask`, or `deny`.
    - Use wildcards for groups of tools (e.g., `"deploy-*": "ask"`).
- **Formatters**: Disable by default; enable specifically for languages you want the agent to auto-clean (e.g., `"prettier": true`).

## 5. Generic Formatting Rules
- **Imperative Language**: Use commands like "Always run...", "Do not edit...", "Sort by...".
- **Avoid Placeholders**: Never leave `[Your text here]` or TODOs in `.opencode` files; these confuse the agent's logic.
- **Case Sensitivity**: Always name files exactly (e.g., `AGENTS.md`, `SKILL.md`).
- **YAML Frontmatter**: Must start on **Line 1** with `---`. Avoid using angle brackets `< >` inside YAML to prevent injection issues.