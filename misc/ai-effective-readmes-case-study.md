---
title: AI-Effective README Reference -- Case Studies
description: Comparative, line-by-line dissection of three real READMEs — HowToAI (non-code knowledge base), uv (code repo), and Claude Cookbooks (docs site) — read through the lens of AI consumption, with cross-case patterns and before/after rewrites.
status: active
tags: [readme, documentation, case-study, agents, context-engineering, analysis]
last_verified: 2026-08-13
layer: cold
applies_to: readers applying the AI-Effective README rules to real files
---

# AI-Effective README Reference -- Case Studies

## Overview

This document applies the [AI-Effective README Reference](ai-effective-readmes.md) to three real READMEs, dissecting what an agent actually reads, what works, and where the file leaks information. It is the evidence companion to that guide: where the guide states rules, this file shows them in situ. The three cases span the consumption spectrum — a non-code knowledge base, a code repository, and a documentation-site repository.

Cases were selected for contrast, not similarity:

- **Case Study A — HowToAI** (`README.md` in this repository): a non-code knowledge base whose README is a routing index. Primary non-code example.
- **Case Study B — uv** (`astral-sh/uv`): a code repository whose README is command-first. Commands-as-ground-truth analysis.
- **Case Study C — Claude Cookbooks** (`anthropics/anthropic-cookbook`): a docs-site repository whose README is a progressive-disclosure recipe index.

## Method

For each case:

1. **Structure map** — the file's section skeleton and what each part is for.
2. **What an agent reads** — the parse order a plain-text consumer follows and the first facts it absorbs.
3. **What works** — lines that follow the six rules from the guide.
4. **Gaps** — lines that leak or waste signal under at least one consumption mode (full-context, chunked retrieval, crawl).

All quoted material is from the READMEs as of 2026-08-13; READMEs change, so treat quotes as specimens, not current snapshots. Line numbers refer to the plain-text (rendered-source) ordering used in each README's raw file.

## Case Study A — HowToAI README (Non-Code Knowledge Base)

### Source and Context

`HowToAI/README.md` is the index and router of a curated reference knowledge base. The repository contains no code an agent would build; it contains reference documents organized into layers. The README's job is to route a reader (human or agent) to the right file without dumping the repository.

### Structure Map

| Lines | Content | Role in AI consumption |
|---|---|---|
| 1 | `# HowToAI` — H1 | Anchor for every parser (Rule 2) |
| 3 | Pitch paragraph | Human marketing; names the covered platforms |
| 5 | Agent pointer: "AI agents: see `AGENTS.md` for the hot → warm → cold loading protocol. This file is the index; read it before fetching any reference." | Explicit agent instruction — first-context routing |
| 7–98 | `## Directory Structure` with per-directory tables | The map: file, layer badge, title, description per row |
| 100–159 | `## Reference Relationships` tree | The hierarchy: which overview branches to which companions |

### What an Agent Reads

An agent loading this file first sees the H1, then the pitch, then the explicit routing instruction at line 5 — which is present *before* the tables, exactly where an agent that stops early will still see it. It then consumes the directory tables as its map. Each row is self-contained: filename, layer, title, description. An agent can grep the table for a topic keyword and get the file path immediately.

The relationship tree at line 100 is the second load-bearing element: it encodes which warm overview nests which cold companion, so an agent can decide "I need the deep reference for X; fetch `X-evidence.md` via the overview's link."

### What Works

- **Routing instruction up front** (line 5): names the file that governs behavior (`AGENTS.md`) and states what this file is for. A full-context agent that reads the first 30 lines is correctly directed. This is Rule 1 executed.
- **Layer column with explicit names**: the legend pairs emoji with words — "🔥 hot, ☀️ warm, ❄️ cold" — so the label survives plain-text parsing (Rule 5). The emoji is decoration; the words carry the fact.
- **One-row-per-entry tables**: each row answers "what is this file and what does it cover" in isolation — retrieval-friendly (Rule 6).
- **Descriptive link text**: rows link `[filename](dir/filename.md)`, and the title column says what the file covers. No "click here."
- **Descriptions capped**: `truncate()` in the generator caps descriptions at 250 chars, keeping rows scannable.

### Gaps

