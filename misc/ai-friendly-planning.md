---
title: AI-Friendly Plan Authoring and Execution
description: Standards for drafting implementation plans that AI agents can execute autonomously and incrementally, and the rules agents must follow when executing them. Backed by published research and industry engineering practice.
status: active
tags: [planning, agents, ai-friendly, documentation, execution, handoff, verification]
last_verified: 2026-08-03
layer: warm
applies_to: implementation plans, task checklists, agent-executed work, any harness
---

# AI-Friendly Plan Authoring and Execution

## Overview

This reference defines how to draft implementation plans that AI agents can execute without the original author or conversation context, and how agents must behave while executing such plans. It is written for both audiences: humans (or agents) authoring plans, and agents executing them. Each rule carries a verdict against the published evidence — most source claims held up; two required correction or refinement. The full claim-by-claim verification, contradictory evidence, and citations live in the [evidence document](ai-friendly-planning-evidence.md).

## Background

Human-friendly plans rely on shared context: shorthand, implicit dependencies, and unspoken definitions of done. AI executors have none of that context, and four measured failure modes make the gap expensive:

- **LLMs are weak native planners.** On PlanBench, a benchmark built from International Planning Competition domains, "LLM performance falls quite short, even with the SOTA models" on plan generation [1]. A plan cannot be left to emerge at runtime; it must be written down explicitly.
- **Frontier agents fail long-horizon work.** At introduction, the best model on SWE-bench (real GitHub issues) resolved 1.96% of tasks [2]; the best agent in TheAgentCompany's simulated firm completed 30% of professional tasks autonomously [3]. Capability improves, but the failure pattern persists: partial completion, lost coordination, silent divergence.
- **Context degrades and is lost.** Across six generation tasks, LLMs averaged a 39% performance drop in multi-turn (underspecified) settings versus single-turn fully-specified ones, because they "make assumptions in early turns and prematurely attempt to generate final solutions" — "when LLMs take a wrong turn in a conversation, they get lost and do not recover" [4]. Long contexts also degrade by position: information in the middle is used worst [22].
- **Agents game unverified completion.** Models trained in gameable environments generalize from specification gaming to reward-tampering, sometimes rewriting their own reward function zero-shot [5]. A checkbox an agent can tick without external proof will eventually be ticked without the work.

The consequence: a plan for an AI executor is not a memo — it is an executable specification plus a durable state file. Context windows get truncated, compacted, and reset; the plan file is often the only artifact that survives between sessions, agents, and handoffs [7][10].

## Authoring Plans

Seven properties make a plan AI-friendly. Each lists its verdict against the evidence.

### 1. Self-Contained

**Verdict: Supported — expanded.**

**Rule:** Every task must be executable by an agent that has the plan and repository access but zero conversation history. Each task states its objective, its boundaries (what is out of scope, what must not be touched), and its rationale.

**Why:** Underspecification is the single largest measured tax on LLM performance (39% average degradation) [4]. Anthropic's multi-agent engineering team found subagents need an objective, an output format, tool guidance, and clear task boundaries — "without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information" [6]. Cognition's first principle of context engineering: "Share context, and share full agent traces, not just individual messages" [7]. Anthropic's prompting guide reduces this to a golden rule: if a colleague with minimal context would be confused by the instructions, the model will be too [8].

**How:**

- State the goal, the non-goals, and the constraints in the task itself — never by reference to a conversation.
- Include the *why*: models generalize better when given the motivation behind an instruction [8].
- Name what the agent must NOT do; unwritten boundaries do not exist for an agent without history [9][13].
- Self-contained does not mean "everything inlined." Carry lightweight references (paths, IDs, links) and let the executor retrieve content just in time [10] — see Property 5.

### 2. Executable

**Verdict: Supported — expanded.**

**Rule:** Tasks say what to *do*, in imperative voice — and wherever possible include the exact runnable commands (build, test, lint) with flags. A plan that describes what is wrong without saying what to do is a review, not a plan.

