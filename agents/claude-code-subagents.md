---
title: Claude Code Subagents
description: Overview of Claude Code subagent system — built-in agents, quickstart, usage patterns, workflows, and forking.
status: active
tags: [claude-code, subagents, agents, workflows]
last_verified: 2026-08-13
layer: warm
applies_to: Claude Code
---

# Claude Code Subagents

> Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

[Documentation index](https://code.claude.com/docs/llms.txt) — Fetch the complete Claude Code documentation index.

## Overview

Subagents are specialized AI assistants that handle specific types of tasks. Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary. Define a custom subagent when you keep spawning the same kind of worker with the same instructions.

Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results. To see the context savings in practice, the [context window visualization](https://code.claude.com/en/context-window) walks through a session where a subagent handles research in its own separate window.

> **Note:** Subagents work within a single session. To run many independent sessions in parallel and monitor them from one place, see [background agents](https://code.claude.com/en/agent-view). For sessions that communicate with each other, see [agent teams](https://code.claude.com/en/agent-teams).

Subagents help you:

* **Preserve context** by keeping exploration and implementation out of your main conversation
* **Enforce constraints** by limiting which tools a subagent can use
* **Reuse configurations** across projects with user-level subagents
* **Specialize behavior** with focused system prompts for specific domains
* **Control costs** by routing tasks to faster, cheaper models like Haiku

Claude uses each subagent's description to decide when to delegate tasks. When you create a subagent, write a clear description so Claude knows when to use it.

Claude Code includes several built-in subagents such as Explore, Plan, and general-purpose. You can also create custom subagents to handle specific tasks.

## Built-in subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation's permissions with additional tool restrictions.

Explore and Plan skip your CLAUDE.md files and the parent session's git status to keep research fast and inexpensive. Every other built-in and [custom subagent](claude-code-subagents-configure.md) loads both. For the full breakdown of what reaches a subagent, see [what loads at startup](#what-loads-at-startup).


#### Explore
    A fast, read-only agent optimized for searching and analyzing codebases.

    * **Model**: inherits from the main conversation, capped at Opus on the Claude API, so Explore never runs on a more expensive model than the one you already chose for the session
    * **Tools**: read-only tools; Write and Edit are denied
    * **Purpose**: file discovery, code search, codebase exploration

    As of v2.1.198, Explore inherits the main conversation's model instead of always running on Haiku. On the Claude API, the inherited model is capped at Opus: a main conversation on a higher tier runs Explore on Opus, and a main conversation on Sonnet or Haiku runs Explore on that same model. On any other provider, such as [Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS](https://code.claude.com/en/third-party-integrations), Explore inherits the main conversation's model directly.

    A [user or project subagent](claude-code-subagents-configure.md#choose-the-subagent-scope) named `Explore` overrides the built-in and keeps its own `model` field, so define one with `model: haiku` to keep exploration on a lower-cost model.

    Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context.

    When invoking Explore, Claude specifies a thoroughness level: **quick** for targeted lookups, **medium** for balanced exploration, or **very thorough** for comprehensive analysis.


#### Plan
    A research agent used during [plan mode](https://code.claude.com/en/permission-modes#analyze-before-you-edit-with-plan-mode) to gather context before presenting a plan.

    * **Model**: inherits from the main conversation
    * **Tools**: read-only tools; Write and Edit are denied
    * **Purpose**: codebase research for planning

    When you're in plan mode and Claude needs to understand your codebase, it delegates research to the Plan subagent so that exploration output stays in a separate context window while the main conversation remains read-only.


#### General-purpose
    A capable agent for complex, multi-step tasks that require both exploration and action.

    * **Model**: inherits from the main conversation
    * **Tools**: all tools
    * **Purpose**: complex research, multi-step operations, code modifications

    Claude delegates to general-purpose when the task requires both exploration and modification, complex reasoning to interpret results, or multiple dependent steps.


#### Other
    Claude Code includes additional helper agents for specific tasks. These are typically invoked automatically, so you don't need to use them directly.

    | Agent             | Model  | When Claude uses it                                      |
    | :---------------- | :----- | :------------------------------------------------------- |
    | statusline-setup  | Sonnet | When you run `/statusline` to configure your status line |
    | claude-code-guide | Haiku  | When you ask questions about Claude Code features        |



Built-in subagents are registered by default in interactive sessions. To restrict them:

* To block a specific built-in type, add it to `permissions.deny` as shown in [Disable specific subagents](claude-code-subagents-configure.md#disable-specific-subagents).
* To prevent Claude from delegating to any subagent, deny the `Agent` tool itself with [`permissions.deny`](https://code.claude.com/en/permissions#tool-specific-permission-rules).
* To remove only the built-in `Explore` and `Plan` subagents, set [`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`](https://code.claude.com/en/env-vars). Claude reads and explores files directly instead of delegating to them. Requires Claude Code v2.1.198 or later.
* In [non-interactive mode](https://code.claude.com/en/headless) and the [Agent SDK](https://code.claude.com/en/agent-sdk/overview), set [`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`](https://code.claude.com/en/env-vars) to remove all built-in types and supply only your own.

Beyond these built-in subagents, you can create your own with custom prompts, tool restrictions, permission modes, hooks, and skills. The following sections show how to get started and customize subagents.

## Quickstart: create your first subagent

Subagents are Markdown files with YAML frontmatter. To create one, ask Claude to write it for you, or [write the file yourself](claude-code-subagents-configure.md#write-subagent-files).

As of v2.1.198, the `/agents` command no longer opens the interactive creation wizard; running it prints a reminder to ask Claude or edit `.claude/agents/` directly. Subagent files, frontmatter fields, and the `.claude/agents/` and `~/.claude/agents/` locations are unchanged; only the terminal wizard is removed.

This walkthrough creates a user-level subagent that reviews code and suggests improvements.


**Ask Claude to create the subagent**
    In Claude Code, describe the subagent you want and where to save it:

    ```text
    Create a personal code-improver subagent in ~/.claude/agents/ that scans
    files and suggests improvements for readability, performance, and best
    practices. It should explain each issue, show the current code, and
    provide an improved version. Make it read-only and have it use Sonnet.
    ```

    Claude writes the file with a `name`, a `description`, a `tools` list, a `model`, and a system prompt.


**Review the file**
    Open `~/.claude/agents/code-improver.md` and confirm the frontmatter matches what you asked for. The result looks like this:

    ```markdown
    ---
    name: code-improver
    description: Scans files and suggests improvements for readability, performance, and best practices. Use after writing or modifying code.
    tools: Read, Grep, Glob
    model: sonnet
    ---

    You are a code improvement specialist. For each issue you find, explain
    the problem, show the current code, and provide an improved version.
    ```

    Because the file lives in `~/.claude/agents/`, the subagent is available in every project on your machine. To scope it to one project instead, move it to that project's `.claude/agents/` directory. [Choose the subagent scope](claude-code-subagents-configure.md#choose-the-subagent-scope) compares the two.


**Try it out**
    Ask Claude to delegate to the new subagent:

    ```text
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delegates to your new subagent, which scans the codebase and returns improvement suggestions.

    If Claude can't find the new subagent, restart Claude Code and try again. This happens only when `~/.claude/agents/` didn't exist before the session started, because a running session doesn't detect a newly created `agents` directory.



You now have a subagent you can use in any project on your machine to analyze codebases and suggest improvements.

You can also write subagent files by hand, define them via CLI flags, or distribute them through plugins. The following sections cover all configuration options.

> **Note:** On Claude Code v2.1.197 and earlier, `/agents` opens an interactive wizard with a **Running** tab that lists live subagents and a **Library** tab for creating, editing, and deleting them.

## Configure subagents

See [Claude Code Subagent Configuration](claude-code-subagents-configure.md) for the complete configuration reference — scope, file format, frontmatter fields, models, capabilities, permissions, and hooks.

## Work with subagents

### Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like "use proactively" in your subagent's description field.

### Invoke subagents explicitly

When automatic delegation isn't enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

* **Natural language**: name the subagent in your prompt; Claude decides whether to delegate
* **@-mention**: guarantees the subagent runs for one task
* **Session-wide**: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

For natural language, there's no special syntax. Name the subagent and Claude typically delegates:

```text
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention the subagent.** Type `@` and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:

```text
@"code-reviewer (agent)" look at the auth changes
```

Your full message still goes to Claude, which writes the subagent's task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives.

Subagents provided by an enabled [plugin](https://code.claude.com/en/plugins) appear in the typeahead under their scoped name, such as `my-plugin:code-reviewer` or `my-plugin:review:security` when the plugin [organizes agents into subfolders](claude-code-subagents-configure.md#choose-the-subagent-scope). Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name.

You can also type the mention manually without using the picker: `@agent-<name>` for local subagents, or `@agent-` followed by the scoped name for plugin subagents, for example `@agent-my-plugin:code-reviewer`.

**Run the whole session as a subagent.** Pass [`--agent <name>`](https://code.claude.com/en/cli-reference) to start a session where the main thread itself takes on that subagent's system prompt, tool restrictions, and model:

```bash
claude --agent code-reviewer
```

The subagent's system prompt replaces the default Claude Code system prompt entirely, the same way [`--system-prompt`](https://code.claude.com/en/cli-reference) does. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header so you can confirm it's active.

This works with built-in and custom subagents, and the choice persists when you resume the session.

For a plugin-provided subagent, you can pass only the agent name and Claude Code finds it:

```bash
claude --agent security-reviewer
```

If multiple plugins provide agents with the same name, pass the scoped name to disambiguate:

```bash
claude --agent my-plugin:security-reviewer
```

If the plugin places the agent in a subfolder of its `agents/` directory, include the subfolder in the scoped name, for example `claude --agent my-plugin:review:security`.

To make it the default for every session in a project, set `agent` in `.claude/settings.json`:

```json
{
  "agent": "code-reviewer"
}
```

The CLI flag overrides the setting if both are present.

### Run subagents in foreground or background

Subagents can run in the foreground or the background:

* **Foreground subagents** block the main conversation until complete. Permission prompts are passed through to you as they come up.
* **Background subagents** run concurrently while you continue working. As of v2.1.186, when a background subagent reaches a tool call that needs permission, the prompt surfaces in your main session and names the subagent that is asking. Approve to let the subagent continue, or press Esc to deny that one tool call without stopping the subagent. Before v2.1.186, background subagents auto-denied any tool call that would have prompted.

As of v2.1.198, subagents run in the background by default. Claude runs a subagent in the foreground when it needs the result before continuing. The default changes where a subagent runs, not what it's allowed to do: background subagents still surface every permission prompt in your main session. Before v2.1.198, Claude chose between foreground and background based on the task.

You can also steer this yourself:

* Ask Claude to run a task in the background or in the foreground
* Press **Ctrl+B** to background a running task

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](https://code.claude.com/en/env-vars).

When [`CLAUDE_CODE_FORK_SUBAGENT`](#fork-the-current-conversation) is set to `1`, every subagent spawn runs in the background and the frontmatter `background` field has no effect, because fork mode removes the `run_in_background` parameter from the `Agent` tool. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` takes precedence over fork mode and keeps subagent spawns in the foreground.

### API errors in subagents

As of v2.1.199, a subagent whose run ends on an API error, such as a usage limit or a repeated server error, reports that failure back to Claude instead of returning the error text as if it were the subagent's findings. What Claude receives depends on where the subagent ran:

* **Foreground**: if a rate limit, overload, or server error cuts off a subagent that already produced text output, the Agent tool returns that partial output with a note that the subagent was cut off and didn't finish its task. A subagent that produced nothing, or whose only output was tool calls, fails with [`Agent terminated early due to an API error`](https://code.claude.com/en/errors#agent-terminated-early-due-to-an-api-error), followed by the error detail. In v2.1.199, a rate limit, overload, or server error that cut off the tool-calls-only shape returned an empty partial result containing only the cut-off note instead.
* **Background**: the subagent is marked failed, and the message Claude receives when it ends names the API error and includes the subagent's last output, so partial work isn't lost.

Once the underlying API error clears, ask Claude to retry the task or [resume the subagent](#resume-subagents).

### Common patterns

#### Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent's context while only the relevant summary returns to your main conversation.

```text
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:

```text
Research the authentication, database, and API modules in parallel using separate subagents
```

Each subagent explores its area independently, then Claude synthesizes the findings. This works best when the research paths don't depend on each other.

> **Warning:** When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context.

For tasks that need sustained parallelism or exceed your context window, [agent teams](https://code.claude.com/en/agent-teams) give each worker its own independent context.

#### Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.

```text
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Choose between subagents and main conversation

Use the **main conversation** when:

* The task needs frequent back-and-forth or iterative refinement
* Multiple phases share significant context, such as planning, implementation, and testing
* You're making a quick, targeted change
* Latency matters. Subagents start fresh and may need time to gather context

Use **subagents** when:

* The task produces verbose output you don't need in your main context
* You want to enforce specific tool restrictions or permissions
* The work is self-contained and can return a summary

Consider [Skills](https://code.claude.com/en/skills) instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context.

For a quick question about something already in your conversation, use [`/btw`](https://code.claude.com/en/interactive-mode#side-questions-with-%2Fbtw) instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.

### Spawn nested subagents

As of Claude Code v2.1.172, a subagent can spawn its own subagents. Use this when a delegated task itself splits into parallel subtasks, such as a reviewer subagent that dispatches a verifier per finding, so the intermediate output never reaches your main conversation. Only the top-level subagent's summary returns to you.

A nested subagent is configured the same way as a top-level one and resolves from the same [scopes](claude-code-subagents-configure.md#choose-the-subagent-scope).

The subagent panel below the prompt input shows the full tree: each row displays a `(+N)` count of descendants, and as of v2.1.193, opening a row shows that subagent's siblings and direct children with a path back to `main`.

Depth is counted as the number of subagent levels below the main conversation, regardless of whether each level runs in the [foreground or background](#run-subagents-in-foreground-or-background). A subagent at depth three (Claude Code v2.1.219+) doesn't receive the Agent tool and can't spawn further. Prior to v2.1.217 the default depth limit was five; as of v2.1.217 the limit can be configured via `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`.

As of Claude Code v2.1.187, a background subagent's depth is fixed when it is first spawned, and [resuming](#resume-subagents) it later doesn't change that depth. For example, if your main conversation spawns subagent A, and A spawns a background subagent B at depth two, B is still at depth two when you resume it directly from the main conversation. Resuming a subagent from a shallower context doesn't let it spawn additional levels that the depth limit already prevented.

To prevent a specific subagent from spawning others, omit `Agent` from its [`tools`](claude-code-subagents-configure.md#available-tools) list or add it to `disallowedTools`.

A [fork](#fork-the-current-conversation) still can't spawn another fork. It can spawn other subagent types, and those count toward the depth limit.

### Manage subagent context

#### What loads at startup

Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read. Claude composes a delegation message that summarizes the task, and the subagent works from there. The exception is a [fork](#fork-the-current-conversation), which inherits the parent conversation instead of starting fresh.

A non-fork subagent's initial context contains:

* **System prompt**: the agent's own prompt plus environment details that Claude Code appends, not the full Claude Code system prompt. Custom subagents define theirs in the [markdown body](claude-code-subagents-configure.md#write-subagent-files) or `prompt` field. Built-in agents have predefined prompts.
* **Task message**: the delegation prompt Claude writes when it hands off the work.
* **CLAUDE.md and memory**: every level of the [memory hierarchy](https://code.claude.com/en/memory#how-claude-md-files-load) the main conversation loads, including `~/.claude/CLAUDE.md`, project rules, `CLAUDE.local.md`, and managed policy files. The built-in Explore and Plan agents skip this.
* **Git status**: a snapshot taken at the start of the parent session. Absent when the working directory isn't a Git repository or when [`includeGitInstructions`](https://code.claude.com/en/settings#available-settings) is `false`. Explore and Plan skip it regardless.
* **Preloaded skills**: full content of any skill named in the agent's [`skills` field](claude-code-subagents-configure.md#preload-skills-into-subagents). Built-in agents don't preload skills.

Explore and Plan are the only subagents that omit CLAUDE.md and git status. There is no frontmatter field or per-agent setting to change which agents skip them.

The main conversation reads Explore and Plan results with full CLAUDE.md context, so most rules don't need to reach the subagent itself. If a rule must, such as "ignore the `vendor/` directory," restate it in the prompt you give Claude when delegating.

#### Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent's work instead of starting over, ask Claude to resume it.

Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.

When a subagent completes, Claude receives its agent ID. The built-in Explore and Plan agents are one-shot and return no agent ID, so they can't be resumed; use `general-purpose` or a custom subagent when you need to continue the work.

Claude uses the `SendMessage` tool with the agent's ID or name as the `to` field to resume it. `SendMessage` doesn't require [agent teams](https://code.claude.com/en/agent-teams) to be enabled; only structured team-protocol messages such as `shutdown_request` and `plan_approval_response` do.

To resume a subagent, ask Claude to continue the previous work:

```text
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

If a stopped subagent receives a `SendMessage`, it auto-resumes in the background without requiring a new `Agent` invocation.

As of v2.1.199, `SendMessage` checks that a name still refers to the same agent it reached earlier in the conversation. If a newer agent has taken the name, such as a re-spawned background agent that reused it, Claude Code refuses the send rather than delivering it to the wrong agent, and the error reports which agent the name now reaches so Claude can retarget. To reach the earlier agent while it's still running, Claude addresses it by the agent ID from its spawn result. The check is scoped to the current conversation and resets on `/clear`.

As of v2.1.198, a subagent treats messages from the agent that launched it as normal task direction, including mid-task course corrections, and acts on them within its own permission settings. Two limits still hold regardless of who sent the message: no message from any agent counts as your approval for a pending permission prompt, and no agent message can change a subagent's permission settings, `CLAUDE.md`, or configuration. Only the permission system or your own messages can grant approval.

You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at `~/.claude/projects/{project}/{sessionId}/subagents/`. Each transcript is stored as `agent-{agentId}.jsonl`.

Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: when the main conversation compacts, subagent transcripts are unaffected. They're stored in separate files.
* **Session persistence**: subagent transcripts persist within their session. You can [resume a subagent](#resume-subagents) after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: transcripts are cleaned up based on the `cleanupPeriodDays` setting, which defaults to 30 days.

#### Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. Compaction triggers under the same conditions, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` applies to subagents as well. See [environment variables](https://code.claude.com/en/env-vars) for when the override takes effect.

Compaction events are logged in subagent transcript files:

```json
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

The `preTokens` value shows how many tokens were used before compaction occurred.

## Fork the current conversation

> **Note:** Forked subagents require Claude Code v2.1.117 or later. From v2.1.161 the `/fork` command is enabled by default; on earlier versions it requires setting the [`CLAUDE_CODE_FORK_SUBAGENT`](https://code.claude.com/en/env-vars) environment variable to `1`. Letting Claude itself spawn forks is experimental and may change in future releases. This capability may also be enabled in interactive sessions as part of a staged rollout.

A fork is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation. The fork's own tool calls still stay out of your conversation and only its final result comes back, so your main context window stays clean. Use a fork when a named subagent would need too much background to be useful, or when you want to try several approaches in parallel from the same starting point.

To control fork mode regardless of the staged rollout, set [`CLAUDE_CODE_FORK_SUBAGENT`](https://code.claude.com/en/env-vars) to `1` to enable it explicitly or to `0` to disable it. The variable is honored in interactive mode and via the SDK or `claude -p`.

Enabling fork mode changes Claude Code in two ways:

* Claude can spawn a fork by requesting the `fork` subagent type explicitly. Spawns without a subagent type still use the [general-purpose](#built-in-subagents) subagent, and named subagents such as Explore still spawn as before.
* Every subagent spawn runs in the [background](#run-subagents-in-foreground-or-background), whether it is a fork or a named subagent. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to `1` to keep spawns synchronous.

You can start a fork yourself with `/fork` followed by a directive, with or without the variable set. Claude Code names the fork from the first words of the directive. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

```text
/fork draft unit tests for the parser changes so far
```

The fork appears in a panel below your prompt and runs in the background while you keep working. When it finishes, its result arrives as a message in your main conversation. The next section covers the panel controls for watching and steering forks while they run.

### Observe and steer running forks

Running forks appear in a panel below the prompt input, with one row for the main session and one for each fork. Use these keys to interact with the panel:

| Key       | Action                                                             |
| :-------- | :----------------------------------------------------------------- |
| `?` / `?` | Move between rows                                                  |
| `Enter`   | Open the selected fork's transcript and send it follow-up messages |
| `x`       | Dismiss a finished fork or stop a running one                      |
| `Esc`     | Return focus to the prompt input                                   |

With a fork's or subagent's transcript open, follow-up messages and [skills](https://code.claude.com/en/skills) go to that agent, but built-in commands still run in your main conversation. As of v2.1.199, typing `/model` or `/fast` in that view shows a notice that it changes the main conversation's model or fast mode, not the viewed agent's, instead of running it silently.

### How forks differ from named subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

|                         | Fork                             | Named subagent                                                                                                    |
| :---------------------- | :------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| Context                 | Full conversation history        | Fresh context with the prompt you pass                                                                            |
| System prompt and tools | Same as main session             | From the subagent's [definition file](claude-code-subagents-configure.md#write-subagent-files)                                                      |
| Model                   | Same as main session             | From the subagent's `model` field                                                                                 |
| Permissions             | Prompts surface in your terminal | [Prompts surface in your main session](#run-subagents-in-foreground-or-background) when running in the background |
| Prompt cache            | Shared with main session         | Separate cache                                                                                                    |

Because a fork's system prompt and tool definitions are identical to the parent, its first request reuses the parent's [prompt cache](https://code.claude.com/en/prompt-caching#subagents-and-the-cache). This makes forking cheaper than spawning a fresh subagent for tasks that need the same context.

When Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` so the fork's file edits are written to a separate git worktree instead of your checkout.

### Limitations

Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, [non-interactive mode](https://code.claude.com/en/headless), and the Agent SDK; setting it to `0` disables fork mode everywhere, including any server-side rollout. A fork can't spawn further forks.

## Example subagents

See [Claude Code Subagent Examples](claude-code-subagents-examples.md) for complete, copy-safe subagent configurations — code reviewer, debugger, data scientist, and database query validator with hooks.

## Next steps

Now that you understand subagents, explore these related features:

* [Distribute subagents with plugins](https://code.claude.com/en/plugins) to share subagents across teams or projects
* [Run Claude Code programmatically](https://code.claude.com/en/headless) with the Agent SDK for CI/CD and automation
* [Use MCP servers](https://code.claude.com/en/mcp) to give subagents access to external tools and data

## Related Documents

- [Claude Code Subagent Configuration](claude-code-subagents-configure.md) — complete configuration reference (scope, frontmatter, models, permissions, hooks)
