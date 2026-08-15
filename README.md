# HowToAI

A curated collection of references, guides, patterns, and best practices for Applied AI — covering agent orchestration, skill authoring, prompt optimization, and security tooling across multiple AI coding platforms (OpenAI Codex, OpenCode, Claude Code, Nanobot).

AI agents: see `AGENTS.md` for the hot → warm → cold loading protocol. This file is the index; read it before fetching any reference.

## Directory Structure

Layer column shows loading intent: 🔥 always in context, ☀️ task-loaded, ❄️ fetched via links. Sizes are guidance, not limits. See `AGENTS.md` for the loading protocol.

### agents/

Agent-level configuration, subagents, and cross-platform porting.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [agents-best-practices.md](agents/agents-best-practices.md) | ☀️ | Best Practices for AGENTS.md Files | Reference guide for designing high-performance AGENTS.md files that guide AI coding agents with progressive disclosure, optimal sizing, and production-ready templates. For developers and teams using AI coding tools. |
| [claude-code-subagents-configure.md](agents/claude-code-subagents-configure.md) | ❄️ | Claude Code Subagent Configuration | Complete reference for configuring Claude Code subagents — scope, file format, frontmatter fields, models, capabilities, permissions, and hooks. |
| [claude-code-subagents-examples.md](agents/claude-code-subagents-examples.md) | ☀️ | Claude Code Subagent Examples | Ready-to-use subagent configurations for Claude Code — code reviewer, debugger, data scientist, and database query validator with hooks. |
| [claude-code-subagents.md](agents/claude-code-subagents.md) | ☀️ | Claude Code Subagents | Overview of Claude Code subagent system — built-in agents, quickstart, usage patterns, workflows, and forking. |
| [codex-agent-conversion.md](agents/codex-agent-conversion.md) | ☀️ | Codex Agent Conversion | Maps OpenCode agent and subagent configurations to OpenAI Codex-compatible structure, covering primary agents, subagents, permissions, and orchestration patterns. |
| [codex-subagents.md](agents/codex-subagents.md) | ☀️ | Codex Subagents | Reference for subagent workflows in OpenAI Codex, including custom agents, model selection, sandbox controls, and batch processing patterns. |
| [nanobot-personas-guide.md](agents/nanobot-personas-guide.md) | ☀️ | Nanobot Persona Engineering Guide | How to build production-grade, instruction-drift-resistant workspace personas for the HKUDS/nanobot framework. |
| [opencode-agents-config.md](agents/opencode-agents-config.md) | ❄️ | OpenCode Agent Configuration | Complete reference for configuring agents in OpenCode — JSON config, markdown agents, permissions, models, and all available options. |
| [opencode-agents.md](agents/opencode-agents.md) | ☀️ | Agents | Overview of OpenCode agent system — built-in agents, types, usage, creating agents, use cases, and example configurations. |
| [opencode-claude-codex-porting.md](agents/opencode-claude-codex-porting.md) | ☀️ | Porting Agents and Skills Between Harnesses | Field guide for migrating agent and skill definitions between OpenCode, Claude Code, and OpenAI Codex. For developers maintaining multi-platform AI coding configurations. |

### skills/

Skill (SKILL.md) authoring, best practices, and platform-specific features.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [nanobot-skills.md](skills/nanobot-skills.md) | ☀️ | Nanobot Skills | Covers nanobot-specific skill features including the SkillsLoader, MCP server pairing, metadata payload format, runtime support matrix, and skill configuration. |
| [skills-best-practices.md](skills/skills-best-practices.md) | ❄️ | Skills Best Practices for AI Assistants | Guidelines for creating, reviewing, and maintaining Skills that make AI assistants more reliable at repeatable tasks through focused instructions and clear workflow guidance. |

### ai-tooling/

Tooling for AI agent execution: deterministic scripts and MCP server best practices.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [ai-scripting-best-practices.md](ai-tooling/ai-scripting-best-practices.md) | ☀️ | Best Practices for Writing AI-Optimized Scripts | Architectural and stylistic principles for writing code optimized for execution by AI agents and LLM code interpreters. |
| [mcp-server-best-practices-deep-reference.md](ai-tooling/mcp-server-best-practices-deep-reference.md) | ❄️ | MCP Server Best Practices Deep Reference | Evidence base, protocol detail, templates, and evaluation guidance for architects and AI engineers building reliable and secure Model Context Protocol servers. |
| [mcp-server-best-practices.md](ai-tooling/mcp-server-best-practices.md) | ☀️ | MCP Server Best Practices | Practical rules and release checks for designing reliable, efficient, secure, and agent-usable Model Context Protocol servers. |

### harnesses/