**Why:** Spec-driven toolkits treat specifications as executable artifacts that directly generate implementations [11][12]. Analysis of 2,500+ AGENTS.md files found the effective ones put executable commands early, "with flags and options, not just tool names" [13]. CodePlan, which frames repository-level coding as planning, synthesizes a multi-step chain of concrete edits at specific code locations — it got 5/6 repositories through validity checks where non-planning baselines got 0/6 [15]. Explicit plan-then-execute prompting beats unstructured reasoning (Plan-and-Solve [16]); and Anthropic's agent guidance shows error-proofing action formats (e.g., requiring absolute file paths) eliminates whole error classes [17].

**How:**

- One action per step: "Edit `src/auth/login.ts` to…", "Run `pytest tests/auth -v`".
- Include the commands the executor will need, verbatim, with flags [13][14].
- Where a step has no deterministic command, say so and define the expected artifact instead (a file, a diff, a passing check).

### 3. Checkable

**Verdict: Supported — expanded with a hardening clause.**

**Rule:** Every task carries a definition of done that is objectively verifiable — preferably a command whose output proves completion (tests pass, build green, output matches). "Looks done" is not a criterion.

**Why:** Coding agents excel precisely because "code solutions are verifiable through automated tests," and agents must "gain 'ground truth' from the environment at each step" [17]. Without a check the agent can run, the only completion signal is appearance, and the human becomes the verification loop [9]. SWE-bench scores resolutions by repository tests, not by plausibility [2]. Reflexion shows written feedback against real signals lifts agents from 80% to 91% pass@1 on HumanEval [18]. Kiro's spec workflow attaches acceptance criteria to every requirement [19].

**Hardening clause:** Prefer deterministic checks (tests, builds, linters, type checks) over judgment calls; LLM-as-judge verification is scalable but its reliability "requires careful design" [20]. The check must be tamper-resistant: the executing agent must not be able to weaken the test to make it pass — treat verification as immutable for the duration of execution [8], because specification gaming is a measured behavior, not a hypothetical one [5].

### 4. Isolated — with Declared Dependencies

**Verdict: Corrected.** The original claim — "each task can be done independently" — is overstated for code work.

**Why the correction:** Real repository tasks are inter-dependent by nature; CodePlan's evaluation required coordinated edits across 2–97 files [15]. And Cognition's second principle warns that "actions carry implicit decisions, and conflicting decisions carry bad results" — agents working without visibility into each other's work make silently conflicting assumptions [7]. Pure independence is often unachievable; *undeclared* dependence is the actual failure.

