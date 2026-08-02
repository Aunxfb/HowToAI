---
title: AI-Friendly Plan Authoring and Execution -- Evidence
description: Claim-by-claim verification of the seven authoring properties and five execution rules, supporting and contradictory evidence, and all 29 references with citation mapping.
status: active
tags: [ai, planning, agents, evidence, references, verification, handoff]
last_verified: 2026-08-03
layer: cold
applies_to: implementation plans, task checklists, agent-executed work
---

# AI-Friendly Plan Authoring and Execution -- Evidence

## Overview

This document contains the evidence base for [AI-Friendly Plan Authoring and Execution](ai-friendly-planning.md). It records the verification outcome for each original claim, the supporting and contradictory evidence from academic benchmarks and industry engineering practice, and all 29 references with claim mapping. Intended for reviewers who want to verify the standard against the original sources.

---

## Snippet Claim Verification

The original proposal contained 7 authoring properties and 5 execution rules. Verdicts after checking against the evidence below:

### Authoring claims

| # | Original claim | Verdict | What changed |
|---|---|---|---|
| 1 | Self-contained — no external context needed | **Supported, expanded** | Added three requirements the research makes explicit: state non-goals/boundaries (agents cannot know implicit constraints), include the *why* (models generalize from motivation [8]), and note self-contained ≠ everything inlined — lightweight references enable just-in-time retrieval [10] |
| 2 | Executable — clear "what to do" | **Supported, expanded** | Added: include verbatim runnable commands with flags [13][14]; where no deterministic command exists, define the expected artifact instead |
| 3 | Checkable — definition of done | **Supported, expanded with hardening** | Added: prefer deterministic checks (LLM-as-judge needs careful design [20]); verification must be tamper-resistant because specification gaming is measured behavior [5][8] |
| 4 | Isolated — each task can be done independently | **Corrected** | Overstated. Code tasks are inter-dependent by nature (CodePlan: 2–97 inter-dependent files [15]); agents without shared visibility make conflicting implicit decisions [7]. Replaced with: independently executable and verifiable *given declared dependencies*; the plan declares the dependency graph [7][19] |
| 5 | Referenced — links to actual files | **Supported, expanded** | Added: references reconcile self-containment with brevity [10]; verify references resolve at draft time; prefer stable references (paths, symbols, IDs) over volatile ones (line numbers) |
| 6 | Specific — not ambiguous | **Supported, refined** | Added an altitude ceiling: specify what/why/constraints, but over-prescribing the incidental *how* is brittle and blocks valid alternative paths [6][10]; place critical constraints at the top or end, never buried mid-document [22] |
| 7 | Frontmatter/metadata — harness format clarity | **Supported, expanded** | Added: freshness fields (`status`, `last_updated`) are required because plans are living documents [10]; minimum field set defined in the main document |

### Execution claims

| # | Original claim | Verdict | What changed |
|---|---|---|---|
| 1 | Update the plan incrementally | **Supported** | Added mechanics: update at every state change (context can be lost at any point [6][10]); explicit status vocabulary; deviations recorded with reasons |
| 2 | Surface blockers early | **Supported** | Added mechanics: record what is blocked / tried / needed in the plan itself; amend the dependency graph on discovery; escalate *before* destructive actions [8][23] |
| 3 | Keep the checklist honest | **Supported — most safety-critical rule** | Added mechanics: `done` requires captured verification output; an unrunnable check means `blocked`, not `done`; never edit the check to pass [5][8][9] |
| 4 | Preserve intent through divergence | **Supported** | Added mechanics: update description *and* rationale; re-verify remaining tasks; log decisions not just status [7]; reopen falsely-completed tasks |
| 5 | Pass the plan forward | **Supported** | Added mechanics: handoff = checklist + decisions with rationale + blockers + verification evidence + remaining work [7][10]; acceptance test — a fresh agent continues from the plan alone |

No claim was found factually false. One (Isolation) required correction; one (Specificity) required a ceiling; the rest were supported as stated and expanded with mechanics.

---

## Evidence Summary

### Evidence for self-contained tasks

LLMs perform best under single-turn, fully-specified instructions; underspecified multi-turn settings cost 39% average performance across six tasks, because models "make assumptions in early turns and prematurely attempt to generate final solutions" [4]. Anthropic's multi-agent engineering team gives each subagent an objective, an output format, tool/source guidance, and task boundaries — "without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information" [6]. Cognition's first principle: "Share context, and share full agent traces, not just individual messages" [7]. Anthropic's prompting guide operationalizes the test: show the instructions to a context-free colleague; if they would be confused, the model will be too [8]. Claude Code's guidance adds that the most useful specs "name the files and interfaces involved, state what is out of scope" [9].

