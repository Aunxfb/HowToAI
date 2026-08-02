# HowToAI

A curated collection of references, guides, patterns, and best practices for Applied AI — covering agent orchestration, skill authoring, prompt optimization, and security tooling across multiple AI coding platforms (OpenAI Codex, OpenCode, Claude Code, Nanobot).

AI agents: see `AGENTS.md` for the hot → warm → cold loading protocol. This file is the index; read it before fetching any reference.

## Directory Structure

### agents/

Agent-level configuration, subagents, and cross-platform porting.

| File | Title | Description |
|------|-------|-------------|
| [agents-best-practices.md](agents/agents-best-practices.md) | Best Practices for AGENTS.md Files | Reference guide for designing high-performance AGENTS.md files that guide AI coding agents with progressive disclosure, optimal sizing, and production-ready templates. For developers and teams usin... |
| [claude-code-subagents-configure.md](agents/claude-code-subagents-configure.md) | Claude Code Subagent Configuration | Complete reference for configuring Claude Code subagents — scope, file format, frontmatter fields, models, capabilities, permissions, and hooks. |
| [claude-code-subagents-examples.md](agents/claude-code-subagents-examples.md) | Claude Code Subagent Examples | Ready-to-use subagent configurations for Claude Code — code reviewer, debugger, data scientist, and database query validator with hooks. |
| [claude-code-subagents.md](agents/claude-code-subagents.md) | Claude Code Subagents | Overview of Claude Code subagent system — built-in agents, quickstart, usage patterns, workflows, and forking. |
| [codex-agent-conversion.md](agents/codex-agent-conversion.md) | Codex Agent Conversion | Maps OpenCode agent and subagent configurations to OpenAI Codex-compatible structure, covering primary agents, subagents, permissions, and orchestration patterns. |
| [codex-subagents.md](agents/codex-subagents.md) | Codex Subagents | Reference for subagent workflows in OpenAI Codex, including custom agents, model selection, sandbox controls, and batch processing patterns. |
| [nanobot-personas-guide.md](agents/nanobot-personas-guide.md) | Nanobot Persona Engineering Guide | How to build production-grade, instruction-drift-resistant workspace personas for the HKUDS/nanobot framework. |
| [opencode-agents-config.md](agents/opencode-agents-config.md) | OpenCode Agent Configuration | Complete reference for configuring agents in OpenCode — JSON config, markdown agents, permissions, models, and all available options. |
| [opencode-agents.md](agents/opencode-agents.md) | Agents | Overview of OpenCode agent system — built-in agents, types, usage, creating agents, use cases, and example configurations. |
| [opencode-claude-codex-porting.md](agents/opencode-claude-codex-porting.md) | Porting Agents and Skills Between Harnesses | Field guide for migrating agent and skill definitions between OpenCode, Claude Code, and OpenAI Codex. For developers maintaining multi-platform AI coding configurations. |

### skills/

Skill (SKILL.md) authoring, best practices, and platform-specific features.

| File | Title | Description |
|------|-------|-------------|
| [nanobot-skills.md](skills/nanobot-skills.md) | Nanobot Skills | Covers nanobot-specific skill features including the SkillsLoader, MCP server pairing, metadata payload format, runtime support matrix, and skill configuration. |
| [skills-best-practices.md](skills/skills-best-practices.md) | Skills Best Practices for AI Assistants | Guidelines for creating, reviewing, and maintaining Skills that make AI assistants more reliable at repeatable tasks through focused instructions and clear workflow guidance. |

### scripting/

Deterministic scripts for AI agent execution.

| File | Title | Description |
|------|-------|-------------|
| [ai-scripting-best-practices.md](scripting/ai-scripting-best-practices.md) | Best Practices for Writing AI-Optimized Scripts | Architectural and stylistic principles for writing code optimized for execution by AI agents and LLM code interpreters. |

### misc/

Cross-cutting topics: platform best practices, security comparisons, LLM design, and documentation standards.

