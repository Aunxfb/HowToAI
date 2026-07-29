# Codex Workspace Best Practices

An optimization blueprint for configuring OpenAI Codex workspace personas, execution guardrails, and file inheritance rules.

---

## 1. Document Scope & Length Metrics

### The 32 KiB Horizon
OpenAI Codex processes your workspace layout using an automatic discovery chain. It scans up to a strict hard limit of **32 KiB** across its discovery path. Exceeding this metric cuts off rules abruptly, causing unpredictable agent responses.

### Target Length Metrics
* **Optimal Payload Size**: 8 KB � 15 KB (Roughly **1,500 to 3,500 words**).
* **Context Conservation Target**: Keeping your rules file lean saves context window tokens, leaving more memory available for actual codebase reasoning loops.
* **Growth Buffer**: Cap your baseline documentation at ~12 KB to leave breathing room for adding local project overrides later.

---

## 2. File Architecture & Cascade Path

Codex merges your instructions across multiple folders. Rather than stuffing all rules into one long document, organize them across these layers:


```

~/.codex/AGENTS.md                <-- 1. Global Developer Habits (Lowest priority)
+-- [Project Root]/AGENTS.md      <-- 2. Project Architecture & Style Standards
+-- [Sub-Folder]/AGENTS.override.md  <-- 3. Isolated Constraints (Highest priority)

```

1.  **Global Level (`~/.codex/AGENTS.md`)**: Define your permanent, personal habits across all projects (e.g., `"Prefer absolute path mappings," "Always use pnpm over npm"`).
2.  **Project Root (`/AGENTS.md`)**: Outline the main repository constraints (Tech stack definitions, directory layout maps, linting paths).
3.  **Directory Level (`/[folder-name]/AGENTS.override.md`)**: Apply localized overrides to highly sensitive folders (e.g., placing an override file inside `/src/services/payments/` to enforce: `Permissions: Edit: Deny`).

---

## 3. The 5 Core Design Best Practices

### 1. Enforce Concrete Boundaries Over Abstract Advice
Codex relies on clear, deterministic rules rather than vague descriptions.
* ? **Vague**: *"Write clean, performant React components."*
* font-style: italic; (The model cannot measure "clean" or "performant" code directly).
* ?? **Deterministic**: *"Write components exclusively using the functional React 19 style. Avoid type assertions (`as unknown`) and do not use the `any` keyword."*

### 2. Establish a Strict Definition of Done (DoD)
Provide a clear checklist that Codex must complete before handing a task back to you. This ensures the model tests and validates its own code.
* *Example Section*:
    ```markdown
    Before signaling task completion, you must:
    1. Confirm the project compiles successfully using `pnpm build`.
    2. Run `pnpm lint` and resolve any new styling warnings.
    3. Update or create the corresponding unit tests inside `src/__tests__/`.
    ```

### 3. Offload Context Using Documentation Anchors
If you have extensive documentation, do not copy-paste it directly into your rules file. Instead, use clear pointers to tell Codex where to find that information.
* *Example Anchor*: `"When adding or editing database tables, follow the design principles detailed in docs/DB_STANDARDS.md before creating migrations."*

### 4. Isolate Tool & File Permissions
Prevent the model from modifying legacy files or breaking core configurations by setting explicit read/write rules.
* *Example Directive*: `"You are strictly read-only within the `/infra/terraform/` directory. You may read these files for context, but do not make changes to them directly."*

### 5. Prevent Token Bloat with Code Signatures
When adding code references to your rules file, only include the basic signatures or type outlines instead of pasting entire multi-line logic implementation details.

---

## 4. Production-Ready Template (`AGENTS.md`)

```markdown
# Project Name: Workspace Rules & Alignment

## 1. Project Context & Technical Stack
- **Purpose**: [Brief 1-sentence overview, e.g., Real-time inventory tracking platform]
- **Primary Tech**: Next.js 15 (App Router), React 19, TypeScript, Prisma, PostgreSQL.
- **Key Directories**:
  - `/src/app`: Next.js core application router logic.
  - `/src/components/ui`: Shared UI elements built using shadcn/ui styles.
  - `/prisma/schema.prisma`: Database schema definition file.

## 2. Engineering & Architecture Conventions
- **State Management**: Use React Server Components (RSC) for data fetching. Use `'use client'` strictly at the terminal UI leaves.
- **Error Handling**: Do not allow silent failures. Wrap API pathways in global try/catch blocks and send logs through `@/lib/logger`.

## 3. Environment & Execution Commands
- **Package Manager**: Always use `pnpm` (do not run `npm` or `yarn`).
- **Testing Engine**: We use Vitest. Run test sweeps via `pnpm test`.

## 4. Operational Guardrails & Constraints (CRITICAL)
- **Security**: Never hardcode credentials, tokens, or API keys. Read them securely via `process.env`.
- **System Changes**: Ask for user confirmation before executing commands that install new third-party production packages.

## 5. Definition of Done
Before completing any coding task, Codex MUST satisfy this checklist:
1. Validate that the TypeScript types compile completely without syntax errors.
2. Execute local linting sweeps (`pnpm lint`) and resolve any formatting issues.
3. Provide a brief summary of all modified files and changed functions in your final response.

```