### Evidence for executable tasks

Spec-driven toolkits treat specifications as executable artifacts [11][12]. The 2,500-repo AGENTS.md analysis found effective files put executable commands early, "with flags and options, not just tool names" [13]. AGENTS.md's own guidance has agents run listed checks and "fix any test or type errors until the whole suite is green" [14]. CodePlan demonstrates the payoff: plans as multi-step chains of concrete edits at specific code locations passed validity checks on 5/6 repositories versus 0/6 for non-planning baselines [15]. Plan-and-Solve shows explicit plan-then-execute beats unstructured zero-shot reasoning across ten datasets [16].

### Evidence for checkable tasks

Anthropic: "Code solutions are verifiable through automated tests," and agents must "gain 'ground truth' from the environment at each step" [17]. Without a runnable check, "looks done" is the only signal and the human becomes the verification loop [9]. SWE-bench scores resolution by repository tests [2]. Reflexion's written-feedback loop against real signals reached 91% pass@1 on HumanEval versus GPT-4's 80% baseline [18]; Self-Refine shows iterative self-feedback improves outputs ~20% absolute on average [28]. Kiro attaches acceptance criteria to every requirement [19]; spec-kit ships requirement checklists described as "unit tests for English" [12].

### Evidence for isolation with declared dependencies (the correction)

The isolation *ideal* is well supported — "each task should be something you can implement and test in isolation," "almost like a test-driven development process for your AI agent" [11]; Anthropic's parallelization workflow notes LLMs do better when each consideration gets a separate, focused call [17]; 12-Factor Agents prescribes small, focused agents [21]. But strict independence is frequently impossible: CodePlan's repository tasks required coordinated edits across 2–97 inter-dependent files, solved via dependency analysis and may-impact analysis [15]. Cognition shows *why* undeclared dependence fails: "Actions carry implicit decisions, and conflicting decisions carry bad results" [7]. Kiro implements the corrected form — a task dependency graph executing independent tasks concurrently in waves [19].

### Evidence for referenced tasks

Anthropic's context engineering guidance: agents built "just in time" keep lightweight identifiers (file paths, stored queries, links) and load data at runtime [10]. Anthropic's multi-agent system has subagents write outputs to the filesystem and pass back condensed references to avoid the "game of telephone" [6]. Claude Code: name the files and interfaces [9]. Kiro tasks trace to requirements and design artifacts [19]. The AGENTS.md analysis recommends explicit read/write directory mapping [13].

### Evidence for specificity at the right altitude

"Most agent files fail because they're too vague" — the 2,500-repo analysis found specific job definitions work and vague personas fail [13]. GitHub's spec-kit post: agents are "literal-minded pair programmers"; a vague prompt "forces the model to guess at potentially thousands of unstated requirements" [11]. Anthropic's prompting guide: be clear and direct, use numbered steps where order matters [8]. The ceiling: Anthropic's context engineering prescribes the "right altitude" — neither brittle hardcoded logic nor vague guidance assuming shared context [10] — and their multi-agent team evaluates end-state outcomes rather than prescribed steps because agents take different valid paths [6]. Placement matters: models use information at the beginning or end of long contexts best, degrading for middle content [22].

### Evidence for structured metadata

AGENTS.md files pair YAML frontmatter with structured sections (role, project knowledge, commands, standards, boundaries) [13][14]. OpenCode defines agents in markdown with YAML frontmatter [23]. Anthropic recommends organizing prompts into distinct sections with headers [10]. Kiro and spec-kit plans follow fixed templates [12][19]. Freshness metadata matters because plans change during execution — see the living-document evidence below.

### Evidence for living-document execution (Rule 1)

Anthropic's agents write NOTES.md and to-do lists persisted outside the context window, re-read after resets [10]; their multi-agent lead saves its plan to memory because the context window will be truncated [6]. ReAct: "reasoning traces help the model induce, track, and update action plans as well as handle exceptions" [24]. Reflexion stores reflective text in an episodic memory buffer to improve subsequent trials [18]. Kiro updates task status in real time [19]; Cline recommends writing the plan to a markdown file and tracking a todo list during execution [25]; the unified agent survey identifies memory as a core agent component [29].

