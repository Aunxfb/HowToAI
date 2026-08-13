---
title: AI-Effective README Reference
description: Rules for making README.md files effective for AI agents — dual-audience writing, commands as ground truth, index patterns for non-code repos, and AI-invisible media pitfalls, with a copy-safe template and validation.
status: active
tags: [readme, documentation, agents, progressive-disclosure, context-engineering, dual-audience]
last_verified: 2026-08-13
layer: warm
applies_to: any repository's README.md, for both human and AI-agent readers
---

# AI-Effective README Reference

> A README is the first context an agent has for an unfamiliar repo — dual-audience: humans scan it, agents execute from it.

## Overview

This reference defines rules for writing `README.md` files that are effective for AI agents while remaining scannable for humans. It applies to any repository — code repos, documentation sites, and non-code projects alike. It is for maintainers who want their first-context file to route agents correctly instead of wasting their context window. A comparative, line-by-line dissection of real READMEs lives in the [case study companion](ai-effective-readmes-case-study.md).

## Background

A README is the first document an agent receives about an unfamiliar repository. Unlike `AGENTS.md` (which is explicit machine-executable policy), a README is **dual-audience**: humans scan it for a pitch and quickstart, and agents read it to bootstrap understanding before executing commands. The sibling artifact guide [Best Practices for AGENTS.md Files](../agents/agents-best-practices.md) contrasts the two: README answers "what is this and how do I use it", AGENTS.md answers "how do I behave while working here".

How an agent actually consumes a README depends on the harness, and the differences drive the rules:

- **Full-context readers** (coding agents like Claude Code, Codex, OpenCode) drop the file into context verbatim. Here the *whole file* is read once, so layout and early placement dominate — information in the middle of a long file is used worst (lost-in-the-middle).
- **Chunked retrievers** (RAG assistants like kapa.ai) split the file into semantic chunks and fetch only the relevant ones. Here each section must make sense in isolation, because retrieval never reads the file as a narrative [4].
- **Crawlers and indexes** (search, llms.txt consumers) reduce the file to text and links. Here structure, headings, and link text are the only signal; anything visual is invisible [1][4].

The consequence: a README that looks great rendered but collapses when parsed as plain text fails every machine reader. The rules below keep the file effective across all three consumption modes.

## Core Concepts

- **First-context file**: the README is what an agent reads before forming any assumption about the repo. Errors here compound.
- **Dual-audience**: humans scan for what the project is and whether it fits; agents scan for facts, commands, and file paths to act on. Both want the same facts first.
- **Progressive disclosure**: put the executive summary and the load-bearing facts up front; push detail behind links, fetched only when a task needs it [2][3].
- **AI-invisible media**: badges, images, emoji, ASCII art, and merged tables carry meaning visually that plain-text parsing loses [4]. Anything critical must exist as text too.
- **Ground truth**: in a code repo, the commands an agent runs (install, build, test) are the highest-value content in the file [3].

### README vs AGENTS.md vs Docs

Three artifacts, three jobs — do not merge them:

| Artifact | Job | Who reads it |
|---|---|---|
| `README.md` | Pitch + routing: what it is, how to use it, where the detail lives | Humans scan, agents bootstrap |
| `AGENTS.md` | Behavior: how an agent must operate in this repo (commands, boundaries, escalation) | Agents only |
| `docs/` | Depth: tutorials, references, API detail behind links | Both, on demand |

A README that tries to be an AGENTS.md buries its routing job under policy; a README that tries to be docs dumps every manual page into one context. When in doubt, keep the README the shallow router and push policy to `AGENTS.md` and detail to `docs/` [2][3].

## Rules

### Rule 1 — Front-load Critical Facts in the First ~30 Lines

Put the three things every reader needs inside the first screen of plain text: what the project is, what it is for, and what it is not for.

- State the one-line purpose immediately after the `# Title`.
- List the top 3–5 facts an agent must not get wrong: language, package manager, supported platforms, the "this is NOT X" caveat.
- Treat the first 30 lines as the elevator pitch for machines — a task-scoped agent may decide from this alone whether to proceed.

**[Conceptual]** — wrong order (marketing first):

```markdown
# SuperFast CLI

🚀⚡🔥 The fastest, most awesome CLI you'll ever use!

[![GitHub stars](stars.svg)] [![Build](build.svg)] [![Join our community](discord.svg)]

We're a small team on a mission to revolutionize...

## Why SuperFast is different from everything else
```