- **Human-marketing pitch at line 3** before the facts: the pitch names platforms (OpenAI Codex, OpenCode, Claude Code, Nanobot) but no explicit "what this repo is NOT" — a chunked retriever answering "is this a tool I install?" gets no signal until the tables.
- **Emoji-only redundancy risk**: the legend states hot/warm/cold in words, but the tree and tables rely on the emoji glyphs alongside the names; if a parser strips inline emoji mid-table, the layer column collapses to an empty cell — the words exist only in the legend, not per row. (Minor, because the columns still carry file+title+description.)
- **Description truncation** hides detail: a row whose description is cut at 250 chars ("...") may omit the one phrase a retrieval query would match.
- **No freshness cue in the map**: nothing in the tables tells an agent how recently a file was verified; agents must open each file to learn `last_verified`.
- **No explicit "read order" for cold files**: the tree shows nesting, but nothing says "fetch the evidence base only when you need to verify a claim" — the loading intent is implicit in the layer names.

### Agent Probe Verdict

- "What is this repo?" — answered at line 3 and confirmed by the tables. Pass.
- "What is the exact command to install/build/test?" — N/A (non-code); the file correctly does not fabricate commands. Pass.
- "Where does detail on X live?" — answered by the tables and tree for any indexed topic. Pass.

## Case Study B — uv README (Code Repo)

### Source and Context

`astral-sh/uv/README.md` is the front door of a Rust-written Python package manager. It is a large, feature-rich README: badges, a benchmark image, a command-first structure, and real console output in every feature section.

### Structure Map

| Lines | Content | Role in AI consumption |
|---|---|---|
| 1 | `# uv` — H1 | Anchor |
| 3–9 | Badge row (PyPI version, Python versions, Discord) | AI-invisible — images |
| 11 | "An extremely fast Python package and project manager, written in Rust." | One-line purpose — Rule 1 done right |
| 12–22 | Benchmark `<picture>` + image caption | AI-invisible chart |
| 25–37 | `## Highlights` bullet list | Facts: replaces pip/pip-tools/pipx/poetry...; 10-100x faster; platforms |
| 39–62 | `## Installation` with four verbatim install commands | Ground truth |
| 64–83 | `## Documentation` (short) | Routing to docs.astral.sh/uv |
| 85–228 | `## Features` with five subsections, each ending in a real command transcript | Commands-as-ground-truth, executed |
| 230+ | `## Contributing`, `## FAQ`, `## Acknowledgements`, `## License` | Stable closing sections |

### What an Agent Reads

The first plain-text facts are: H1, then a badge row that is *silence* to a text parser (four image links), then the one-line purpose at line 11, then a benchmark image (more silence), then the Highlights list. For a full-context agent, the load-bearing text begins at line 11 and the Highlights at line 25.

The `## Installation` block is where the agent's execution starts: four exact commands with flags. The `## Features` sections are the file's strongest asset for agents: each one (`Projects`, `Scripts`, `Tools`, `Python versions`, `The pip interface`) is a self-contained unit ending in a real `$`-prefixed transcript that shows expected output — an agent can run `uv init example` and diff its output against the transcript.

### What Works

- **One-line purpose at line 11** immediately after the badges: "An extremely fast Python package and project manager, written in Rust." — the single highest-signal sentence in the file, correctly placed (Rule 1).
- **Highlights as a fact list** (lines 25–37): every bullet is an executable claim ("A single tool to replace `pip`, `pip-tools`, `pipx`...", "Installable without Rust or Python via `curl` or `pip`") — chunkable, terminology-rich (Rule 6).
- **Install commands verbatim with flags** (lines 40–61): `curl -LsSf https://astral.sh/uv/install.sh | sh`, `pip install uv`, `uv self update`. An agent can copy-run without a single inference.
- **Transcripts as ground truth** (every Features subsection): output shown verbatim, so "does it work?" is answerable by comparison, not faith.
- **`uv help` mentioned** (line 80): tells an agent the CLI is self-documenting — a just-in-time retrieval path.
- **Stable skeleton** closing with Contributing/FAQ/License (Rule 2).

### Gaps

- **Badges before facts**: the four badge images occupy the first screen for a human but contribute nothing to a text parser. The version/platform facts they encode for humans (supported Python versions) are restated in Highlights — but the badge-row is still wasted signal for agents.
- **Benchmark image as evidence**: the "10-100x faster" claim (line 28) links a benchmark image and `BENCHMARKS.md`; an agent cannot verify from the image and must follow the link — Rule 5 violated (no text equivalent in the README itself).
- **Pronunciation/FAQ tail**: `## FAQ` answers ("How do you pronounce uv?") are human-only content; harmless but pure token cost for agents.
- **Feature sections are long**: five subsections with transcripts make the file large; a full-context agent pays for all of it even when the task is "install only." Progressive-disclosure would move the transcripts behind a `docs/` link and keep the README's transcripts to the quickstart (Rule 6 tension: uv trades retrieval-depth for full-context size).
- **`uv run ruff check` transcript uses `ruff` but highlights list `ruff`** — consistent, but an agent asked "what does uv replace?" must hold both terms; minor.

