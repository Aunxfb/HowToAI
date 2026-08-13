---
title: Reference File Standards
description: Defines the consistent structure, frontmatter, writing style, and quality checklist for all reference documents in this repository, serving both human readers and AI coding agents.
status: active
tags: [standards, reference, documentation, frontmatter, quality]
last_verified: 2026-08-13
layer: warm
applies_to: all reference files in this repository
---

# Reference File Standards

## Overview

This document defines the consistent structure, frontmatter, writing style, and quality checklist for all reference documents in this repository. It serves both human readers and AI coding agents — human contributors use it to create consistent files, and AI agents parse it to extract context efficiently. A standardized reference is predictable, scannable, and actionable regardless of which audience reads it.

## The Problem

Before these standards, reference files in this repository had:
- **Inconsistent frontmatter** — most files had none at all
- **No freshness signals** — no dates, status, or version info
- **No cross-references** — related files existed in isolation
- **Ad-hoc headings** — each file used its own structure, making AI retrieval unreliable

AI coding agents rely on predictable structure to extract context efficiently. Humans rely on consistent navigation to find information quickly. Without standards, both audiences waste context window and attention on decoding format instead of understanding content.

## Design Principles

### 1. Progressive Disclosure

Reference files operate in three layers:

| Layer | Loading | Purpose | Size Target |
|---|---|---|---|
| **Hot** | Always in context | Router, index, critical constraints | < 100 lines |
| **Warm** | Loaded by proximity or task relevance | Task-specific guides, patterns | 100-500 lines |
| **Cold** | Explicitly fetched via link | Deep reference, appendices, research | 500+ lines |

Root-level files should be hot. Subdirectory files should be warm. Deep dives belong in cold files linked from warm ones.

### 2. Predictable Structure

Every reference file follows the same skeleton so both humans and AI know where to find specific information without scanning the entire document.

### 3. Freshness Signals

Every file carries explicit metadata about its currency. Stale references are worse than missing ones because they actively mislead.

### 4. Actionable Over Descriptive

Write for execution, not exposition. Prefer concrete rules, commands, and examples over vague guidance. If a rule cannot be verified by a command or check, reconsider whether it belongs in a reference file.

### 5. Self-Documenting System

The standards themselves are documented in this repository. Any file can be evaluated against these standards. The standards evolve as the repository does.

### 6. Dual-Audience Readability

Write once, read by both. Avoid assumptions that favor one audience. AI agents parse structured markup and predictable headings; humans scan headings and bullet lists. Both benefit from concision, active voice, and explicit cross-references.

## File Structure

### Frontmatter

Every reference file **MUST** begin with YAML frontmatter between `---` delimiters.

```yaml
---
title: <concise, descriptive title>
description: <one or two sentences summarizing scope and audience>
status: <active | draft | deprecated | archived>
tags: [<comma-separated keywords for discovery>]
last_verified: <YYYY-MM-DD>
layer: <hot | warm | cold>
applies_to: <platform, component, or concept this covers>
---
```

**Field rules:**

| Field | Required | Rules |
|---|---|---|
| `title` | Yes | Sentence case. No trailing period. Max 80 chars. |
| `description` | Yes | Max 280 chars. Summarizes what the file covers and who it is for. |
| `status` | Yes | One of: `active`, `draft`, `deprecated`, `archived`. |
| `tags` | Yes | Array of lowercase keywords. At least 2, at most 8. |
| `last_verified` | Yes | Date the content was last confirmed accurate. |
| `layer` | No | One of: `hot`, `warm`, `cold`. Declares loading intent. Default inferred from directory (root = hot, subdirectory = warm). When set, line count **MUST** match the size target for that layer. |
| `applies_to` | No | Comma-separated list of platforms, tools, or concepts the document covers. |

### Naming Conventions

- **Files**: `kebab-case.md`. Descriptive but concise. Examples: `agents-best-practices.md`, `ai-vs-sast-comparison.md`.
- **Directories**: Short, lowercase. One or two words. Examples: `agents/`, `skills/`, `programming/`.
- **Sections**: `## Title Case Heading`. Stable across files of the same type.

### Required Sections

Every reference file follows this skeleton. Files may add subsections but **MUST NOT** omit or rename these top-level sections:

```
# Title

> One-line summary (optional — used when the description in frontmatter needs a visible companion).

## Overview

What this document covers, who it is for, and why it exists. 2-4 sentences. No tutorial content.

## Background

(Optional — omit for reference-type documents that don't need context.)

Prerequisites, terminology, or context needed to understand the document.

## [Content Section(s)]

The body. Structure depends on document type. Use stable headings that describe the content:
- For guides: ## Setup, ## Configuration, ## Usage
- For comparisons: ## Criteria, ## Comparison Matrix, ## Recommendations
- For references: ## Concepts, ## Patterns, ## Examples

## Related Documents

(Optional — links to the file's in-scope companion references. Omit when there are none.)

Companion links along the hot→warm→cold hierarchy, in either direction. See the cross-referencing rules below.

## References

(Optional — for research-backed documents.)

External sources, citations, or links to official documentation.

---
```

### Standard Subsection Headings

Use these consistently across files where applicable:

