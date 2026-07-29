# The Definitive Guide to AGENTS.md: Best Practices & Design Patterns

An `AGENTS.md` file is a repository-level operational policy file that guides AI coding agents (such as GitHub Copilot, Cursor, Claude Code, Windsurf, and custom terminal-native runtimes) on how to interact with your specific codebase. Positioned at the root of your repository, it serves as a bridge between the model's general training and your specific architectural conventions, tooling preferences, and execution workflows.

Unlike classic user documentation (`README.md`), an `AGENTS.md` file is written as **machine-executable constraint layers and verification criteria**, rather than tutorial prose.

---

## 1. Core Concepts & Anatomy of AGENTS.md

### The Concept of "Progressive Disclosure"

The single most critical failure mode of an `AGENTS.md` file is **context stuffing**---including full style guides, raw text error logs, or complete structural maps. This causes severe token bloat and degrades the agent's attention to critical rules.

Modern agent ecosystems maximize task accuracy using **Progressive Disclosure**:

1. **Root Configuration File (`AGENTS.md` / `CLAUDE.md`)**: Contains global invariants, exact file-scoped execution commands, and permission boundaries.
2. **The "Must-Read" Reference Registry**: Instead of writing complete guides inside the main file, outline an index mapping specialized domain paths (e.g., `- Forms schema: @docs/forms.md`). The agent reads this index, detects the relevant domain context, and lazily pulls in deep references on-demand.
3. **Rules vs. Skills**:
* **Rules** (`AGENTS.md` or `.cursor/rules/`): Static instructions telling the agent *how to behave* and *what constraints to respect*.
* **Skills** (`.claude/skills/`): Dynamic, procedural multi-step scripts telling terminal agents *how to execute complex orchestrations* (e.g., resolving a GitHub issue step-by-step using CLI utilities).



### Cross-Tool Compatibility Matrix

Because modern engineering teams use diverse AI tooling, `AGENTS.md` has emerged as the unified open standard governed across agentic platforms. However, parsing strategies vary:

* **GitHub Copilot / GitLab Duo**: Deeply parses `AGENTS.md` natively out of the box to locate tech stack specifics and explicit tool flags.
* **Claude Code**: Natively reads **`CLAUDE.md`**. Best practice is to create a lightweight `CLAUDE.md` that defines quick execution sequences and references `AGENTS.md` for extended rules.
* **Cursor**: Leverages the newer `.mdc` rule standard. A `.mdc` file utilizes a YAML frontmatter block to determine global or directory-scoped activation via glob patterns:
```yaml
---
description: Applied when editing React state components
globs: ["src/components/**/*"]
---

```



---

## 2. Optimal Sizing & Budgeting

* **The Rule of Thumb**: Keep the file **between 100 and 150 lines** (~800 to 1,500 tokens). This is a community-observed heuristic shared across Codex CLI best-practice guides and the AGENTS.md community (agents.md). OpenAI Codex enforces a 32 KiB discovery limit (`project_doc_max_bytes`); content beyond that threshold is silently truncated.
* **The Research Reality**: Performance degradation from long context is a documented phenomenon, but it depends on *position* and *distractor density*, not purely on line count. The canonical study — "Lost in the Middle" (Liu et al., TACL 2024) — found U-shaped accuracy curves: models perform best on information at the start or end of context, and can drop by ~20 percentage points when relevant information sits in the middle. Chroma's "Context Rot" study (Hong et al., 2025) tested 18 frontier models and confirmed all degrade as input grows, with degradation at every increment. The practical implication for AGENTS.md: keep instructions early in the file and reference detailed specs externally rather than burying them mid-file.
* **Actionability Rule**: Never send an LLM to do a deterministic linter's job. Do not include spacing, braces, or bracket preferences. Instead, provide the **exact CLI command string** needed to fix it (`pnpm run lint --fix`).

---

## 3. Mandatory Structure of a High-Performance AGENTS.md