**[Conceptual]** — machine-first order:

```markdown
# SuperFast CLI

A command-line tool for batch-renaming files with glob patterns, in Go (Go 1.22+).
Runs on macOS, Linux, and Windows.

- Install: `go install github.com/example/superfast@latest`
- Build: `go build ./cmd/superfast`
- Not a file-watcher; use `watch` for that.
```

### Rule 2 — Blockquote Summary + Predictable Skeleton

Give the file an immediately identifiable shape: an H1, a blockquote one-liner, then a stable set of sections. This mirrors the llms.txt v2 convention (H1 + blockquote summary + file lists) and makes the file machine-routable [1].

- Keep the blockquote to one sentence; it is the "key takeaway" for parsers.
- Use a stable skeleton across repos: `## Overview/Install/Usage`, `## Documentation`, `## Contributing`.
- Keep section headings descriptive; a heading is a retrieval target, not decoration [4].
- Do not bury the section you most need an agent to find below marketing.

### Rule 3 — Commands as Ground Truth (Code Repos)

For a code repository, the README's commands are what an agent will execute. Verbatim, runnable, unambiguous.

- Give the exact install command(s) with flags — "install with your package manager" is not executable.
- Give the build/test/lint commands, with flags, for the project's actual toolchain.
- Show real output where it disambiguates (an agent can verify against it).
- Version-pin nothing that changes weekly; but do pin the language/toolchain version contract.

**[Copy-Safe]** — command block pattern:

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh   # or: pip install uv

# Project
uv init example && cd example
uv add ruff
uv run ruff check
uv lock && uv sync
```

The pattern holds regardless of ecosystem: whatever `git clone` → install → verify looks like for your project, state it literally.

### Rule 4 — Index/Map Pattern for Non-Code Repos

For non-code repositories (knowledge bases, specifications, policy docs), the README's job is routing: a table or list mapping topics to files. This is the pattern this repository's own `README.md` uses — directory tables with one row per file, a layer column, and a relationship tree — and it is what an agent reads to find the right file without dumping the repo [1].

- One row per entry: name, a one-line description, and a link.
- Descriptions must say what the target *covers*, not praise it.
- Link text must describe the target's content ("[AI-Friendly Plan Authoring](misc/ai-friendly-planning.md) — standards for agent-executable plans"), never "click here".
- Keep the map shallow: group by directory, cap descriptions to one line, and let agents fetch depth on demand.

### Rule 5 — Text Equivalents for AI-Invisible Media

Badges, images, emoji, ASCII art, and merged tables carry information visually that plain-text parsing discards [4]. Never make the only copy of a fact visual.

- Replace a badge row with a one-line "Status: ..." text list or keep badges *below* the text facts.
- Give every meaningful diagram a numbered step-list text equivalent, then keep the image as a supplement.
- Avoid emoji as the sole carrier of a label (the layer badges in this repo's README are paired with explicit hot/warm/cold names for exactly this reason).
- Avoid merged/multi-header tables; if a table's meaning lives in the arrangement of cells, convert it to a bulleted list per item [4].
- ASCII diagrams are text and usually survive; still give them a plain-sentence summary.

### Rule 6 — Write for Retrieval

Write so that any *section* answers its question in isolation, with consistent terminology [4].

- Self-contained sections: each section states its own context rather than depending on a linear read ("now that you've configured...", "as mentioned above" are retrieval-death).
- Consistent terminology: name the product/project explicitly in sections; retrieval matches on terms present in the chunk [4].
- Progressive-disclosure file lists: end the README with a short list of where deeper detail lives (docs directory, per-feature files), llms.txt-style `[name](url): one-line note` [1].
- One idea per sentence; prefer bullets; keep the whole file small — detail lives behind links, not in the README [1][3].

## Anti-Patterns

- **Marketing-first ordering** — hero images, animated GIFs, and hype before one useful fact. Agents that read top-down may never reach the real content.
- **Layout-dependent meaning** — tables that only make sense when rendered, columns aligned by whitespace, badges that encode facts. Plain-text parsers lose all of it.
- **Commands implied, not stated** — "requires Node and a database" instead of `nvm use && npm ci && npm run dev`.
- **Vague links** — "see our docs" with no URL, or link text that says nothing about the target.
- **Terminology soup** — the same concept called "auth", "login", and "identity" in different sections, so retrieval misses chunks [4].
- **Wall-of-text single sections** — no headings; chunked retrievers can't target them [4].
- **Freshness neglect** — a README whose install commands have rotted trains agents to fail; commands are ground truth and must be verified (see Validation).
- **Context stuffing** — inlining the entire manual into the README "for completeness"; that is what links are for [2][3].

## Template

**[Copy-Safe]** — Annotated skeleton. Adapt the sections to the repo type; keep the order.

```markdown
# <Project Name>                                      # 1. H1 = project name