| Heading | Purpose |
|---|---|
| `## Overview` | Scope, audience, purpose |
| `## Background` | Prerequisites, context, terminology |
| `## Setup` | Installation, configuration, prerequisites |
| `## Configuration` | Settings, options, environment variables |
| `## Usage` | How to use the concept or tool |
| `## Patterns` | Recommended approaches |
| `## Anti-Patterns` | Approaches to avoid |
| `## Comparison Matrix` | Tabular comparison of options |
| `## Recommendations` | Concrete guidance on what to choose and why |
| `## Examples` | Practical examples with code blocks |
| `## Validation` | Commands or checks to verify correctness |
| `## Known Pitfalls` | Common mistakes and how to avoid them |
| `## Related Documents` | Cross-references to other files |
| `## References` | External citations and sources |

### Prohibited Patterns

- Do not use JSX-style components (`<Note>`, `<Tab>`, `<Step>`) — these break in many markdown renderers and confuse AI parsers.
- Do not use HTML tables where markdown tables suffice.
- Do not rely on JavaScript-dependent content for critical information.
- Do not use vague pronouns like "it" or "that" when the referent is not immediately clear.

## Writing Style

### Voice and Tone

- Use **active voice**. "The agent loads AGENTS.md" not "AGENTS.md is loaded by the agent."
- Write **imperative** for instructions. "Use `## Overview` as the first section heading."
- Be **concise**. Prefer bullet lists over paragraphs. Prefer one idea per sentence.
- Be **specific**. "Use `#private` field syntax" not "Follow our code style."

### Formatting

- **Fenced code blocks** for all code, configuration, and commands. Specify the language.
- **Markdown tables** for comparison matrices and structured data.
- **Bullet lists** for enumerations where order does not matter.
- **Numbered lists** only for sequential steps.
- **Bold** for UI labels and key terms on first use.
- **Inline code** for file names, commands, variable names, and literals.

### Examples

Every example **MUST** be labeled by intent:

- **[Copy-Safe]** — Ready to reuse with minor edits. Include imports, error handling, and test coverage.
- **[Conceptual]** — Illustrates the idea. Not production-ready.
- **[Deprecated]** — Kept for migration context only.
- **[Test-Only]** — Useful for fixtures, not production code.

### Terminology

- Use consistent terminology throughout a file and across the repository.
- If multiple terms exist for the same concept (e.g., "auth", "login", "identity"), list them as keyword aliases near the top of the relevant file so AI searches match regardless of vocabulary.
- Define acronyms on first use.

## Cross-Referencing

### Within the Repository

- Cross-references are **companion links along the hot→warm→cold hierarchy**, and they may run in either direction: an overview links down to its deeper references (hot→warm, hot→cold, warm→cold), and a deep reference links back up to its overview (cold→warm, warm→hot). Peer links (warm↔warm, hot↔hot) and governance/meta links (content files must not link to `reference-standards.md` or `reference-template.md`) are disallowed — those are repo conventions reachable via `AGENTS.md` and the README index.
- If a file has no in-scope companion, omit the section entirely.
- Use **relative markdown links** to reference other files. Example: `[Skills Best Practices](../skills/skills-best-practices.md)`.
- Link text **MUST** describe what the linked document contains. "See [Agent Best Practices](../agents/agents-best-practices.md)" not "See here."
- When a concept is documented in multiple files, the primary definition lives in one file and all others link to it.

### External References

- Use full URLs. AI agents can fetch web content when given explicit URLs.
- Prefer stable URLs (documentation, arxiv, spec pages) over blog posts that may move.

## Freshness and Maintenance

### File Header

Every file carries `last_verified` in its frontmatter. This date is updated when:

- The content is reviewed and confirmed accurate.
- The content is updated for changes.
- The file is read as part of a sweep and the date is bumped to confirm no changes needed.

### Status Values

| Status | Meaning | Search Behavior |
|---|---|---|
| `active` | Current and maintained | Included in all search results |
| `draft` | Work in progress, not yet authoritative | May be excluded from agent-oriented searches |
| `deprecated` | Superseded, kept for migration context | Excluded from default search results |
| `archived` | Historical reference only, no longer applicable | Requires explicit query to surface |

### Validation

Every reference file with commands or rules **SHOULD** include a `## Validation` section (or reference one) that documents:

- The command(s) that prove the content is still accurate.
- Expected output (or a way to check it programmatically).

If a command cannot be written, the document may need restructuring to make its rules verifiable.

## Quality Checklist

For every file:

- [ ] Frontmatter complete with all required fields
- [ ] First line is `# Title` matching frontmatter title
- [ ] Description is 1-2 sentences, max 280 chars
- [ ] Status is one of the four allowed values
- [ ] Tags array has 2-8 lowercase keywords
- [ ] `last_verified` is a valid date
- [ ] `layer` is one of `hot`, `warm`, `cold` (or absent to use directory default)
- [ ] File length matches its layer (hot < 100, warm 100-500, cold 500+), or layer is absent and length matches the directory default
- [ ] All section headings are from the standard set or justified exceptions
- [ ] No HTML tables where markdown tables work
- [ ] No JSX-style components
- [ ] All code in fenced blocks with language specified
- [ ] Every example labeled by intent
- [ ] All relative links are valid
- [ ] Terminology is consistent within file and with related files
- [ ] Cross-references, if present, are in-scope companion links along the hot→warm→cold hierarchy (overview→deeper, or deep reference→overview)
- [ ] File fits the progressive disclosure layer (hot/warm/cold) appropriate for its content
- [ ] Commands are copy-paste runnable or explicitly marked as placeholders

## Related Documents

- [Reference Template](reference-template.md) — template for creating new files that follow these standards.
