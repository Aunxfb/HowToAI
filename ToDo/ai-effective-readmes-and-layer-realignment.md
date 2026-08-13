---
title: AI-Effective README Reference + Layer Rule Realignment
status: in_progress
last_updated: 2026-08-13
harness: plain
---

# AI-Effective README Reference + Layer Rule Realignment

## Goal

1. Add a warm reference `misc/ai-effective-readmes.md` — rules for making `README.md` files effective for AI agents, plus a copy-safe template and a validation section.
2. Add a cold companion `misc/ai-effective-readmes-case-study.md` — a comparative case study dissecting real READMEs (HowToAI's own as the primary non-code example, plus one code repo and one docs site), line-by-line, with before/after rewrites.
3. Loosen the layer↔line-count rule in `reference-standards.md` from "MUST" to guidance, so layers are classified by **loading intent**, not line count.
4. Reclassify three existing files whose layers do not match their loading intent.
5. Regenerate the README index and commit.

## Non-Goals

- Do NOT rewrite the body content of any existing reference file — only frontmatter `layer` + `last_verified` changes for reclassified files.
- Do NOT change hot/warm/cold semantics beyond dropping the hard line-count requirement.
- Do NOT add a generic "how to write a good README" guide. The spine stays: *A README is the first context an agent has for an unfamiliar repo — dual-audience, humans scan it, agents execute from it.*
- Do NOT relax the rule for `hot`: hot files must stay small because they are always in context (that reasoning is why the guidance exists).

## Context and References

- `documentation/reference-standards.md` — the file being amended (layer table ~line 33, frontmatter rule ~line 88, quality checklist ~line 253).
- `regenerate_index.py` — README legend hardcodes size ranges at ~line 205.
- `AGENTS.md` — Loading Protocol size language at lines 18-20.
- `documentation/reference-template.md` — frontmatter comment at line 7.
- `agents/agents-best-practices.md` — the sibling artifact guide; explicitly contrasts AGENTS.md vs README.md.
- `misc/ai-friendly-planning.md` — the plan-authoring standard this plan follows.
- `misc/ai-friendly-planning-evidence.md` — evidence-base precedent (cold) that new cold files emulate.
- Research grounding (from web research):
  - llms.txt v2 (AnswerDotAI/Howard) — H1 + blockquote summary + file lists; "keep the file small; detail lives behind links; test by asking an agent."
  - Agentverse README guidelines — Overview → Features → Usage → Examples → Limitations; markdown only.
  - Anthropic "Effective context engineering" — smallest set of high-signal tokens; progressive disclosure; lost-in-the-middle.
  - kapa.ai "Writing content for AI" — chunking, self-contained sections, text equivalents for visuals, no layout-dependent meaning.

## Verification

- Full-suite check: `python regenerate_index.py` runs without errors and README index reflects new files + reclassifications.
- Grep check: `grep -rn "MUST match the size target" documentation/` returns nothing; `grep -rn "line count" regenerate_index.py AGENTS.md documentation/reference-template.md` returns only guidance wording.
- Quality check: both new files pass the checklist in `documentation/reference-standards.md`; frontmatter `layer` + `last_verified` present.
- Reclassification check: `grep -l "^layer:" security/ai-vs-sast-comparison-evidence.md design/llm-budget-friendly-design-appendix.md agents/opencode-claude-codex-porting.md` shows cold/cold/warm respectively.

## Tasks

- [ ] **T1: Amend `documentation/reference-standards.md`** — change size targets from MUST to guidance.
  - Depends on: none
  - Edit: layer table (~line 33-38) — retitle "Size Target" column to "Size Guidance"; add sentence: "Classify by loading intent; line counts are token-budget guidance, not enforcement." Frontmatter field rule (~line 88) — remove "line count **MUST** match"; replace with "size targets are guidance; classify by loading intent." Quality checklist (~line 253) — reword to "File length is sensible for its loading intent (hot stays small); line counts are guidance."
  - Verify: `grep -n "MUST match" documentation/reference-standards.md` → no output. Bump `last_verified` to today.

- [ ] **T2: Amend `regenerate_index.py`** — update the README legend line (~205).
  - Depends on: T1
  - Edit: change "(< 100 lines), ☀️ warm (100-500), ❄️ cold (500+)" to a loading-intent description, e.g. "🔥 always in context, ☀️ task-loaded, ❄️ fetched via links. Sizes are guidance, not limits."
  - Verify: `python regenerate_index.py` regenerates cleanly; README legend no longer states hard ranges.

- [ ] **T3: Amend `AGENTS.md`** — update Loading Protocol size language (lines 18-20).
  - Depends on: T1
  - Edit: reword "sized under 100 lines", "(100-500 lines)", "(500+ lines)" to loading-intent definitions with sizes as guidance only.
  - Verify: `grep -n "lines" AGENTS.md` → no hard-size enforcement language remains.

- [ ] **T4: Amend `documentation/reference-template.md`** — frontmatter comment (line 7).
  - Depends on: T1
  - Edit: replace `# must match file length: hot<100, warm 100-500, cold 500+` with `# classify by loading intent; sizes are guidance, not limits`.
  - Verify: `grep -n "must match file length" documentation/reference-template.md` → no output.

- [ ] **T5: Reclassify `security/ai-vs-sast-comparison-evidence.md`** warm → cold.
  - Depends on: T1
  - Edit: frontmatter `layer: cold`; bump `last_verified`.
  - Verify: `grep "^layer:" security/ai-vs-sast-comparison-evidence.md` → `layer: cold`. It is an evidence base — fetch-on-demand.

- [ ] **T6: Reclassify `design/llm-budget-friendly-design-appendix.md`** warm → cold.
  - Depends on: T1
  - Edit: frontmatter `layer: cold`; bump `last_verified`.
  - Verify: `grep "^layer:" design/llm-budget-friendly-design-appendix.md` → `layer: cold`. It is an appendix — fetch-on-demand.

- [ ] **T7: Reclassify `agents/opencode-claude-codex-porting.md`** cold → warm.
  - Depends on: T1
  - Edit: frontmatter `layer: warm`; bump `last_verified`.
  - Verify: `grep "^layer:" agents/opencode-claude-codex-porting.md` → `layer: warm`. It is a field guide for a recurring task.
  - Note: relationship tree nests companions under warm overviews regardless of layer (regenerate_index.py handles warm↔warm via out-degree); re-run T10 to confirm tree shape.

- [ ] **T8: Create `misc/ai-effective-readmes.md`** (warm, ~250-350 lines).
  - Depends on: T1 (uses loosened rule), T2
  - Sections (per standards skeleton): Overview; Background (AI-consumption model: full-context vs chunked vs crawled); Core Concepts; Rules in order: (1) front-load critical facts in first ~30 lines, (2) blockquote summary + predictable skeleton, (3) commands as ground truth (code repos), (4) index/map pattern for non-code repos (this repo's README as reference), (5) text equivalents for AI-invisible media (badges/images/emoji/ASCII/merged tables), (6) retrieval-friendliness (self-contained sections, consistent terminology, progressive-disclosure file lists per llms.txt pattern); Anti-Patterns; a `[Copy-Safe]` annotated template; `## Validation` (fresh agent, README-only probe); `## Related Documents` linking to the cold companion and `agents-best-practices.md`; `## References` (the four research sources).
  - Verify: passes reference-standards checklist; `grep -c "^##" misc/ai-effective-readmes.md` ≥ 8; layer warm.

- [ ] **T9: Create `misc/ai-effective-readmes-case-study.md`** (cold, comparative).
  - Depends on: T8
  - Sections: Overview; Method; Case Study A — HowToAI README (primary non-code example: index tables, layer column, relationship tree — what an agent reads, what works, gaps); Case Study B — a representative code-repo README (commands-as-ground-truth analysis); Case Study C — a docs-site README (progressive-disclosure index); Cross-Case Patterns; before/after rewrites (`[Copy-Safe]`); `## Related Documents` → main guide; `## References`.
  - Verify: frontmatter `layer: cold`; ≥ 3 case studies present; passes checklist.

- [ ] **T10: Regenerate the index**.
  - Depends on: T2, T3, T4, T5, T6, T7, T8, T9
  - Run: `python regenerate_index.py`
  - Verify: exit code 0; README.md directory tables show the two new misc/ files and updated layer badges; relationship tree nests case study under the main guide. Inspect the ToDo plan file is NOT indexed (ToDo/ is not a reference section — add `ToDo` to `EXCLUDED_DIRECTORIES` in `regenerate_index.py` if it appears).

- [ ] **T11: Final quality pass + commit**.
  - Depends on: T10
  - Run the repo's quality checklist against the two new files and the four amended files. Run `python regenerate_index.py` once more to confirm idempotence (no changes). Stage reference files + README + regenerate script; commit message: `Add AI-effective README reference; classify layers by loading intent`.
  - Verify: `git status` shows only intended files; README regenerated is idempotent.

## Decisions Log

- 2026-08-13: Scope is general-purpose (READMEs in any repo), advisory, non-code-repo inclusive — sibling of ai-friendly-planning in spirit, not content.
- 2026-08-13: Resolve human-marketing vs machine-actionability conflict by fixed layout order (blockquote pitch → machine facts → marketing/visuals), not by prioritizing an audience.
- 2026-08-13: Main file is warm rules+template+validation; case study is a cold comparative companion (single-repo dissection would not legitimately reach cold depth; comparative does).
- 2026-08-13: Layer classification axis is loading intent, NOT importance — evidence bases stay cold despite being essential.
- 2026-08-13: Line-count targets become guidance-only, enforced in 4 files (reference-standards, regenerate_index.py, AGENTS.md, reference-template.md).

## Blockers

- none

## Handoff Notes

- All research sources for the two new files are captured in this plan's Context section; full URLs are in the fetched references (llms.txt v2, kapa.ai, Anthropic context engineering, Agentverse README guidelines).
- The cold case study needs real README content pulled from GitHub for Cases B and C — verify the URLs resolve before writing (plan-mode exploration first).
- After this plan executes, future new-reference ideas/planning go into `ToDo/` (per the AGENTS.md update).
