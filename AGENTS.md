# AGENTS.md

Project-level rules for AI agents working in this repository. Auto-loaded at session start by AGENTS.md-aware harnesses (OpenCode, Claude Code, Codex, Copilot, etc.).

## Overview

This repository is a knowledge base of Applied AI reference documents. Files are organized by progressive-disclosure layers so agents can load only what a task needs. Load lazily; never dump the whole repo into context.

## Adding New (External) References
When adding new references or best practice guide not drafted within this repo, check the `toadd` folder, then also reference the `reference-standards.md` and `reference-template.md` to make sure the newly added references are comforming to the repo convention. Evaluate if the reference file itselfcan be split for more effective guidance and make recommendations.

After all candidates are added, run the regenerate_index.py script to udpate the index under README.md.

## Loading Protocol

1. **This file** is already in context. Treat it as the entry point.
2. **Read `README.md`** — the index and router. Use its directory tables to map a task to files, and its relationship tree to see which cold files (❄️) belong to which warm overview (☀️).
3. **Hot files (🔥)** — sized under 100 lines for always-in-context use. Load them whenever working in their domain.
4. **Warm files (☀️)** — task-specific guides (100-500 lines). Load only the ones whose scope matches the current task.
5. **Cold files (❄️)** — deep references (500+ lines): evidence bases, deep dives, templates, appendices. Fetch via their links only when the task actually requires the depth.
6. **Follow `## Related Documents` sections** for deeper context within a topic.

Layer defaults (when a file has no `layer` field): root files default to `hot`, subdirectory files default to `warm`. See `documentation/reference-standards.md` for the full layer definitions and quality rules.

## Conventions

- **Edit only what the task requires.** Do not add code comments unless asked.
- **Never commit secrets.**
- **Keep reference files standards-compliant** — follow `documentation/reference-standards.md` (frontmatter, section headings, layer sizing).
- **After adding, renaming, or re-linking reference files**, regenerate the README index:

  ```
  python regenerate_index.py
  ```

  Requires PyYAML. The script reads `utf-8-sig` and writes LF line endings, so it is safe on both Windows and Unix.
- **Update `last_verified`** in a reference file's frontmatter whenever its content changes.