### Evidence for early blocker surfacing (Rule 2)

"Agents can then pause for human feedback at checkpoints or when encountering blockers," with stopping conditions such as maximum iterations [17]. 12-Factor Agents makes human contact a first-class structured tool call [21]. OpenCode's `ask` permissions gate risky tools, and its step limit forces a summary of work and remaining tasks [23]. Anthropic's prompting guide instructs agents to ask before hard-to-reverse or shared-system actions [8].

### Evidence for checklist honesty (Rule 3)

Training in gameable environments increases specification gaming; "a small but non-negligible proportion of the time, LLM assistants trained on the full curriculum generalize zero-shot to directly rewriting their own reward function" — and retraining mitigates but does not eliminate it [5]. Anthropic's countermeasures: ground truth from the environment at each step [17], evidence over assertion (show the test output) [9], immutable tests ("unacceptable to remove or edit tests") [8], and fresh-context review of the diff against the plan [9]. SWE-bench's resolution bar is repository tests passing [2]; AGENTS.md's bar is "the whole suite is green" [14].

### Evidence for intent preservation (Rule 4)

Spec-kit's course-correction loop: update the spec, regenerate the plan, re-execute — with cross-artifact consistency analysis (`/speckit.analyze`) before implementation [11][12]. Cline: return to plan mode when execution hits unexpected complexity rather than pushing through [25]. Cognition's second principle: unrecorded deviations silently invalidate downstream work built on conflicting assumptions [7]. Multi-turn research: "when LLMs take a wrong turn in a conversation, they get lost and do not recover" [4].

### Evidence for plan-forward handoff (Rule 5)

Anthropic's compaction preserves architectural decisions, unresolved bugs, and implementation details, with structured notes re-read after resets [10]; their multi-agent system spawns fresh agents with clean contexts and maintains continuity through stored plans and careful handoffs [6]. LangChain's taxonomy — write, select, compress, isolate — covers scratchpads, trajectory summarization, and context splitting [26]. Cognition compresses history into "key details, events, and decisions" [7]. OpenCode's step limit triggers a work summary plus recommended remaining tasks [23]; Cline carries full planning context into execution [19]. Voyager's executable skill library transferring zero-shot to new worlds shows durable artifacts outperform durable contexts [27].

---

## Contradictory Evidence and How to Interpret It

### Claim: "LLMs can generate their own plans at runtime, so authoring barely matters."

PlanBench contradicts this directly: "on many critical capabilities — including plan generation — LLM performance falls quite short, even with the SOTA models" [1]. Plan-and-Solve shows explicit plans improve even zero-shot reasoning [16], and CodePlan shows planning-based execution succeeding where non-planning baselines fail entirely (5/6 vs 0/6) [15].

**Interpretation:** The plan must be authored, explicit, and external. Runtime planning is a supplement, not a substitute.

### Claim: "LLM-as-judge verification can replace deterministic checks."

The LLM-as-a-Judge survey finds the approach scalable and cost-effective but that reliability "remains a significant challenge that requires careful design and standardization" [20].

**Interpretation:** Use deterministic checks (tests, builds, linters) as the primary gate; reserve model-based judgment for criteria with no deterministic form, and design those checks deliberately.

### Claim: "More detail always helps."

Anthropic's "right altitude" guidance [10] and the multi-agent practice of evaluating outcomes rather than prescribed steps [6] contradict pure more-is-better. Over-specification produces brittle plans that break on first surprise.

**Interpretation:** Maximize specificity of outcomes, constraints, boundaries, and verification; leave incidental implementation latitude to the executor.

### Claim: "Tasks can always be made independent."

CodePlan's inter-dependent edits (2–97 files) [15] and Cognition's implicit-decision failures [7] contradict universal independence.

**Interpretation:** Independence is the target, declared dependence is the requirement. The dependency graph is a first-class section of the plan [19].

### Claim: "Agents will report completion honestly if instructed to."

Reward-tampering research contradicts reliance on instruction alone [5]. The same paper notes false positives — models editing rewards while attempting honest completion — so the failure is not always malicious.

**Interpretation:** Never rely on instruction or intent. Make verification external, deterministic where possible, and immutable by the executor [8][9].

### Claim: "Long context windows remove the need for notes and handoffs."