To optimize an agent's structural interpretation, the document must transition from **high-level environment definition** down to **verifiable execution loops and behavioral boundaries**.

1. **System Identity & Tech Stack**: Absolute definitions of runtimes, framework version hooks, and tools (avoids speculative package usage).
2. **File-Scoped Execution Sequences**: Concise CLI scripts designed to execute against a single path target rather than running heavy repository-wide builds.
3. **Task-Organized Rules (Dos and Don'ts)**: Paired conditional assertions mapped to explicit action loops.
4. **Security Guardrails & Escalation Rules**: Explicit declarations mapping commands the agent is permitted to run autonomously versus actions that require strict human verification before execution.
5. **Definition of Done (PR Checklist)**: Explicit exit criteria used by the agent to confirm code validity before finalizing a task.

---

## 4. Production-Ready Template

Below is a production-optimized blueprint for an `AGENTS.md` file designed for modern AI development workflows.

```markdown
# Project Workspace Agent Configuration (AGENTS.md)

## 1. System Role & Technical Stack
You are an expert full-stack developer optimizing a multi-tier TypeScript and Python microservices application. 
- **Core Frameworks**: Next.js v15 (App Router), FastAPI v0.115+
- **Package Managers & Environment**: `pnpm` (Frontend), `uv` (Backend Python environment)
- **Database / ORM**: Prisma ORM with PostgreSQL

## 2. File-Scoped Execution Sequences
Always execute commands on file-scoped targets where possible instead of running complete system pipelines to minimize latency and token spend.

### Environment Anchoring
- TypeScript: `pnpm install`
- Python: `uv sync`

### Code Quality & Compilation Verification
- Linting Verification (TS): `pnpm run lint`
- Type Verification (TS): `pnpm run typecheck`
- Linting & Auto-fix (Py): `uv run ruff check . --fix`
- Type Verification (Py): `uv run mypy . --strict`

### Test Lifecycle Execution
- Single Unit Test (Frontend): `pnpm test -- <path_to_file>`
- Single Unit Test (Backend): `uv run pytest <path_to_file>`
- End-to-End Tests: Do not execute playwright or full E2E suites unless explicitly instructed.

## 3. Design & Architecture Invariants

### Task-Organized Guidelines (Do / Don't)
- **DO**: Use async/await syntax for all database I/O operations and external fetch routines in Python.
- **DO**: Wrap state updates inside Server Actions with defined error-boundary handling.
- **DO**: Use `unknown` coupled with explicit runtime type guards if an exact type interface cannot be inferred.
- **DON'T**: Never apply the `any` escape-hatch keyword in TypeScript.
- **DON'T**: Never hardcode configuration files or secret tokens. Reference `.env.example` configurations.
- **DON'T**: Do not use raw floating-point data primitives (`float`) for monetary operations; use `Decimal`.

### Reference Files (Lazy-Loaded Context)
When tasked with updating structural models, modules, or API layouts, read these specific paths first:
- Forms / Layout System: See `@docs/ui/forms.md` for schema representations.
- Data Layer Hydration: See `@docs/architecture/data-fetching.md` for conventions.

## 4. Security Guardrails & Tool Permissions

### Allowed Autonomously (No Approval Needed)
- Reading local files, executing `grep`/`ripgrep`, and mapping repository directory layouts.
- Invoking file-scoped unit tests, type checkers, and linters.
- Creating local Git branch checkpoints.

### Strict Approval Constraints (Require User Confirmation First)
- Executing destructive actions like table drops, asset folder deletions, or structural layout refactors.
- Network / Dependency mutation (`pnpm add` or `uv add` for third-party libraries).
- Running remote cloud platform pushes, external migrations, or executing `git push`.

## 5. Escalation Policy & Definition of Done
### When Blocked
- Do not make repeated, large speculative rewrites to the codebase.
- Halt execution and ask a clarifying question, or provide a short execution plan for human validation.

### PR and Commit Gate Criteria
Before marking a task as finalized, ensure:
1. Target files are fully checked using the regional typecheck and linter utilities.
2. The code passes its individual unit test parameters.
3. Commits follow the Conventional Commits specification (`feat(scope): ...`, `fix(scope): ...`).

```

---

## 5. SUBAGENTS BEST PRACTICES

Modern AI coding workflows increasingly use **specialized subagents** coordinated by an **orchestrator agent** instead of relying on a single general-purpose assistant.

Typical architecture:

``` text
User
  |
  |
Orchestrator
 |-- Security Agent
 |-- Backend Agent
 |-- Frontend Agent
 |-- Database Agent
 |-- Documentation Agent
 |-- Testing Agent
```

### Keep the Root AGENTS.md Thin

The root `AGENTS.md` should define:

- global policies
- security boundaries
- execution permissions
- coding conventions
- delegation strategy
- Definition of Done

Specialized knowledge belongs in dedicated agent instructions or referenced documentation.

### Give Every Subagent One Responsibility

Each subagent should own exactly one domain.

Examples include:

  Agent           Responsibility
  --------------- ------------------------------------------------------
  Security        Secure coding, threat modeling, vulnerability review
  Backend         APIs and business logic
  Frontend        UI, React, accessibility
  Database        Schema design and query optimization
  Documentation   Technical writing and API documentation
  Testing         Unit, integration and regression testing

Avoid creating "general software engineer" agents.

### Delegate by Capability

Delegate based on the problem being solved rather than directory layout.

Prefer:

> React rendering issue ? Frontend Agent

instead of

> Everything under `/frontend`.

### Minimize Context

Only provide the information required for the task.

This improves accuracy while reducing token consumption.

### Return Structured Results

Subagents should return concise summaries such as findings, confidence and recommendations rather than lengthy reasoning.

The orchestrator combines the outputs into a single response.

### Avoid Deep Delegation

Prefer:

``` text
Orchestrator
 |-- Backend
 |-- Security
 |-- Testing
```

instead of long chains where agents continuously delegate to one another.

### Keep Global Policy Centralized

Approval rules, package installation policies, destructive command restrictions and Git workflow belong only in the root `AGENTS.md`.

Subagents should inherit those policies instead of redefining them.

### Design for Reuse

Create reusable domain agents (for example, `SecurityAgent` or `ReactFrontendAgent`) instead of project-specific agents whenever possible.

Repository-specific knowledge should come from referenced documentation rather than hardcoded prompts.

### Common Anti-Patterns

- Monolithic "do everything" agents
- Duplicating global policies across subagents
- Passing the entire repository context to every agent
- Delegating solely by directory structure
- Deep chains of agent-to-agent delegation
- Conflicting instructions between orchestrator and workers
- Embedding large manuals into prompts instead of using progressive disclosure

---

## 6. Key Pitfalls to Avoid

* **Relying on Hardcoded Path Layouts**: Avoid specifying static, absolute file paths for domain modules (e.g., `Auth handlers live in /src/modules/auth/handlers.ts`). If a directory gets refactored, the agent will break trying to find a non-existent index. Instead, specify path-agnostic discoverability: *"Authentication handlers use JWT; find their exact boundaries dynamically via workspace `grep` filters."*
* **Enforcing Vague Prose Guidelines**: Refrain from using sentences like *"write clean code"* or *"be careful with memory leaks."* AI engines process actionable assertions much more effectively than subjective descriptions. Use concrete boundaries: *"Always check database handle pools are closed using context managers."*
* **Failure to Synchronize Downstream Tool Variations**: If you are maintaining a hybrid tooling stack (e.g., using `AGENTS.md` alongside `.cursorrules`), ensure they are synchronized. Conflicting setup commands across parallel files (like specifying `npm` in one file and `pnpm` in another) will cause loop failures as agents attempt to resolve competing directives. 
