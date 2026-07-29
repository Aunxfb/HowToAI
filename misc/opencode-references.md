# OpenCode Official Documentation References

This document serves as a central index for OpenCode (by Zen.ai) official documentation. AI agents should refer to these links to understand the system architecture, design patterns, and best practices for creating personas, skills, and custom tools.

## 🛠 Core Documentation
- **Main Documentation Hub**: [https://opencode.ai/docs](https://opencode.ai/docs)
  - *Purpose*: General overview, installation, and project initialization (`/init`).
- **Models & Providers**: [https://opencode.ai/docs/models/](https://opencode.ai/docs/models/)
  - *Purpose*: Reference for configuring Zen.ai models and external LLM providers in `opencode.json`.

## 🤖 Agents & Personas
- **Agent Definitions**: [https://opencode.ai/docs/agents/](https://opencode.ai/docs/agents/)
  - *Best Practices*: Use `.opencode/agents/<name>.md`. Include frontmatter for `mode` (primary/subagent) and specific tool permissions.
  - *Format*: Maintain concise system instructions; use headings to separate "Capabilities" and "Constraints."

## 🔧 Skills & Custom Tools
- **Skills System**: [https://opencode.ai/docs/skills/](https://opencode.ai/docs/skills/)
  - *Design Rule*: Each skill requires a `.opencode/skills/<name>/SKILL.md` file.
  - *Ideal Length*: Keep the `description` in frontmatter under 200 characters for optimal discovery.
- **Custom Tools**: [https://opencode.ai/docs/custom-tools/](https://opencode.ai/docs/custom-tools/)
  - *Purpose*: Logic for defining how the agent interacts with external APIs or local scripts.
- **Built-in Tools**: [https://opencode.ai/docs/tools/](https://opencode.ai/docs/tools/)
  - *Purpose*: Reference for native capabilities like filesystem access and terminal execution.

## 🌐 Connectivity & Integration
- **MCP Servers**: [https://opencode.ai/docs/mcp-servers/](https://opencode.ai/docs/mcp-servers/)
  - *Purpose*: Integration guide for the Model Context Protocol (MCP) to connect external data sources.

## 🛡 Security & Governance
- **Permissions Framework**: [https://opencode.ai/docs/permissions/](https://opencode.ai/docs/permissions/)
  - *Best Practices*: Define granular `allow`/`ask`/`deny` rules in `opencode.json` to ensure safe terminal execution.

---
*Note: When designing for OpenCode, prioritize modularity by placing specific logic in `.opencode/` subdirectories to ensure configuration is portable and version-controlled.*