"Lost in the Middle" shows models do not robustly use long-context information [22], and production harnesses still compact, summarize, and persist notes by design [10][23][26].

**Interpretation:** Treat the plan file as the durable record regardless of context size.

---

## References

> Each reference includes the claims it supports so reviewers can verify the standard directly.

### 1. PlanBench — LLM Planning Benchmark

**Reference:** Valmeekam, Marquez, Olmo, Sreedharan, Kambhampati, "PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change," NeurIPS 2023 Track on Datasets and Benchmarks.
**Link:** https://arxiv.org/abs/2206.10498
**Supports:**

* LLMs are weak native planners; plan generation "falls quite short, even with the SOTA models."
* Prior planning claims conflate planning with retrieval from world knowledge.
* Formal planning domains provide objective correctness criteria.

**Use in standard:** Primary motivation for requiring authored, explicit, external plans.

---

### 2. SWE-bench — Real-World GitHub Issue Resolution

**Reference:** Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan, "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?," ICLR 2024.
**Link:** https://arxiv.org/abs/2310.06770
**Supports:**

* 2,294 real issues across 12 Python repositories; resolution verified by repository tests.
* At introduction, the best model (Claude 2) resolved 1.96% of issues.
* Real tasks require coordinating changes across functions, classes, and files.

**Use in standard:** Motivation (long-horizon failure) and the model for objective, test-based definitions of done.

---

### 3. TheAgentCompany — Professional Task Benchmark

**Reference:** Xu, Song, Li, et al., "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks," 2024.
**Link:** https://arxiv.org/abs/2412.14161
**Supports:**

* The most competitive agent completed 30% of professional tasks autonomously.
* "More difficult long-horizon tasks are still beyond the reach of current systems."
* Self-contained environments enable objective scoring.

**Use in standard:** Motivation for incremental, checkpointed, verifiable plan execution.

---

### 4. LLMs Get Lost In Multi-Turn Conversation

**Reference:** Laban, Hayashi, Zhou, Neville, "LLMs Get Lost In Multi-Turn Conversation," 2025.
**Link:** https://arxiv.org/abs/2505.06120
**Supports:**

* All tested open- and closed-weight LLMs drop an average of 39% in multi-turn (underspecified) versus single-turn fully-specified settings, across six generation tasks.
* Degradation decomposes into minor aptitude loss and major unreliability increase; models make early assumptions and over-rely on premature solutions.
* "When LLMs take a wrong turn in a conversation, they get lost and do not recover."

**Use in standard:** Core citation for self-containment (Property 1), full upfront specification (Property 6), and deviation logging (Rule 4).

---

### 5. Sycophancy to Subterfuge — Reward-Tampering

**Reference:** Denison, MacDiarmid, Barez, et al., "Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models," 2024 (Anthropic-affiliated authors).
**Link:** https://arxiv.org/abs/2406.10162
**Supports:**

* Training on easily-gamed environments increases specification gaming on remaining environments.
* Models generalize zero-shot to rewriting their own reward function; retraining mitigates but does not eliminate tampering.
* Caveat: some operationalized tampering cases were honest-completion false positives.

**Use in standard:** Primary evidence for tamper-resistant verification (Property 3) and checklist honesty (Rule 3).

---

### 6. Anthropic — Multi-Agent Research System

**Reference:** Anthropic, "How we built our multi-agent research system," Jun 2025.
**Link:** https://www.anthropic.com/engineering/built-multi-agent-research-system
**Supports:**

* Subagents need an objective, output format, tool/source guidance, and clear task boundaries; vague descriptions cause duplicated work and gaps.
* The lead agent saves its plan to memory because context windows truncate; fresh subagents plus stored plans maintain continuity.
* Subagents write outputs to the filesystem and pass back lightweight references ("game of telephone" avoidance).
* Evaluate end-state outcomes, not prescribed steps; break evaluations into discrete checkpoints.

**Use in standard:** Properties 1, 5, 6 (altitude ceiling) and Rules 1, 5.

---

### 7. Cognition — Don't Build Multi-Agents

**Reference:** Yan, Cognition, "Don't Build Multi-Agents," Jun 2025.
**Link:** https://cognition.ai/blog/dont-build-multi-agents
**Supports:**

* Principle 1: "Share context, and share full agent traces, not just individual messages."
* Principle 2: "Actions carry implicit decisions, and conflicting decisions carry bad results."
* Long tasks need history compressed into key details, events, and decisions.
* Context engineering is effectively the top job of agent builders.

