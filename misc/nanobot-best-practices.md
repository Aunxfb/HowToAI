# Nanobot Best Practices for AI Customization

A practical guide for designing, customizing, and operating high-quality nanobot agents using the HKUDS framework.

---

# Architecture Philosophy: File-Based Cognition

nanobot is an ultra-lightweight personal AI agent framework (~4,000 lines of Python core). It rejects massive, monolithic orchestration engines. Instead, it delegates agent behavior to a **file-first cognitive architecture** in your workspace, while using a central `config.json` strictly for routing APIs, setting up chat channels (Telegram, Discord, Slack, WebUI), and managing tool sandboxing.

The best nanobots are:

* **Narrowly scoped:** Driven by concise, highly declarative markdown files.
* **Context-disciplined:** Using on-demand skill loading to prevent token bloating.
* **Operationally isolated:** Utilizing isolated per-session execution tracks so parallel user requests don't overlap.

---

# The System Prompt Equation: Optimizing Workspace Files

At the start of every chat turn, nanobot's engine runs `build_system_prompt()`. This function dynamically stitches together your core workspace markdown files to create the foundation of the agent's context.

Because everything is concatenated, keeping these core files lean is critical to avoid token inflation, high inference costs, and "lost-in-the-middle" instruction drift.

```
┌──────────────────────────────────────────────────────────┐
│                   build_system_prompt()                  │
├───────────┬───────────┬───────────┬──────────────┬───────┤
│ AGENTS.md │  SOUL.md  │  USER.md  │  MEMORY.md   │ SKILL │
│ (Rules)   │ (Persona) │ (Profile) │ (Compacted)  │ (Body)│
└───────────┴───────────┴───────────┴──────────────┴───────┘

```

### Workspace File Reference Guide

| Workspace File | Target Size | Functional Role | Optimization Guardrail |
| --- | --- | --- | --- |
| **`AGENTS.md`** | **300 – 400 words** | **Active Runtime Manual:** Governs tool execution rules, multi-agent task delegation boundaries, and background loop automation. | Avoid abstract philosophy. Use strict formatting blocks (`# Rules`, `# Tool Usage`) so the model switches cleanly to tool-calling mode. |
| **`SOUL.md`** | **250 – 450 words** | **Identity & Persona:** Defines character traits, communication style, tone preferences, and core behavioral values. | Do not exceed 600 tokens. Over-conditioning emotional context causes the model to ignore practical workspace instructions. |
| **`USER.md`** | **150 – 300 words** | **User Profile & Environment:** Explicitly declares your OS, coding environment, specific preferences, and localized context. | Keep up-to-date with your current tech stack. Let the model read this to tailor shell commands and file changes to your host machine. |
| **`HEARTBEAT.md`** | **200 – 350 words** | **Scheduled Automation:** Templates the cron rules and periodic tasks executed asynchronously by the backend daemon. | Ensure instructions have explicit exit criteria so proactive background tasks don't get stuck in execution loops. |

> **Architectural Best Practice:** Protect the core file layer. Never manually inject fluid facts, temporary project updates, or learned user quirks here. Offload all active conversation summaries to `memory/MEMORY.md` or modularize workflows into the `skills/` directory.

---

# Memory Best Practices: The "Dream" Protocol

nanobot splits its memory architecture into two distinct pipelines: raw history execution and long-term consolidation.

## 1. Respect the Multi-Stage Memory Lifecycle

* **Stage 1 (Raw Logs):** The active turn interaction logs tool results and text streams directly into `history.jsonl` or `memory/HISTORY.md`. This is hard-capped (typically the last 50 entries up to 32k characters) to protect the context window.
* **Stage 2 (The Dream Loop):** In the background, the framework triggers its native **Dream** protocol. It reads the raw log traces, runs a pattern analysis, extracts durable insights (e.g., "User changed production cluster to AWS-West"), and appends/consolidates them cleanly into **`memory/MEMORY.md`**.

## 2. Leverage Auto-Compaction

Let the engine room handle micro-compaction. Do not manually edit `MEMORY.md` during live sessions. Instead, ensure that your `config.json` sets a reasonable `memoryWindow` (e.g., 50) and let the background coroutines systematically handle token pressure reduction.

