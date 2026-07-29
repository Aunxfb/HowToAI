To convert OpenCode agents and subagents into a Codex-compatible structure, you have to map them across two completely different design systems.

* **OpenCode** switches environments dynamically by routing completely independent sessions via a TUI or `@name` flags.
* **Codex** runs a singular, continuous main agent loop. It handles varying responsibilities by ingesting a **layered markdown file hierarchy (`AGENTS.md`)** and executing conditional procedures called **Skills**.

Here is how to break down and map your OpenCode agent configurations (`.opencode/agents/` or `opencode.json`) into the official Codex format.

---

## 1. Mapping Table: OpenCode vs. Codex Architecture

| OpenCode Property | Codex Mapping Strategy | Implementation Choice |
| --- | --- | --- |
| **`mode: "primary"`** | Converted into your repository's root **`AGENTS.md`** file. | Universal baseline instructions always loaded in the environment. |
| **`mode: "subagent"`** | Converted into a **Codex Skill (`.agents/skills/`)** or a targeted **Subdirectory Override**. | Triggered by conditional tasks or localized directory scopes. |
| **`permissions`** (`deny`, `ask`, `allow`) | Evaluated via **Developer/Developer Sandbox Prompt Directives** inside `AGENTS.md`. | Dictates shell evaluation thresholds and file access limits textually. |

---

## 2. Converting a Primary Agent (e.g., `Build` / `Plan`)

If you have a primary OpenCode agent that dictates how the code should be constructed or evaluated, extract its system instructions and drop them straight into your root `/AGENTS.md`.

### OpenCode Configuration (`.opencode/agents/plan.md`):

```markdown
---
description: Restricted planning agent
mode: primary
permission:
  edit: ask
  bash: ask
---
You analyze architectural patterns. Do not edit code directly.

```

### Translated Codex Root Configuration (`/AGENTS.md`):

```markdown
# Codex Architectural Plan Configuration

## 1. Persona & Strategy
You act as our repository structure planner. Prioritize dry-runs and blueprint definitions over hasty implementation.

## 2. Tool Guardrails & Permissions
- Before altering any files or initiating system updates, you MUST prompt the host user for validation.
- Treat backend structural directories as read-only unless an explicit write instruction is passed in the prompt thread.

```

---

## 3. Converting Subagents (e.g., `Reviewer`, `Security-Scout`)

OpenCode invokes specialized tasks via `@mention` routing (e.g., `@explore` or `@security`). In Codex, these specialized behaviors are converted into **Skills** that live inside your project repo under `.agents/skills/<name>/SKILL.md`. Codex matches these automatically when your prompt matches the skill metadata.

### OpenCode Subagent Template (`.opencode/agents/security.md`):

```markdown
---
description: Scans project for vulnerable dependency trees and secret leakage
mode: subagent
permission:
  edit: deny
  bash: allow
---
You are an aggressive security auditor. Scan configurations and look for exposed keys.

```

### Translated Codex Skill Configuration (`.agents/skills/security/SKILL.md`):

```markdown
# Security Audit Skill

## Metadata
- **Description**: Trigger this workflow when the user requests code auditing, security validations, dependency verification, or credential tracking.
- **Trigger Keywords**: security, audit, verify dependencies, scan credentials, CVE check.

## System Directive
You act as an aggressive local security auditor. 

## Tooling Execution Plan
1. You have permission to invoke read commands and local dependency checking loops.
2. Critical Guardrail: You are explicitly denied file mutation rights. Output vulnerabilities purely as a summary matrix inside the conversation log�do not apply edits.

```

---

## 4. Converting Local Permission Trees

OpenCode uses a hardcoded configuration schema to lock down binary tools. Because Codex processes environment restrictions through text instructions and its developer sandbox template, you convert those rules into clear, imperative formatting clauses.

* **OpenCode `edit: deny**` $\$rightarrow **Codex Textual Guardrail:** `"CRITICAL: Do not modify files within this path. You are operating in a read-only context."`
* **OpenCode `bash: ask**` $\rightarrow$ **Codex Textual Guardrail:** `"You must output shell scripts into a markdown block for review and await user approval before firing execution layers."`