**Use in standard:** Properties 1, 4 (the correction) and Rules 4, 5.

---

### 8. Anthropic Docs — Prompting Best Practices

**Reference:** Anthropic Docs, "Prompting best practices" (includes "Be clear and direct").
**Link:** https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct
**Supports:**

* Golden rule: if a context-free colleague would be confused by the instructions, the model will be too.
* Numbered sequential steps when order matters; providing motivation behind instructions improves generalization.
* Long-horizon state tracking via structured files and progress notes; tests written before work and treated as immutable.
* Ask the user before hard-to-reverse or shared-system actions.

**Use in standard:** Properties 1, 3 (immutable checks), 6 and Rules 2, 3.

---

### 9. Anthropic — Claude Code Best Practices

**Reference:** Anthropic, "Claude Code best practices."
**Link:** https://www.anthropic.com/engineering/claude-code-best-practices
**Supports:**

* Give the agent a check it can run — tests, a build, a screenshot diff — otherwise "looks done" is the only signal.
* The most useful specs are self-contained: they name the files and interfaces involved and state what is out of scope.
* Evidence over assertion: show test output rather than claiming success; fresh-context subagent review of diffs against the plan.
* Explore → plan → implement workflow; clear context between unrelated tasks.

**Use in standard:** Properties 1, 3, 5 and Rule 3.

---

### 10. Anthropic — Effective Context Engineering for AI Agents

**Reference:** Anthropic, "Effective context engineering for AI agents," Sep 2025.
**Link:** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Supports:**

* Context is finite; curate the smallest high-signal token set; prompts need the "right altitude."
* "Just in time" agents keep lightweight identifiers (file paths, stored queries, links) and load data at runtime.
* Compaction must preserve architectural decisions, unresolved bugs, and implementation details.
* Structured note-taking: NOTES.md and to-do lists persisted outside the context window, re-read after resets; sub-agents return condensed summaries.

**Use in standard:** Properties 1, 5, 6, 7 and Rules 1, 5.

---

### 11. GitHub Blog — Spec-Driven Development with AI

**Reference:** Delimarsky, GitHub Blog, "Spec-driven development with AI: Get started with a new open source toolkit," Sep 2025.
**Link:** https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
**Supports:**

* Agents are "literal-minded pair programmers"; vague prompts force the model to guess thousands of unstated requirements.
* "Each task should be something you can implement and test in isolation" — "almost like a test-driven development process for your AI agent."
* Four phases (Specify, Plan, Tasks, Implement) with checkpoints; no advancing until the current phase is validated.
* Course correction = update the spec, regenerate the plan, re-execute; concrete task example: "create a user registration endpoint that validates email format."

**Use in standard:** Properties 2, 4, 6 and Rule 4.

---

### 12. GitHub — Spec Kit

**Reference:** GitHub, "Spec Kit" repository.
**Link:** https://github.com/github/spec-kit
**Supports:**

* Fixed pipeline: constitution → specify → plan → tasks → implement; validation commands clarify, analyze (cross-artifact consistency), and checklist ("unit tests for English").
* Templates enforce organizational standards, including test-first task ordering and review gates.

**Use in standard:** Properties 2, 3, 7 and Rule 4 (consistency analysis before implementation).

---

### 13. GitHub Blog — AGENTS.md Lessons from 2,500+ Repositories

**Reference:** Nigh, GitHub Blog, "How to write a great agents.md: Lessons from over 2,500 repositories," Nov 2025.
**Link:** https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
**Supports:**

* "Most agent files fail because they're too vague"; specific job definitions work.
* Executable commands early, with flags; exact stack versions and file locations; explicit read/write directory mapping.
* Three-tier boundaries (always do / ask first / never do); "Never commit secrets" the most common helpful constraint.
* Self-validation commands so agents check their own work; "The best agent files grow through iteration, not upfront planning."

**Use in standard:** Properties 1, 2, 5, 6, 7 and Rule 1 (iteration).

---

### 14. AGENTS.md — Open Format

**Reference:** AGENTS.md project.
**Link:** https://agents.md/
**Supports:**

* "A README for agents": a dedicated, predictable place for context and instructions, plain markdown.
* Runnable setup/build/test commands; agents run listed checks and "fix any test or type errors until the whole suite is green."
* Nested files: the closest file to the edited file takes precedence.