---

# Skills Engineering: Modular Extension over System Bloat

If you want your nanobot to execute specific complex workflows (e.g., stock market analysis, code performance profiling, or multi-exchange tracking as introduced in PR #1219), do not write them into `AGENTS.md`. Use the native **Skill System**.

```
~/.nanobot/workspace/skills/
  └── stock-analysis/
      └── SKILL.md      <-- Contains targeted tool descriptions & frontmatter

```

### Best Practices for Designing a `SKILL.md`:

* **Use Clear Frontmatter:** Declare the metadata exactly so the framework's `SkillsLoader` can catalog it efficiently.
```markdown
---
name: stock_analyzer
description: Fetches real-time market data and executes technical indicator formulas.
always: false
requires: pandas, httpx
---

```


* **On-Demand Compounding:** Set `always: false` for hyper-specific workflows. This allows `build_skills_summary()` to inject a tiny, single-line XML summary into the prompt. The full manual is only read into context when the agent explicitly elects to trigger the skill.
* **Idempotent Tool Writing:** When writing custom Python skills or wrapping external APIs, guarantee that repeated calls are safe. For high-risk, destructive actions, mandate an explicit dry-run block or use the native `ask_user` tool to pause execution for a manual user confirmation handshake.

---

# Configuration & Platform Fine-Tuning

Your core infrastructure routes through `~/.nanobot/config.json`. Optimize this file to maintain structural boundaries across channels.

### 1. Multi-Provider Resiliency

Always design a heterogeneous provider stack. If your main reasoning model suffers from latency spikes or API timeouts, nanobot should fall back gracefully.

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

*When pointing at reasoning models like DeepSeek-V4 (`deepseek-reasoner`), ensure that your config explicitly supports streamed thinking blocks so the real-time reasoning transcript is isolated from the conversational message payload.*

### 2. Granular Channel Interface Controls

Avoid global communication settings. Fine-tune your `channels` settings directly inside your JSON structure. You can turn progress indicators off for chat platforms to minimize spam, while keeping them completely verbal on your local WebUI.

```json
"channels": {
  "telegram": {
    "enabled": true,
    "token": "ENV_TELEGRAM_TOKEN",
    "allowFrom": ["YOUR_USER_ID"],
    "sendProgress": false,
    "inline_keyboards": true
  },
  "websocket": {
    "enabled": true,
    "sendProgress": true,
    "sendToolHints": true
  }
}

```

---

# Security & Isolation Guardrails

Because nanobot has access to direct terminal execution and filesystem pathways, treating security as an operational priority is a necessity.

* **Isolate Pathing:** Keep `"tools": { "restrictToWorkspace": true }` active in production. This walls off the agent loop from reading or editing raw system directories outside your active `~/.nanobot/workspace`.
* **Sandbox the Shell System:** Never run the `nanobot gateway` process as root. In multi-user setups or public chat channels (Slack/Discord), enforce sandboxing by wrapping local commands natively using isolated container environments or container runtimes (e.g., running nanobot inside Docker with restricted volume mappings).
* **Audit Traces:** Actively monitor your runtime session logs. Watch for overlapping tool calls or race conditions, particularly when deploying complex background tasks driven by `HEARTBEAT.md` loops.

---

# Anti-Patterns to Avoid

* ❌ **Monolithic Prompt Packing:** Shoving 2,000 lines of documentation directly into `AGENTS.md`. (Use on-demand Skills or MCP servers instead).
* ❌ **Open-Ended Loop Definitions:** Setting a high `maxToolIterations` (e.g., >50) without a strict stop criteria in the markdown instructions, inviting endless recursive self-reflection loops.
* ❌ **Unprotected Global Inbound Channels:** Enabling Telegram, Discord, or DingTalk bridges without populating the `allowFrom` or `group_allow_from` list—effectively granting random internet users access to execute workspace commands.
* ❌ **Over-Agentification:** Creating separate sub-agents for minor linear tasks that a single model execution turn could solve directly with standard tools.