> <One-sentence summary: what it is, for whom.>        # 2. Blockquote = key takeaway

- <Critical facts 3-5: language, toolchain, platforms, NOT-X caveat>  # 3. Facts up front

## Overview                                            # 4. 2-4 sentences, no tutorial

What this is, what problem it solves, who it is for.
For code repos: exact install command in the next block.
For non-code repos: a map of what lives where (Rule 4).

## Installation                                        # 5. Commands as ground truth (code)

    # exact, runnable, with flags
    <install command>

## Usage                                               # 6. Minimal runnable example

    <build / test / lint commands with flags>
    <real output where it disambiguates>

## Documentation                                       # 7. Progressive-disclosure index
- [Guides](docs/): one-line note per area
- [API reference](docs/api.md): one-line note
- [FAQ](docs/faq.md): one-line note

## Contributing                                        # 8. Stable closing sections
<Where to report issues, contribution flow.>

## License
<SPDX identifier.>
```

**Annotation key:**

| # | Rule | Why |
|---|---|---|
| 1 | H1 = project name | llms.txt v2 requires an H1; it anchors every parser [1] |
| 2 | Blockquote summary | llms.txt v2 "key information necessary for understanding the rest" [1] |
| 3 | Facts up front | first ~30 lines; lost-in-the-middle [2][3] |
| 4 | Overview | 2-4 sentences per repo reference standards |
| 5 | Install commands | commands as ground truth (Rule 3) |
| 6 | Usage with real output | agent can verify against output (Rule 3) |
| 7 | Docs index | progressive disclosure, file lists per llms.txt [1] |
| 8 | Stable closing | predictable skeleton (Rule 2) |

## Validation

The file is AI-effective if a fresh agent, given only the README, can answer without guessing. Probe with three questions, then fix the README until all three pass:

1. "What is this repo, and what is it explicitly not?" — answered by the first 30 lines.
2. "Give me the exact commands to install, build, and test it." — every command exists verbatim, with flags.
3. "Where does the deeper documentation live, by topic?" — answered by the docs index section.

Run the probe with a fresh conversation/agent every time the README changes; commands rot silently. Optionally automate a smoke check that every code-fence command block in the file executes:

**[Copy-Safe]** — extract and run the README's `bash` code fences in a clean environment:

```bash
python - <<'PY'
import re, subprocess, sys
text = open("README.md", encoding="utf-8").read()
blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)
fails = 0
for i, b in enumerate(blocks, 1):
    lines = [l for l in b.strip().splitlines() if not l.lstrip().startswith("#")]
    if not lines:
        continue
    print(f"[{i}] {lines[0][:70]}")
    if subprocess.run(lines, shell=True).returncode != 0:
        fails += 1
sys.exit(1 if fails else 0)
PY
```

Run this in a throwaway container/venv, not the working repo. Note that some commands are intentionally interactive or network-bound; mark those with a `# requires-network` comment and exclude them from the check.

## Related Documents

- [AI-Effective README Reference — Case Studies](ai-effective-readmes-case-study.md) — line-by-line dissection of HowToAI's, uv's, and Claude Cookbooks' READMEs, with before/after rewrites.
- [Best Practices for AGENTS.md Files](../agents/agents-best-practices.md) — the sibling artifact guide; contrasts AGENTS.md vs README.md.

## References

1. Howard, J., "The /llms.txt file, v2," llms-txt.org. https://llmstxt.org/
2. Anthropic, "Effective context engineering for AI agents," Sep 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
3. Agentverse, "README Guidelines," Agentverse Documentation. https://docs.agentverse.ai/documentation/agent-discovery/readme-guidelines
4. kapa.ai, "Writing documentation for AI: best practices," kapa.ai docs. https://docs.kapa.ai/improving/writing-best-practices

---

*Last verified: 2026-08-13 — update this date when content is reviewed or changed.*