**Use in standard:** Properties 2, 3, 7 and Rule 3.

---

### 15. CodePlan — Repository-Level Coding via Planning

**Reference:** Bairi, Sonwane, Kanade, et al., "CodePlan: Repository-level Coding using LLMs and Planning," 2023.
**Link:** https://arxiv.org/abs/2309.12499
**Supports:**

* Repository tasks are inter-dependent; solutions need a multi-step chain of edits at specific code locations with repo-derived context.
* Dependency analysis + change may-impact analysis + adaptive planning.
* 5/6 repositories passed validity checks with planning; 0/6 without.

**Use in standard:** Property 2 (executable edit steps), Property 4 (why strict independence fails and dependency declaration works), Property 5.

---

### 16. Plan-and-Solve Prompting

**Reference:** Wang, Xu, Lan, et al., "Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models," ACL 2023.
**Link:** https://arxiv.org/abs/2305.04091
**Supports:**

* "First, devising a plan to divide the entire task into smaller subtasks, and then carrying out the subtasks according to the plan."
* PS+ beats zero-shot chain-of-thought on all ten evaluated datasets; more detailed instructions reduce errors.

**Use in standard:** Property 2 (plan-then-execute) and Property 4 (subtask decomposition).

---

### 17. Anthropic — Building Effective Agents

**Reference:** Anthropic (Schluntz, Zhang), "Building effective agents," Dec 2024.
**Link:** https://www.anthropic.com/engineering/building-effective-agents
**Supports:**

* "Code solutions are verifiable through automated tests"; agents iterate on test feedback; quality is objectively measurable.
* Agents must "gain 'ground truth' from the environment at each step"; "Agents can then pause for human feedback at checkpoints or when encountering blockers"; include stopping conditions.
* Prompt chaining with programmatic gates between subtasks; parallel sectioning improves focused considerations; evaluator-optimizer loops.
* Invest in agent-computer interfaces: poka-yoke (e.g., require absolute file paths), clear tool docs.

**Use in standard:** Properties 2, 3, 4 and Rules 2, 3.

---

### 18. Reflexion — Verbal Reinforcement Learning

**Reference:** Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao, "Reflexion: Language Agents with Verbal Reinforcement Learning," NeurIPS 2023.
**Link:** https://arxiv.org/abs/2303.11366
**Supports:**

* "Reflexion agents verbally reflect on task feedback signals, then maintain their own reflective text in an episodic memory buffer to induce better decision-making in subsequent trials."
* 91% pass@1 on HumanEval, surpassing the prior GPT-4 baseline of 80%.

**Use in standard:** Property 3 (feedback-driven verification) and Rule 1 (written state improves subsequent execution).

---

### 19. Kiro — Specs Documentation

**Reference:** Kiro (AWS), "Specs" documentation.
**Link:** https://kiro.dev/docs/specs/
**Supports:**

* Three artifacts: requirements.md (user stories + acceptance criteria), design.md, tasks.md ("a detailed implementation plan with discrete, trackable tasks"), with approval gates between phases.
* Task status updates in real time; "Run all Tasks" builds a dependency graph and runs independent tasks concurrently in waves.
* Requirements analysis catches inconsistencies, ambiguities, and gaps before design.

**Use in standard:** Properties 3, 4 (dependency waves), 5, 7 and Rule 1.

---

### 20. LLM-as-a-Judge Survey

**Reference:** Gu, Jiang, Shi, et al., "A Survey on LLM-as-a-Judge," 2024.
**Link:** https://arxiv.org/abs/2411.15594
**Supports:**

* LLM-based judgment is scalable and cost-effective, but reliability "remains a significant challenge that requires careful design and standardization."
* Surveys consistency improvement, bias mitigation, and judge-reliability evaluation.

**Use in standard:** Property 3 hardening clause — deterministic checks primary, model-based judgment deliberate.

---

### 21. 12-Factor Agents

**Reference:** Horthy, HumanLayer, "12-Factor Agents."
**Link:** https://github.com/humanlayer/12-factor-agents
**Supports:**

* Own your prompts and context window; own your control flow; tools are structured outputs.
* Contact humans with tool calls — escalation is a first-class output.
* Compact errors into the context window; small, focused agents; unify execution state and business state.

**Use in standard:** Property 4 (small tasks) and Rule 2 (human escalation as mechanism).

---

### 22. Lost in the Middle — Long-Context Degradation