| File | Title | Description |
|------|-------|-------------|
| [ai-friendly-planning-evidence.md](misc/ai-friendly-planning-evidence.md) | AI-Friendly Plan Authoring and Execution -- Evidence | Claim-by-claim verification of the seven authoring properties and five execution rules, supporting and contradictory evidence, and all 29 references with citation mapping. |
| [ai-friendly-planning.md](misc/ai-friendly-planning.md) | AI-Friendly Plan Authoring and Execution | Standards for drafting implementation plans that AI agents can execute autonomously and incrementally, and the rules agents must follow when executing them. Backed by published research and industr... |
| [ai-vs-dast-comparison-deep-dives.md](misc/ai-vs-dast-comparison-deep-dives.md) | AI vs DAST Comparison: Vulnerability Deep Dives | Per-vulnerability-type descriptions for all 30 AI-delegated and DAST-delegated categories, with examples, reasoning, and validation steps. |
| [ai-vs-dast-comparison-evidence.md](misc/ai-vs-dast-comparison-evidence.md) | AI vs DAST Comparison: Evidence Base and References | Complete evidence base supporting the AI vs traditional DAST scanner delegation model, including AI cyber-agent studies, OWASP guidance, DAST scanner documentation, and citation mapping. |
| [ai-vs-dast-comparison.md](misc/ai-vs-dast-comparison.md) | AI vs Traditional DAST Scanner Vulnerability Delegation | Decision framework for delegating vulnerability testing between AI and traditional DAST scanners, with delegation matrix, recommended workflow, and counter-evidence. |
| [ai-vs-sast-comparison-evidence.md](misc/ai-vs-sast-comparison-evidence.md) | AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence | Supporting and contradictory evidence, all 13 references with citations, and claim mapping for the AI vs SAST/SCA/secret scanning delegation model. |
| [ai-vs-sast-comparison.md](misc/ai-vs-sast-comparison.md) | AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review | Defines when to delegate security review tasks to AI-assisted code review, SAST, SCA, secret scanners, or humans, with decision matrices and operating principles. |
| [codex-workspace-best-practices.md](misc/codex-workspace-best-practices.md) | Codex Workspace Best Practices | Optimization blueprint for configuring OpenAI Codex workspace personas, execution guardrails, file inheritance rules, and AGENTS.md cascade hierarchy. |
| [llm-budget-friendly-design-appendix.md](misc/llm-budget-friendly-design-appendix.md) | LLM Budget-Friendly Design Appendix | Practical engineering procedure for designing AI frameworks — state machine first, task decomposition, operation classification, LLM eligibility, evaluation, and avoiding overengineering. |
| [llm-budget-friendly-design-arch.md](misc/llm-budget-friendly-design-arch.md) | LLM Budget-Friendly Reference Architecture | Reference architecture for budget-friendly AI frameworks — system overview, project structure, runtime loop, context loading, multi-agent communication, failure handling, and model replacement. |
| [llm-budget-friendly-design-operating.md](misc/llm-budget-friendly-design-operating.md) | LLM Budget-Friendly Design — Operating | Operations and governance principles for workflow state separation, recoverability, token budgeting, framework complexity, and preferring reversible AI actions. |
| [llm-budget-friendly-design-patterns.md](misc/llm-budget-friendly-design-patterns.md) | LLM Budget-Friendly Design Patterns | Detailed patterns and implementation guidance for externalizing memory, file-based state passing, context boundary splitting, skills design, and interfaces optimized for AI consumption. |
| [llm-budget-friendly-design-templates.md](misc/llm-budget-friendly-design-templates.md) | LLM Budget-Friendly Design Templates | Design guidance and YAML templates for AI framework components — state models, phase contracts, skills, agents, prompts, and supporting template examples. |
| [llm-budget-friendly-design.md](misc/llm-budget-friendly-design.md) | LLM Budget-Friendly Design | Core philosophy and actionable principles for designing efficient, reliable, and scalable AI systems that minimize unnecessary LLM usage. |
| [nanobot-best-practices.md](misc/nanobot-best-practices.md) | Nanobot Best Practices for AI Customization | Practical guide for designing, customizing, and operating high-quality nanobot agents using the HKUDS framework, covering file-based cognition, memory, skills, and security. |
| [opencode-best-practices.md](misc/opencode-best-practices.md) | OpenCode Best Practices Guide | Optimal formats, structures, and constraints for designing OpenCode configurations, agents, and skills to maximize efficiency and reduce token waste. |
| [opencode-references.md](misc/opencode-references.md) | OpenCode Official Documentation References | Central index of OpenCode official documentation links for AI agents and developers configuring OpenCode agents, skills, tools, and permissions. |
| [reference-standards.md](misc/reference-standards.md) | Reference File Standards | Defines the consistent structure, frontmatter, writing style, and quality checklist for all reference documents in this repository, serving both human readers and AI coding agents. |