### Agent Probe Verdict

- "What is this repo?" — answered at line 11. Pass.
- "Exact install/build/test commands?" — install: verbatim. Build: the README says "Installable without Rust" but does *not* show `cargo build`; build-from-source lives behind the contributing link. Partial pass — the *user-facing* commands are complete; *contributor* build commands are fetched.
- "Where does deeper documentation live?" — `## Documentation` → docs.astral.sh/uv plus per-feature guide links. Pass.

## Case Study C — Claude Cookbooks README (Docs-Site Repo)

### Source and Context

`anthropics/anthropic-cookbook/README.md` is the front door of a repository whose entire content is notebooks and guides — a docs site living in GitHub. Its README is deliberately thin: a pitch, prerequisites, links, and one large index ("Table of recipes"). No build, no transcripts; the "product" is the links.

### Structure Map

| Lines | Content | Role in AI consumption |
|---|---|---|
| 1 | `# Claude Cookbooks` — H1 | Anchor |
| 3 | One-sentence purpose | Rule 1 |
| 5–12 | `## Prerequisites` | Facts: API key needed, Python, link to fundamentals course |
| 14–23 | `## Explore Further` | External links (docs, support, Discord) |
| 25–31 | `## Contributing` | Stable closing, issues/PRs guidance |
| 33–88 | `## Table of recipes` | The progressive-disclosure index |

### What an Agent Reads

The agent gets: H1 → one-sentence pitch → prerequisites → external links → a giant categorized link list. The `## Table of recipes` is the entire value: categorized bullets (`Capabilities`, `Tool Use and Integration`, `Third-Party Integrations`, `Multimodal Capabilities`, `Advanced Techniques`), each a link with a one-line note ("[Tool use](...): Learn how to integrate Claude with external tools and functions"). An agent asked "how do I do RAG with Claude?" can grep the index for "Retrieval Augmented Generation", follow the link, and fetch the notebook — exactly the llms.txt file-list pattern [1].

### What Works