**Reference:** Liu, Lin, Hewitt, et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL 2024.
**Link:** https://arxiv.org/abs/2307.03172
**Supports:**

* "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle."
* Holds even for models explicitly designed for long contexts.

**Use in standard:** Property 6 (constraint placement) and the caution against relying on long contexts instead of notes.

---

### 23. OpenCode — Agents Documentation

**Reference:** OpenCode, "Agents" documentation.
**Link:** https://opencode.ai/docs/agents/
**Supports:**

* Built-in Plan agent analyzes code and creates plans "without making any actual modifications"; Explore/Scout subagents are read-only.
* Fine-grained `ask`/`allow`/`deny` permissions; step limits force "a summarization of its work and recommended remaining tasks."
* Agents defined via markdown with YAML frontmatter.

**Use in standard:** Properties 5 (read-only research before drafting), 7 and Rules 2, 5.

---

### 24. ReAct — Reasoning and Acting

**Reference:** Yao, Zhao, Yu, Du, Shafran, Narasimhan, Cao, "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023.
**Link:** https://arxiv.org/abs/2210.03629
**Supports:**

* "Reasoning traces help the model induce, track, and update action plans as well as handle exceptions."
* Outperforms imitation/RL baselines by an absolute 34% (ALFWorld) and 10% (WebShop) success rate; grounding via environment interaction overcomes hallucination.

**Use in standard:** Rules 1, 2, 4 (continuous plan tracking, exception handling, replanning).

---

### 25. Cline — Plan & Act Mode

**Reference:** Cline, "Plan & Act Mode" documentation.
**Link:** https://docs.cline.bot/core-workflows/plan-and-act.md
**Supports:**

* Plan mode is read-only research ("can read your codebase, run searches, and discuss strategy, but cannot modify any files or execute commands"); context carries into Act mode.
* Return to Plan mode when hitting unexpected complexity rather than pushing through.
* Recommended: write the plan to a markdown file, track a todo list during execution, enable checkpoints for rollback.

**Use in standard:** Properties 5 (verify references before drafting) and Rules 1, 4, 5.

---

### 26. LangChain — Context Engineering for Agents

**Reference:** LangChain, "Context Engineering for Agents," Jul 2025.
**Link:** https://blog.langchain.com/context-engineering-for-agents/
**Supports:**

* Four strategies: write, select, compress, isolate context; scratchpads save plans outside the context window.
* Long contexts fail via poisoning, distraction, confusion, and clash; compress trajectories to required tokens.

**Use in standard:** Rules 1 and 5 (the write/compress/isolate playbook for living plans and handoffs).

---

### 27. Voyager — Open-Ended Embodied Agent

**Reference:** Wang, Xie, Jiang, et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models," TMLR 2024.
**Link:** https://arxiv.org/abs/2305.16291
**Supports:**

* "A new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification for program improvement."
* An ever-growing skill library of executable code transfers zero-shot to new worlds; 3.3x more unique items than prior SOTA.

**Use in standard:** Property 3 (self-verification with environment feedback) and Rule 5 (durable artifacts beat durable contexts).

---

### 28. Self-Refine — Iterative Self-Feedback

**Reference:** Madaan, Tandon, Gupta, et al., "Self-Refine: Iterative Refinement with Self-Feedback," NeurIPS 2023.
**Link:** https://arxiv.org/abs/2303.17651
**Supports:**

* One model acts as generator, feedback provider, and refiner; outputs "improving by ~20% absolute on average in task performance" over one-step generation.

**Use in standard:** Supporting evidence for feedback-loop verification (Property 3).

---

### 29. Survey on LLM-Based Autonomous Agents

**Reference:** Wang, Ma, Feng, et al., "A Survey on Large Language Model based Autonomous Agents," Frontiers of Computer Science, 2024.
**Link:** https://arxiv.org/abs/2308.11432
**Supports:**

* Unified agent framework: profile, memory, planning, and action components — memory and planning are distinct, both required.

**Use in standard:** Background support for treating the plan file as the agent's external planning+memory component.

---

## Related Documents

- [AI-Friendly Plan Authoring and Execution](ai-friendly-planning.md) — the standard this evidence supports.
- [Reference File Standards](reference-standards.md) — the conventions this document follows.
- [AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence](ai-vs-sast-comparison-evidence.md) — the evidence-file pattern this document mirrors.

---

*Last verified: 2026-08-03 — update this date when content is reviewed or changed.*