## Reference Relationships
Warm overviews branch into their cold deep-references. Cold files that no warm file references appear standalone.
### agents/
```
├── [Best Practices for AGENTS.md Files](agents/agents-best-practices.md) (☀️)
    └── [Porting Agents and Skills Between Harnesses](agents/opencode-claude-codex-porting.md) (❄️)
├── [Claude Code Subagent Examples](agents/claude-code-subagents-examples.md) (☀️)
    └── [Claude Code Subagent Configuration](agents/claude-code-subagents-configure.md) (❄️)
├── [Claude Code Subagents](agents/claude-code-subagents.md) (☀️)
    ├── [Claude Code Subagent Configuration](agents/claude-code-subagents-configure.md) (❄️)
    └── [Porting Agents and Skills Between Harnesses](agents/opencode-claude-codex-porting.md) (❄️)
├── [Codex Agent Conversion](agents/codex-agent-conversion.md) (☀️)
    └── [Porting Agents and Skills Between Harnesses](agents/opencode-claude-codex-porting.md) (❄️)
├── [Codex Subagents](agents/codex-subagents.md) (☀️)
├── [Nanobot Persona Engineering Guide](agents/nanobot-personas-guide.md) (☀️)
└── [Agents](agents/opencode-agents.md) (☀️)
    ├── [OpenCode Agent Configuration](agents/opencode-agents-config.md) (❄️)
    └── [Porting Agents and Skills Between Harnesses](agents/opencode-claude-codex-porting.md) (❄️)
```
### skills/
```
└── [Nanobot Skills](skills/nanobot-skills.md) (☀️)
    └── [Skills Best Practices for AI Assistants](skills/skills-best-practices.md) (❄️)
```
### scripting/
```
└── [Best Practices for Writing AI-Optimized Scripts](scripting/ai-scripting-best-practices.md) (☀️)
```
### misc/
```
├── [AI-Friendly Plan Authoring and Execution](misc/ai-friendly-planning.md) (☀️)
    ├── [AI-Friendly Plan Authoring and Execution -- Evidence](misc/ai-friendly-planning-evidence.md) (❄️)
    └── [LLM Budget-Friendly Design Patterns](misc/llm-budget-friendly-design-patterns.md) (❄️)
├── [AI vs Traditional DAST Scanner Vulnerability Delegation](misc/ai-vs-dast-comparison.md) (☀️)
    ├── [AI vs DAST Comparison: Vulnerability Deep Dives](misc/ai-vs-dast-comparison-deep-dives.md) (❄️)
    └── [AI vs DAST Comparison: Evidence Base and References](misc/ai-vs-dast-comparison-evidence.md) (❄️)
├── [AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence](misc/ai-vs-sast-comparison-evidence.md) (☀️)
├── [AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review](misc/ai-vs-sast-comparison.md) (☀️)
├── [Codex Workspace Best Practices](misc/codex-workspace-best-practices.md) (🔥)
├── [LLM Budget-Friendly Design](misc/llm-budget-friendly-design.md) (☀️)
    ├── [LLM Budget-Friendly Design Appendix](misc/llm-budget-friendly-design-appendix.md) (❄️)
    ├── [LLM Budget-Friendly Reference Architecture](misc/llm-budget-friendly-design-arch.md) (❄️)
    ├── [LLM Budget-Friendly Design — Operating](misc/llm-budget-friendly-design-operating.md) (❄️)
    ├── [LLM Budget-Friendly Design Patterns](misc/llm-budget-friendly-design-patterns.md) (❄️)
    └── [LLM Budget-Friendly Design Templates](misc/llm-budget-friendly-design-templates.md) (❄️)
├── [Nanobot Best Practices for AI Customization](misc/nanobot-best-practices.md) (☀️)
├── [OpenCode Best Practices Guide](misc/opencode-best-practices.md) (🔥)
├── [OpenCode Official Documentation References](misc/opencode-references.md) (🔥)
└── [Reference File Standards](misc/reference-standards.md) (☀️)
```