In OpenAI Codex, multi-agent coordination moves away from independent running sessions and instead uses a centralized routing structure guided by your workspace markdown files.

---

## The Codex Orchestration Pattern

Instead of configuring a standalone "orchestrator agent" that manages subagents via chat loops, the **Codex Main Agent Loop** acts as the core router. You define the orchestration rules in the root `AGENTS.md`, and you deploy the "experts" as specialized **Skills** or **Subdirectory Overrides**.

```
                +------------------------+
                �   Codex Main Loop      �  <-- Acts as the Orchestrator
                +------------------------+
                            �
         +------------------+------------------+
         ?                  ?                  ?
+-----------------++-----------------++-----------------+
�  Expert Skill A ��  Expert Skill B �� Directory Impl. �
�  (Static/SAST)  �� (Dependency/CI) �� (Service Rules) �
+-----------------++-----------------++-----------------+

```

---

## 1. Setting Up the Orchestrator (`/AGENTS.md`)

The root `AGENTS.md` file serves as the global brain for the session. It tells the main Codex loop when to work quietly, when to escalate tasks, and how to delegate analysis to specialized guidelines.

```markdown
# Defensive Audit Workspace Orchestrator

## 1. Operational Mode
You function as the Security Review Orchestrator. Your goal is to analyze the repository for architectural weaknesses, misconfigurations, and compliance drift.

## 2. Delegation Strategy
Do not attempt to solve multi-step validation processes in a single generic chat turn. Instead, delegate to specialized playbooks using the following routing conditions:
- If reviewing static source code patterns or language-specific vulnerabilities, invoke the rules defined in `.agents/skills/sast-review/SKILL.md`.
- If inspecting configuration files, infrastructure-as-code, or container parameters, pivot execution context to the criteria found in `.agents/skills/infra-audit/SKILL.md`.

## 3. Tool Constraints
- Operating Level: Read-Only across all primary source directories.
- Modification: Restrict file writes explicitly to generating output reports under the `/audit-reports/` path.

```

---

## 2. Deploying the Experts (Codex Skills)

In OpenCode, experts are separate agents with unique system prompts. In Codex, these experts are packaged into the `.agents/skills/` directory. Each skill contains **Trigger Keywords** or specialized prompts that tell the main loop how to change its persona.

### Expert 1: Static Analysis Expert (`.agents/skills/sast-review/SKILL.md`)

```markdown
# Skill: Static Application Security Testing (SAST)

## Persona Alignment
You are a precision code auditor specializing in OWASP Top 10 mitigation patterns for TypeScript and Node.js.

## Execution Rules
1. Scan input files specifically for weak cryptographic primitives, injection vectors, and broken object-level authorization (BOLA) structures.
2. Cross-reference identified patterns against industry-standard defensive controls.
3. Format discoveries strictly into a Markdown compatibility table specifying File, Line, Vulnerability Type, and Remediation Strategy.

```

### Expert 2: Infrastructure Compliance Expert (`.agents/skills/infra-audit/SKILL.md`)

```markdown
# Skill: Infrastructure Compliance Auditor

## Persona Alignment
You are an expert in cloud infrastructure compliance (CIS Benchmarks, Docker security, and Kubernetes network policies).

## Execution Rules
1. Inspect deployment manifests, Dockerfiles, and cloud configuration scripts.
2. Flag instances of root-user execution inside containers, overly permissive security groups, or unencrypted persistent storage volumes.
3. Provide remediation snippets conforming exactly to the secure versions of those respective configuration schemas.

```

---

## 3. Triggering the Workflow

Once your files are placed in the repository, you interact with the system via the Codex CLI or Desktop workspace interface.

* **To run the general orchestrator:** Simply prompt Codex normally: `"Analyze the current workspace state for compliance issues."` Codex will ingest `AGENTS.md` and map the scope of the project.
* **To invoke a specific expert:** Use the trigger phrases or explicit skill paths defined in your skill files: `"Execute a SAST review on the authentication module under /src/auth."` Codex will immediately load the specific `.agents/skills/sast-review/SKILL.md` rules into its active context to process that task.