- **Purpose in one sentence at the top** (line 3): "code and guides designed to help developers build with Claude, offering copy-able code snippets" — Rule 1, minimal.
- **Prerequisites as an explicit facts block** (lines 5–12): states the API key requirement and the language assumption up front, so an agent knows before fetching any notebook whether the material fits its stack.
- **Categorized index with per-item notes** (lines 33–88): every entry is `[name](url): one-line note` — self-contained, terminologically rich ("Retrieval Augmented Generation", "Sub-agents", "Prompt caching"), and directly retrievable (Rules 4 and 6, llms.txt pattern [1]).
- **Skeleton matches a docs-site expectation**: no fake install; the file correctly answers "where is the content" rather than inventing commands (Rule 3's N/A branch).
- **Sub-categorization** (e.g., `Tool Use and Integration` → `customer_service_agent.ipynb`, `calculator_tool.ipynb`): gives agents topic-level precision before fetching a notebook.

### Gaps

- **No text context for a reader who never follows links**: the index is entirely pointer; an agent that must answer "does this cookbook cover vision?" reads category headings and must open files to confirm. For a docs-site index this is acceptable (the README's job is routing, not answering) but it is the inverse of uv's depth-in-file choice.
- **Nested bullets under categories** have trailing structure (`- [Tool use](...): Learn how to integrate Claude with external tools and functions to extend its capabilities.` followed by indented sub-items) — a chunked retriever that splits mid-list can orphan a sub-item from its category heading (Rule 6: keep hierarchy shallow).
- **"Additional Resources" tail** (lines 88+): links out to AWS samples with a caveat ("may require modification") — good caveat, but a tail of external links costs full-context tokens with low routing value.
- **Missing freshness**: no date or version marker; an agent cannot tell whether "best practices for vision" is current (the guide's Validation probes for exactly this).

### Agent Probe Verdict

- "What is this repo?" — answered at line 3. Pass.
- "Exact install/build/test commands?" — N/A; correctly absent. Pass.
- "Where does deeper documentation live, by topic?" — the whole README is that answer. Pass.

## Cross-Case Patterns

| Pattern | HowToAI (A) | uv (B) | Cookbooks (C) |
|---|---|---|---|
| One-line purpose in first screen | ✓ (line 3) | ✓ (line 11) | ✓ (line 3) |
| Commands as ground truth | N/A | ✓ verbatim + transcripts | N/A |
| Routing index / file map | ✓ tables + tree | Partial (docs links) | ✓ categorized index |
| Text equivalent for visuals | ✓ layer names in words | ✗ badges, benchmark image | N/A (no visuals) |
| Self-contained sections | ✓ per-row | ✓ per-feature | ✓ per-index-entry |
| Explicit freshness cue | ✗ (in files only) | ✗ | ✗ |
| What this repo is NOT | ✗ | ✗ | ✗ |
| Keep-size balance | ✓ small | ✗ large, transcripts inline | ✓ small |

**Three cross-case conclusions:**

1. **All three front-load the purpose** — and it is always the highest-signal sentence in the file. None of the three states "what this is NOT", a common cheap win.
2. **Code repos and docs sites split on depth-in-file**: uv inlines execution depth (transcripts), Cookbooks externalizes it (links). Both satisfy their consumers because the README's *role* — executable entry point vs router — is honored. The failure mode would be a code repo that routes without commands, or a docs site that inlines every page.
3. **Visuals and freshness are the universal blind spots**: every case has an AI-invisible element (uv's badges/chart, the layer emoji in A) and none exposes freshness in the README itself. Rule 5 and the freshness discipline in the guide exist because real files leak exactly here.

## Before/After Rewrites

**[Copy-Safe]** — how a mixed-order README opening becomes machine-first. The "Before" is a composite of the gaps observed in the cases (marketing-first, badges, implied commands); the "After" applies Rules 1–3.

Before (marketing-first, badges before facts, commands implied):

```markdown
# PulseBot

🚀 The smartest notification bot for Slack and Discord!

[![Stars](stars.svg)] [![Build](build.svg)] [![Discord](discord.svg)]

PulseBot is the culmination of years of research into how teams actually
communicate. Join our community, star the repo, and watch the magic.

## Getting started

You'll need Node and a database. Then you can start the app and point it at
your channels. See the docs for the full guide.
```

After (machine-first, facts and commands front-loaded):

```markdown
# PulseBot

A notification bot that forwards webhooks into Slack and Discord channels,
written in Node.js 22+ (TypeScript). Runs on any Node host; not a chat
automation platform.

- Install: `npm install -g pulsebot`
- Configure: `pulsebot init --channel #ops`
- Test: `npm run test`

## Overview

PulseBot receives HTTP webhooks and posts formatted messages to configured
Slack/Discord channels. It replaces in-house curl scripts, not a full
chat-automation suite.

## Installation

```bash
npm install -g pulsebot   # requires Node 22+
```

## Usage

```bash
pulsebot init --channel #ops     # interactive; writes pulsebot.json
pulsebot run --config pulsebot.json
```

## Documentation

- [Configuration reference](docs/configuration.md): all channels, filters, retries
- [Deploy guides](docs/deploy.md): Docker, Fly.io, bare Node
- [FAQ](docs/faq.md): rate limits, token scopes

## Contributing

Report issues at https://github.com/example/pulsebot/issues.
```

What changed and why: the purpose sentence now carries the facts an agent needs (language, platform, the NOT-x). Commands are verbatim with flags instead of "you'll need Node and a database." The docs section is an llms.txt-style file list [1]. The badges are gone — their facts (status, support) are not critical to an agent's first decision.

## Related Documents

- [AI-Effective README Reference](ai-effective-readmes.md) — the rules this case study applies; read the rules first, then the cases as evidence.
- [AI-Friendly Plan Authoring and Execution](ai-friendly-planning.md) — plan authoring for agent execution; the "commands as ground truth" rule in the README guide mirrors the plan-standard's executable-task rule.

## References

1. Howard, J., "The /llms.txt file, v2," llms-txt.org. https://llmstxt.org/
2. astral-sh, "uv — README.md" (raw). https://raw.githubusercontent.com/astral-sh/uv/main/README.md
3. Anthropic, "Claude Cookbooks — README.md" (raw). https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/README.md
4. Anthropic, "Effective context engineering for AI agents," Sep 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
5. kapa.ai, "Writing documentation for AI: best practices," kapa.ai docs. https://docs.kapa.ai/improving/writing-best-practices

---

*Last verified: 2026-08-13 — update this date when content is reviewed or changed.*