Platform-specific best practices, workspace configuration, and official documentation indexes.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [codex-workspace-best-practices.md](harnesses/codex-workspace-best-practices.md) | 🔥 | Codex Workspace Best Practices | Optimization blueprint for configuring OpenAI Codex workspace personas, execution guardrails, file inheritance rules, and AGENTS.md cascade hierarchy. |
| [nanobot-best-practices.md](harnesses/nanobot-best-practices.md) | 🔥 | Nanobot Best Practices for AI Customization | Practical guide for designing, customizing, and operating high-quality nanobot agents using the HKUDS framework, covering file-based cognition, memory, skills, and security. |
| [opencode-best-practices.md](harnesses/opencode-best-practices.md) | 🔥 | OpenCode Best Practices Guide | Optimal formats, structures, and constraints for designing OpenCode configurations, agents, and skills to maximize efficiency and reduce token waste. |
| [opencode-references.md](harnesses/opencode-references.md) | 🔥 | OpenCode Official Documentation References | Central index of OpenCode official documentation links for AI agents and developers configuring OpenCode agents, skills, tools, and permissions. |

### documentation/

Repository documentation standards and reference-file templates.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [reference-standards.md](documentation/reference-standards.md) | ☀️ | Reference File Standards | Defines the consistent structure, frontmatter, writing style, and quality checklist for all reference documents in this repository, serving both human readers and AI coding agents. |

### security/

Security testing and vulnerability assessment references.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [ai-vs-dast-comparison-deep-dives.md](security/ai-vs-dast-comparison-deep-dives.md) | ❄️ | AI vs DAST Comparison: Vulnerability Deep Dives | Per-vulnerability-type descriptions for all 30 AI-delegated and DAST-delegated categories, with examples, reasoning, and validation steps. |
| [ai-vs-dast-comparison-evidence.md](security/ai-vs-dast-comparison-evidence.md) | ❄️ | AI vs DAST Comparison: Evidence Base and References | Complete evidence base supporting the AI vs traditional DAST scanner delegation model, including AI cyber-agent studies, OWASP guidance, DAST scanner documentation, and citation mapping. |
| [ai-vs-dast-comparison.md](security/ai-vs-dast-comparison.md) | ☀️ | AI vs Traditional DAST Scanner Vulnerability Delegation | Decision framework for delegating vulnerability testing between AI and traditional DAST scanners, with delegation matrix, recommended workflow, and counter-evidence. |
| [ai-vs-sast-comparison-evidence.md](security/ai-vs-sast-comparison-evidence.md) | ❄️ | AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence | Supporting and contradictory evidence, all 13 references with citations, and claim mapping for the AI vs SAST/SCA/secret scanning delegation model. |
| [ai-vs-sast-comparison.md](security/ai-vs-sast-comparison.md) | ☀️ | AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review | Defines when to delegate security review tasks to AI-assisted code review, SAST, SCA, secret scanners, or humans, with decision matrices and operating principles. |

### design/

Design and architecture guidance for AI systems.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [llm-budget-friendly-design-appendix.md](design/llm-budget-friendly-design-appendix.md) | ❄️ | LLM Budget-Friendly Design Appendix | Practical engineering procedure for designing AI frameworks — state machine first, task decomposition, operation classification, LLM eligibility, evaluation, and avoiding overengineering. |
| [llm-budget-friendly-design-arch.md](design/llm-budget-friendly-design-arch.md) | ☀️ | LLM Budget-Friendly Reference Architecture | Reference architecture for budget-friendly AI frameworks — system overview, project structure, runtime loop, context loading, multi-agent communication, failure handling, and model replacement. |
| [llm-budget-friendly-design-operating.md](design/llm-budget-friendly-design-operating.md) | ☀️ | LLM Budget-Friendly Design — Operating | Operations and governance principles for workflow state separation, recoverability, token budgeting, framework complexity, and preferring reversible AI actions. |
| [llm-budget-friendly-design-patterns.md](design/llm-budget-friendly-design-patterns.md) | ☀️ | LLM Budget-Friendly Design Patterns | Detailed patterns and implementation guidance for externalizing memory, file-based state passing, context boundary splitting, skills design, and interfaces optimized for AI consumption. |
| [llm-budget-friendly-design-templates.md](design/llm-budget-friendly-design-templates.md) | ☀️ | LLM Budget-Friendly Design Templates | Design guidance and YAML templates for AI framework components — state models, phase contracts, skills, agents, prompts, and supporting template examples. |
| [llm-budget-friendly-design.md](design/llm-budget-friendly-design.md) | ☀️ | LLM Budget-Friendly Design | Core philosophy and actionable principles for designing efficient, reliable, and scalable AI systems that minimize unnecessary LLM usage. |

### webdev/

Building web applications with AI coding agents and open-source tooling.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [ai-web-development-open-tooling.md](webdev/ai-web-development-open-tooling.md) | ☀️ | AI Web Development with Open-Source Tooling | How developers can build web applications with AI using open-source, self-hosted tools — bridging the text-to-UI gap and the "AI can't see the rendered page" gap with browser automation, browser MCP servers, screenshots, and open coding agents. |

### misc/

Cross-cutting topics not covered by the other sections.