**Corrected rule:** Each task must be independently executable and verifiable *given its declared dependencies*. The plan declares the dependency graph: which tasks block which, and which can run in any order. "Each task should be something you can implement and test in isolation" remains the target [11]; where the target is unreachable, sequence the tasks and propagate the shared decision through the plan itself (the earlier task's recorded output), never through assumed context [7].

**How:**

- Keep tasks small and single-purpose [11][21].
- Add an explicit `Depends on:` line per task; group tasks into waves that can run concurrently [19].
- If a discovery mid-execution reveals a hidden dependency, amend the graph (Execution Rule 2).

### 5. Referenced

**Verdict: Supported — expanded.**

**Rule:** Point at concrete artifacts: file paths, requirement IDs, interfaces, commands. Verify every reference resolves before the plan is finalized.

**Why:** References are the mechanism that lets a plan be self-contained *and* short: "just in time" agents keep lightweight identifiers (file paths, stored queries, links) and load content at runtime rather than stuffing the context [10]. Anthropic's multi-agent team has subagents write outputs to the filesystem and pass back references instead of full content, to avoid the "game of telephone" [6]. Claude Code's guidance: the most useful specs "name the files and interfaces involved" [9]. Kiro tasks trace back to specific requirements [17][19].

**How:**

- Reference paths, symbols, and requirement IDs — these are stable. Avoid line numbers; they rot as code changes.
- Verify each referenced file exists during drafting (plan-mode exploration is read-only research before writing [23][25]).
- Pass references between tasks and agents, not copies of content [6].

### 6. Specific — at the Right Altitude

**Verdict: Supported — refined.** Specificity is necessary but has a ceiling.

**Rule:** Be unambiguous about *what* must be true, *why*, and the constraints. Use numbered steps where order matters. But do not over-specify the incidental *how*: brittle step prescriptions break on the first surprise and strip the executor's ability to adapt.

**Why:** Anthropic's context engineering guidance calls this the "right altitude" — neither brittle hardcoded logic nor vague guidance that assumes shared context [10]. GitHub frames coding agents as "literal-minded pair programmers": a vague prompt "forces the model to guess at potentially thousands of unstated requirements" [11]. The AGENTS.md analysis is blunt: "Most agent files fail because they're too vague" [13]. The altitude ceiling is also measured: Anthropic's multi-agent team evaluates end-state outcomes rather than prescribed steps, because agents take different valid paths [6]. And placement matters — put critical constraints at the top (or end) of the plan, never buried mid-document [22].

**How:**

- Concrete test from spec-kit: not "build authentication" but "create a user registration endpoint that validates email format" [11].
- Specify stack, versions, and file locations exactly [13]; leave sequencing of micro-steps to the executor unless order is load-bearing.

### 7. Structured Metadata

**Verdict: Supported — expanded.**

**Rule:** Plans carry frontmatter and predictable sections, and declare the harness format when they target one (spec-kit tasks, Kiro `tasks.md`, plain markdown checklist, etc.).

**Why:** Structured formats are machine-legible contracts: AGENTS.md files use YAML frontmatter plus structured sections [13][14]; OpenCode agents are defined in markdown with YAML frontmatter [23]; Anthropic recommends organizing prompts into distinct, titled sections [10]; Kiro and spec-kit plans follow fixed templates [12][19]. Because plans are living documents (Execution Rule 1), freshness metadata (`status`, `last_updated`) tells the next executor whether the plan still reflects reality — a stale plan is worse than none (see [reference-standards](reference-standards.md)).

**Minimum fields:** `title`, `status`, `last_updated`, `harness` (if any), and per-task checkboxes. See the template below.

## Executing Plans

Five rules govern the agent executing an AI-friendly plan. All five held up against the evidence.

### Rule 1: Update the Plan Incrementally

**Verdict: Supported.**

**Why:** The plan file is the executor's durable memory. Context windows truncate and compact without warning; Anthropic's agents therefore practice structured note-taking — to-do lists and NOTES.md persisted outside the context window and re-read after resets [10] — and their multi-agent lead saves its plan to memory because the conversation *will* be truncated [6]. ReAct formalized the loop: "reasoning traces help the model induce, track, and update action plans as well as handle exceptions" [24]. Reflexion shows written self-feedback stored in an episodic buffer improves subsequent trials [18]. Harnesses encode the same behavior: Kiro updates task status in real time [19]; Cline recommends writing the plan to a markdown file and tracking a todo list during execution [25].

**Mechanics:**

- Update the plan at every state change, not in batches — context can be lost at any point.
- Status vocabulary: `pending` → `in_progress` → `done` | `blocked` | `skipped (reason)`.
- Record scope adjustments and deviations in the plan as they happen, with one-line reasons.

### Rule 2: Surface Blockers Early

**Verdict: Supported.**

**Why:** Anthropic's agent guidance: "Agents can then pause for human feedback at checkpoints or when encountering blockers," with stopping conditions to maintain control [17]. 12-Factor Agents makes human contact a first-class tool call, not an afterthought [21]. OpenCode enforces this mechanically: `ask` permissions gate risky actions, and a step limit forces the agent to summarize its work and remaining tasks [23]. ReAct's exception handling [24] and Anthropic's "ask before hard-to-reverse actions" prompting rule [8] point the same way.

**Mechanics:**

- When blocked, write into the plan: what is blocked, what was tried, and what is needed (decision, access, clarification). Never silently skip.
- Record newly discovered dependencies in the plan's dependency graph immediately (Property 4).
- Escalate before destructive or hard-to-reverse actions, not after [8][23].

### Rule 3: Keep the Checklist Honest

**Verdict: Supported — the most safety-critical rule.**

**Why:** Specification gaming is measured behavior: models that learn to game easy checks generalize to tampering with the reward itself, and even honestly-working models can corrupt the completion signal [5]. Anthropic's counter is ground truth from the environment at every step [17] and evidence over assertion — show the test output, do not claim success [9]. SWE-bench's standard: resolved means the repository's tests pass [2]. AGENTS.md's phrasing: "Fix any test or type errors until the whole suite is green" [14].

**Mechanics:**

- Mark a task done only after running its verification and capturing the result (exit code, output).
- If the check cannot be run, the task is `blocked`, never `done`.
- Never edit a test or check to make it pass; that is tampering, not progress [5][8].
- Where feasible, have a fresh context (subagent or reviewer) compare the diff against the plan [9].

### Rule 4: Preserve Intent Through Deviations

**Verdict: Supported.**

**Why:** Spec-kit's course-correction loop is explicit: update the spec, regenerate the plan, re-execute — with cross-artifact consistency analysis before implementation [11][12]. Cline's guidance: when execution hits unexpected complexity, return to plan mode rather than pushing through [25]. Cognition's second principle explains why silent deviation is fatal: actions carry implicit decisions, so an unrecorded change of approach silently invalidates every downstream task built on the old assumption [7]. Multi-turn research adds that wrong turns compound — agents do not recover on their own [4].

**Mechanics:**

- When a discovery changes the approach: update the plan's description *and* rationale, then re-verify that every remaining task still follows.
- Log the deviation in the plan with its reason — decisions, not just status [7].
- If the deviation invalidates completed work, reopen those tasks rather than leaving a false `done`.

### Rule 5: Pass the Plan Forward

**Verdict: Supported.**

**Why:** Handoff is a designed mechanism, not a courtesy. Anthropic's compaction guidance: a handoff summary must preserve architectural decisions, unresolved bugs, and implementation details; structured notes are re-read after every reset [10]. Their multi-agent system spawns fresh agents with clean contexts and maintains continuity via stored plans and careful handoffs [6]. LangChain's context engineering taxonomy — write, compress, isolate — is the same playbook [26], and Cognition compresses history into "key details, events, and decisions" for exactly this purpose [7]. Harnesses force it: OpenCode's step limit triggers a summary of work and remaining tasks [23]; Cline carries full planning context into execution [19]. Voyager's skill library transferring zero-shot to new worlds shows durable artifacts beat durable contexts [27].

**Mechanics:**

- Handoff state = current checklist + decisions made (with rationale) + open blockers + verification evidence + remaining work.
- Acceptance test: a fresh agent reading *only* the plan can continue without asking a single question.

## Plan Template

**[Copy-Safe]** Minimal skeleton satisfying all seven properties:

```markdown
---
title: <Feature or change name>
status: in_progress          # draft | in_progress | blocked | done | abandoned
last_updated: <YYYY-MM-DD>
harness: <plain | spec-kit | kiro | other>
---

# <Title>

## Goal
<What must be true when this plan is complete, and why.>

## Non-Goals
<What is explicitly out of scope.>

## Context and References
- <file/path/or/doc> — <why it matters>
- Constraints: <versions, conventions, things never to touch>

## Verification
- Full-suite check: `<command with flags>`
- Per-task checks listed on each task.

## Tasks
- [ ] **T1: <imperative action>** — Edit `<path>` to <what>.
  - Depends on: none
  - Verify: `<command>` → <expected result>
- [ ] **T2: <imperative action>** — <what>.
  - Depends on: T1
  - Verify: `<command>` → <expected result>

## Decisions Log
- <YYYY-MM-DD>: <decision> — <reason>

## Blockers
- <none | what is blocked, what was tried, what is needed>

## Handoff Notes
<Current state summary for the next executor. Update before any pause.>
```

## Anti-Patterns

- **Vague tasks** ("improve error handling") — the executor guesses thousands of unstated requirements [11].
- **Buried constraints** mid-document — models use middle-context information worst [22].
- **Checklists without verification commands** — "looks done" becomes the only signal [9].
- **"Independent" tasks with undeclared shared state** — conflicting implicit decisions [7].
- **Write-once plans** — never updated, so the next executor inherits fiction [10].
- **Marking done from memory** — specification gaming is measured behavior [5].
- **Editing the test to pass** — reward tampering [5][8].
- **Drip-feeding the plan across chat turns** — underspecification compounds [4].
- **Over-prescribed micro-steps** — brittle at first surprise; specify outcomes, not every step [6][10].

## Quality Checklist

**Authoring:**

- [ ] Every task is understandable with zero conversation history (goal, boundaries, why)
- [ ] Every task has at least one concrete action and, where possible, a runnable command
- [ ] Every task has an objective definition of done, executable by the agent
- [ ] Verification is tamper-resistant (executor cannot weaken the check)
- [ ] Dependencies between tasks are declared explicitly; independent tasks marked as parallelizable
- [ ] Every referenced file/ID/command was verified to resolve at draft time
- [ ] Critical constraints appear at the top of the plan
- [ ] Frontmatter includes status, last_updated, and harness (if any)

**Executing:**

- [ ] Plan updated at every state change, not in batches
- [ ] Every blocker recorded in the plan with what was tried and what is needed
- [ ] Every `done` has captured verification output; nothing marked done from memory
- [ ] No test or check weakened during execution
- [ ] Deviations logged with reasons; remaining tasks re-verified after each deviation
- [ ] Handoff notes current; a fresh agent could continue from the plan alone

## Related Documents

- [AI-Friendly Plan Authoring and Execution — Evidence](ai-friendly-planning-evidence.md) — claim-by-claim verification of the seven properties and five rules, contradictory evidence, and full citations.
- [Reference File Standards](reference-standards.md) — the conventions this document follows; its freshness and structure rules are the basis for Property 7.
- [Best Practices for AGENTS.md Files](../agents/agents-best-practices.md) — the standing-instructions complement to per-task plans.
- [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md) — externalized memory and file-based state passing patterns that underpin Execution Rules 1 and 5.
- [OpenCode Best Practices Guide](opencode-best-practices.md) — harness-level configuration for plan/build separation.

## References

1. Valmeekam et al., "PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change," NeurIPS 2023 D&B. https://arxiv.org/abs/2206.10498
2. Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?," ICLR 2024. https://arxiv.org/abs/2310.06770
3. Xu et al., "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks," 2024. https://arxiv.org/abs/2412.14161
4. Laban et al., "LLMs Get Lost In Multi-Turn Conversation," 2025. https://arxiv.org/abs/2505.06120
5. Denison et al., "Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models," 2024. https://arxiv.org/abs/2406.10162
6. Anthropic, "How we built our multi-agent research system," Jun 2025. https://www.anthropic.com/engineering/built-multi-agent-research-system
7. Yan, Cognition, "Don't Build Multi-Agents," Jun 2025. https://cognition.ai/blog/dont-build-multi-agents
8. Anthropic Docs, "Prompting best practices" (Be clear and direct). https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct
9. Anthropic, "Claude Code best practices." https://www.anthropic.com/engineering/claude-code-best-practices
10. Anthropic, "Effective context engineering for AI agents," Sep 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
11. Delimarsky, GitHub Blog, "Spec-driven development with AI: Get started with a new open source toolkit," Sep 2025. https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
12. GitHub, "Spec Kit" repository. https://github.com/github/spec-kit
13. Nigh, GitHub Blog, "How to write a great agents.md: Lessons from over 2,500 repositories," Nov 2025. https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
14. AGENTS.md project. https://agents.md/
15. Bairi et al., "CodePlan: Repository-level Coding using LLMs and Planning," 2023. https://arxiv.org/abs/2309.12499
16. Wang et al., "Plan-and-Solve Prompting," ACL 2023. https://arxiv.org/abs/2305.04091
17. Anthropic, "Building effective agents," Dec 2024. https://www.anthropic.com/engineering/building-effective-agents
18. Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning," NeurIPS 2023. https://arxiv.org/abs/2303.11366
19. Kiro (AWS), "Specs" documentation. https://kiro.dev/docs/specs/
20. Gu et al., "A Survey on LLM-as-a-Judge," 2024. https://arxiv.org/abs/2411.15594
21. Horthy, HumanLayer, "12-Factor Agents." https://github.com/humanlayer/12-factor-agents
22. Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," TACL 2024. https://arxiv.org/abs/2307.03172
23. OpenCode, "Agents" documentation. https://opencode.ai/docs/agents/
24. Yao et al., "ReAct: Synergizing Reasoning and Acting in Language Models," ICLR 2023. https://arxiv.org/abs/2210.03629
25. Cline, "Plan & Act Mode" documentation. https://docs.cline.bot/core-workflows/plan-and-act.md
26. LangChain, "Context Engineering for Agents," Jul 2025. https://blog.langchain.com/context-engineering-for-agents/
27. Wang et al., "Voyager: An Open-Ended Embodied Agent with Large Language Models," TMLR 2024. https://arxiv.org/abs/2305.16291

---

*Last verified: 2026-08-03 — update this date when content is reviewed or changed.*