| File | Layer | Title | Description |
|------|-------|-------|-------------|
| [ai-effective-readmes-case-study.md](misc/ai-effective-readmes-case-study.md) | ❄️ | AI-Effective README Reference -- Case Studies | Comparative, line-by-line dissection of three real READMEs — HowToAI (non-code knowledge base), uv (code repo), and Claude Cookbooks (docs site) — read through the lens of AI consumption, with cross-case patterns and before/after rewrites. |
| [ai-effective-readmes.md](misc/ai-effective-readmes.md) | ☀️ | AI-Effective README Reference | Rules for making README.md files effective for AI agents — dual-audience writing, commands as ground truth, index patterns for non-code repos, and AI-invisible media pitfalls, with a copy-safe template and validation. |
| [ai-friendly-planning-evidence.md](misc/ai-friendly-planning-evidence.md) | ❄️ | AI-Friendly Plan Authoring and Execution -- Evidence | Claim-by-claim verification of the seven authoring properties and five execution rules, supporting and contradictory evidence, and all 29 references with citation mapping. |
| [ai-friendly-planning.md](misc/ai-friendly-planning.md) | ☀️ | AI-Friendly Plan Authoring and Execution | Standards for drafting implementation plans that AI agents can execute autonomously and incrementally, and the rules agents must follow when executing them. Backed by published research and industry engineering practice. |

## Reference Relationships
Warm overviews branch into their companions — deep references and related guides — regardless of layer. Files that no overview references appear standalone.
### agents/
```
├── [Best Practices for AGENTS.md Files](agents/agents-best-practices.md) (☀️)
├── [Claude Code Subagent Examples](agents/claude-code-subagents-examples.md) (☀️)
│   └── [Claude Code Subagent Configuration](agents/claude-code-subagents-configure.md) (❄️)
├── [Claude Code Subagents](agents/claude-code-subagents.md) (☀️)
│   └── [Claude Code Subagent Configuration](agents/claude-code-subagents-configure.md) (❄️)
├── [Codex Agent Conversion](agents/codex-agent-conversion.md) (☀️)
├── [Codex Subagents](agents/codex-subagents.md) (☀️)
├── [Nanobot Persona Engineering Guide](agents/nanobot-personas-guide.md) (☀️)
├── [Agents](agents/opencode-agents.md) (☀️)
│   └── [OpenCode Agent Configuration](agents/opencode-agents-config.md) (❄️)
└── [Porting Agents and Skills Between Harnesses](agents/opencode-claude-codex-porting.md) (☀️)
```
### skills/
```
└── [Nanobot Skills](skills/nanobot-skills.md) (☀️)
    └── [Skills Best Practices for AI Assistants](skills/skills-best-practices.md) (❄️)
```
### ai-tooling/
```
├── [Best Practices for Writing AI-Optimized Scripts](ai-tooling/ai-scripting-best-practices.md) (☀️)
└── [MCP Server Best Practices](ai-tooling/mcp-server-best-practices.md) (☀️)
    └── [MCP Server Best Practices Deep Reference](ai-tooling/mcp-server-best-practices-deep-reference.md) (❄️)
```
### harnesses/
```
├── [Codex Workspace Best Practices](harnesses/codex-workspace-best-practices.md) (🔥)
├── [Nanobot Best Practices for AI Customization](harnesses/nanobot-best-practices.md) (🔥)
├── [OpenCode Best Practices Guide](harnesses/opencode-best-practices.md) (🔥)
└── [OpenCode Official Documentation References](harnesses/opencode-references.md) (🔥)
```
### documentation/
```
└── [Reference File Standards](documentation/reference-standards.md) (☀️)
```
### security/
```
├── [AI vs Traditional DAST Scanner Vulnerability Delegation](security/ai-vs-dast-comparison.md) (☀️)
│   ├── [AI vs DAST Comparison: Vulnerability Deep Dives](security/ai-vs-dast-comparison-deep-dives.md) (❄️)
│   └── [AI vs DAST Comparison: Evidence Base and References](security/ai-vs-dast-comparison-evidence.md) (❄️)
└── [AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review](security/ai-vs-sast-comparison.md) (☀️)
    └── [AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence](security/ai-vs-sast-comparison-evidence.md) (❄️)
```
### design/
```
└── [LLM Budget-Friendly Design](design/llm-budget-friendly-design.md) (☀️)
    ├── [LLM Budget-Friendly Design Appendix](design/llm-budget-friendly-design-appendix.md) (❄️)
    ├── [LLM Budget-Friendly Reference Architecture](design/llm-budget-friendly-design-arch.md) (☀️)
    ├── [LLM Budget-Friendly Design — Operating](design/llm-budget-friendly-design-operating.md) (☀️)
    ├── [LLM Budget-Friendly Design Patterns](design/llm-budget-friendly-design-patterns.md) (☀️)
    └── [LLM Budget-Friendly Design Templates](design/llm-budget-friendly-design-templates.md) (☀️)
```
### webdev/
```
└── [AI Web Development with Open-Source Tooling](webdev/ai-web-development-open-tooling.md) (☀️)
```
### misc/
```
├── [AI-Effective README Reference](misc/ai-effective-readmes.md) (☀️)
│   └── [AI-Effective README Reference -- Case Studies](misc/ai-effective-readmes-case-study.md) (❄️)
└── [AI-Friendly Plan Authoring and Execution](misc/ai-friendly-planning.md) (☀️)
    └── [AI-Friendly Plan Authoring and Execution -- Evidence](misc/ai-friendly-planning-evidence.md) (❄️)
```
