---
title: Harness Toolset Best Practices
description: How to design, implement, and evaluate an agent harness's internal toolset so both frontier and smaller local tool-calling models select, parameterize, and recover from tools efficiently.
status: active
tags: [tools, function-calling, harness, tool-design, local-models, evaluation, context]
last_verified: 2026-10-07
layer: warm
applies_to: agent harnesses, internal toolsets, function/tool calling, frontier and local models
---

# Harness Toolset Best Practices

> Design the tool surface for your weakest supported model, then verify it does not cap your strongest one.

## Overview

This guide covers the tool layer of an AI harness: the catalog of callable tools (names, descriptions, JSON schemas, result shapes) that an agent runtime exposes to its model, plus the loop that executes them. It is written for engineers building agent harnesses, internal toolsets, and coding-assistant runtimes.

The problem is one toolset serving a capability spectrum. Frontier models have native tool calling, large context, and strong selection reasoning. Smaller local models (1B–8B class, often served through Ollama, llama.cpp, or vLLM) also expose an OpenAI-style tools API, but they select worse, parameterize worse, degrade faster as the catalog grows, and have far less context. The goal is a single contract that both tiers can call correctly and cheaply.

This document assumes both tiers **support tool calling natively**. It does not cover grammar hacks or text-parsing scaffolding for models with no tool-calling support.

## Background

### The tool-calling loop

Tool calling is a multi-step conversation: send tools and a prompt; receive zero or more tool calls; execute them in application code; return results; receive the final answer. Build the loop to expect several calls, not exactly one ([OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)).

### The two failure modes

Almost all tool-use failures reduce to two categories. Anthropic states the failure directly: "The most common failures are wrong tool selection and incorrect parameters, especially when tools have similar names" ([Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)). Everything below targets one of these.

### The capability spectrum

Small models are not just slower; they fail differently. Measured differences:

- Frontier and open-weight models both over-call tools, but smaller models do so more: "top-tier models achieve only 80.2% [tool-selection precision]; open-source models get just 62.5%," with open-source error rates "rising to 37.5%" ([The Tool-Overuse Illusion](https://arxiv.org/abs/2604.19749)).
- Selection accuracy collapses as the catalog grows, far worse for open weights: catalog growth caused "a degradation of 7% for GPT-4o and a range of 91% (Mistral-large) to 30.5% (Granite-3.1-8b-instruct)" ([LongFuncEval](https://arxiv.org/abs/2505.10570)).
- The readout, not the harness, is the bottleneck: on BFCL failures "the model attends most to the correct tool 80% of the time (vs. 21% chance), and the gold is the under-attended segment on only 10%: it looks at the right tool and still picks wrong" ([Looking Is Not Picking](https://arxiv.org/abs/2606.16364)). A training-free selector added "+11.9 pts pooled function-name selection" across 3–32B models, so the same fix helps both tiers.

The practical consequence: shrinking and sharpening the catalog helps every tier, and helps weak models most.

## Core Principles

1. **Design from workflows, not endpoints.** Implement the few tools that complete real jobs, not one tool per API route ([Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents)).
2. **Keep the active catalog small.** OpenAI recommends "fewer than 20 functions available at the start of a turn"; Together calls `<20` a soft target; Copilot avoids tool search only "below roughly 30 tools."
3. **Treat metadata as prompt.** The description is the model's only instructions for when and how to call. Together: "The function description is the single biggest factor in tool-calling accuracy."
4. **Give every tool a distinct, namespaced name.** Avoid near-duplicates like `notification-send-user` vs `notification-send-channel`.
5. **Make invalid states unrepresentable.** Use enums, closed schemas, and one parameter per decision instead of contradictory booleans.
6. **Offload work to code.** Remove arguments the application already knows and merge always-sequential calls.
7. **Return high-signal, bounded results.** Paginate, filter, and truncate; return semantic identifiers, not UUIDs and MIME types.
8. **Make failures instructable.** Return the failing field, the constraint, and the next safe action.
9. **Disclose progressively when large.** Use tool search or retrieval instead of loading everything up front.
10. **Constrain with strict schemas where the runtime supports it.**
11. **Separate read, preview, and mutate; require approval for consequential writes.**
12. **Evaluate every supported model tier on held-out tasks.**

## Tool Design

### The contract

Every tool must answer five questions unambiguously:

- When to use it, and when **not** to.
- What each parameter means, its type, and its units.
- What side effects, permissions, and approvals apply.
- What the result represents.
- What to do when it fails.

Together's rubric is the clearest formulation: "Aim for three to four sentences per tool, more for complex tools. Apply the intern test: if a new engineer could correctly call the function given only the schema, the model can too." The same test appears in OpenAI's guide and Anthropic's "describe the tool to a new hire" advice.

### Descriptions

A strong description states what the tool does, what it returns, when to reach for it, and what it explicitly does not cover. **[Conceptual]** Good versus weak:

```json
{
  "name": "search_orders",
  "description": "Search a customer's orders by date range, status, or total. Returns matching orders with id, status, total, and currency. Use for questions about a specific customer's purchases. Does not return catalog items, refunds, or shipping tracking.",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": { "type": "string", "description": "Customer ID, e.g. CUS-9182" },
      "status": { "type": "string", "enum": ["pending", "shipped", "delivered", "cancelled"] },
      "since": { "type": "string", "description": "ISO 8601 date, e.g. 2026-01-01" }
    },
    "required": ["customer_id"],
    "additionalProperties": false
  }
}
```

Prefer `customer_id` over `customer`; make implicit conventions (date formats, ID schemes) explicit. Anthropic notes that "merely resolving arbitrary alphanumeric UUIDs to more semantically meaningful and interpretable language... significantly improves Claude's precision in retrieval tasks."

### Namespacing and granularity

Group by service and resource: `github_list_prs`, `github_create_pr`, `slack_send_message`. Both Anthropic and OpenAI ship explicit namespace support, and Together recommends service prefixes as the catalog grows. Namespacing "reduces the number of tools... and offloads agentic computation from the agent's context back into the tool calls."

Consolidate operations that share intent, authorization, and output shape. Implement `schedule_event` instead of `list_users`, `list_events`, and `create_event`. Merge calls that are always sequential: "if you always call `mark_location()` after `query_location()`, just move the marking logic into the query function call."

### Schemas

Constrain as much as possible at the schema layer:

- Give every parameter a type and an enum when values are fixed.
- Mark exactly the fields that must be supplied as `required`.
- Set `additionalProperties: false`.
- Avoid representable contradictions such as `toggle_light(on: bool, off: bool)`; use `state: ["on", "off"]`.
- Keep nesting shallow. Deeply nested objects are a top source of malformed arguments for small models.

OpenAI strict mode requires `additionalProperties: false` on every object and every property listed in `required`; optional fields are expressed with a `null` type union.

### Examples on the tool

JSON Schema defines validity, not usage. Anthropic's **Tool Use Examples** (`input_examples`) teach formats, nested structures, and optional-parameter correlations; internal testing "improved accuracy from 72% to 90% on complex parameter handling." This matters more for weaker models, which rely on pattern-matching over inference. Keep it to 1–5 examples, use realistic values, and only where the schema leaves ambiguity.

### Results

Return only what informs the next action. Prioritize `name`, `status`, `total`, `id`; drop `uuid`, `256px_image_url`, and `mime_type`. Offer a `response_format` enum (`concise` / `detailed`) when downstream calls need raw identifiers but reasoning needs brevity; Anthropic measured roughly a third of the tokens in concise mode.

Bound every variable-size result with pagination, filtering, and truncation. Claude Code "restrict[s] tool responses to 25,000 tokens by default," and other harnesses impose their own caps. Truncation must come with steering text telling the model how to narrow the next request.

## Making One Toolset Work Across the Capability Spectrum

The contract stays constant; the *delivery* is tuned per tier.

### The dominant lever: active catalog size

Selection accuracy is a function of how many tools are in view, and weak models have the lower ceiling:

- Anthropic: "Claude's ability to pick the right tool degrades once you exceed 30–50 available tools."
- Retrieval filtering more than tripled accuracy (43.13% vs 13.62%) while cutting prompt tokens by over half ([RAG-MCP](https://arxiv.org/abs/2505.03275)).
- Adaptive shortlists nearly match showing 50 tools "while presenting only 7 on average," at "roughly 200 tokens per tool description" ([How Many Tools Should an LLM Agent See?](https://arxiv.org/abs/2605.24660)).

Design rule: **pick the weakest tier you must support and size the always-loaded catalog for it.** If that catalog exceeds ~20 tools, add retrieval or tool search rather than trusting the model to filter distractors.

### Techniques, ordered by leverage

1. **Retrieval / tool search.** Defer everything but the 3–5 most-used tools. Anthropic reports an ~85% reduction in tool-definition tokens and selection accuracy on MCP evals rising "from 79.5% to 88.1%." OpenAI (`tool_search`), Copilot CLI, and the Claude Agent SDK all enable this automatically past a threshold.
2. **Descriptions and negative guidance.** State when *not* to use a tool, and forbid guessing: "Do not guess values. If a required detail is missing, ask the user." Negative guidance compensates for weak internal reasoning.
3. **Strict, flat schemas plus constrained decoding.** vLLM and Together support `strict: true`; vLLM applies structural-tag constraints for named/required calls, and without strict, "vLLM extracts tool calls from raw text, so arguments may occasionally be malformed or violate the function's parameter schema." Weak models benefit most from making invalid output impossible.
4. **`tool_choice` control.** If a small model under-calls, use `required` or a named tool; if it over-calls, use `none` or tighten the prompt. Over-calling is measurable and costly.
5. **Examples.** `input_examples` or one-shot examples in the system prompt raise weak-model accuracy the most.
6. **Fewer, flatter parameters.** Enums over free strings; avoid deep nesting; remove arguments the app can supply.
7. **Aggressive output bounding.** Small models have small context; truncate early and often.
8. **Native tool-call format and the right parser.** Use the model's trained format, not a text workaround.

### Runtime-specific notes

- **Qwen:** use Hermes-style tool calling. Qwen warns that "for reasoning models like Qwen3, it is not recommended to use tool call template based on stopwords, such as ReAct."
- **llama.cpp:** native format handlers are preferable to the generic handler; "Generic support may consume more tokens and be less efficient than a model's native format," and aggressive KV-cache quantization "can substantially degrade the model's tool calling performance." Parallel calls "are disabled by default."
- **vLLM:** enable with `--enable-auto-tool-choice --tool-call-parser <parser>` and a tool-aware chat template. For `tool_choice="auto"`, strict schema enforcement requires opting in per tool with `strict: true`.
- **Llama 3 vs 4:** parallel tool calls are unsupported on Llama 3; Llama 4 supports them and recommends the pythonic parser.

### When tiers diverge

If the frontier tier needs a capability the local tier cannot select reliably, keep it in the deferred catalog and gate it behind tool search or an explicit workflow, rather than loading it into every turn. Do not let a tool that only the strongest model can disambiguate set the floor. When a behavior is genuinely tier-specific, make it a runtime policy, not a second toolset.

## Implementation

### The execution loop

Build defensively. The response may contain zero, one, or several calls. **[Copy-Safe]** pattern:

```python
# tools and messages are already defined
response = client.chat.completions.create(model=MODEL, tools=TOOLS, messages=messages)

for call in response.choices[0].message.tool_calls or []:
    try:
        args = json.loads(call.function.arguments)
    except json.JSONDecodeError:
        messages.append(informative_error(call, "arguments were not valid JSON"))
        continue
    try:
        result = dispatch(call.function.name, args)
        messages.append(tool_result(call, result))
    except ToolError as err:
        messages.append(tool_result(call, {"error": str(err)}))
```

Check `finish_reason == "tool_calls"` rather than assuming a tool fired. Return informative tool errors so the model can recover instead of crashing the loop.

### Side effects and safety

- Validate and sanitize arguments before acting.
- Require approval for destructive, financial, access-control, communication, and deployment actions.
- Prefer preview-then-commit for consequential mutations; require idempotency keys for retryable writes.
- Keep secrets out of tool arguments and results.
- Treat tool output, resource text, and upstream errors as untrusted data.

### Context budget

Track two budgets: the catalog (definitions) and the results. Anthropic has "seen tool definitions consume 134K tokens before optimization"; a five-server MCP setup reached "~55K tokens before the conversation even starts." Measure the actual overhead of your toolset before optimizing anything else.

## Evaluation

Tool design without evaluation is guessing. Anthropic's method: generate dozens of realistic tasks, run simple agentic loops (one per task) with reasoning and feedback blocks, and collect accuracy, tool calls, tokens, runtime, and errors. Keep a held-out set to prevent overfitting.

**Benchmarks**

- **Berkeley Function Calling Leaderboard (BFCL)** is the de facto standard for selection and argument accuracy, including multi-turn and agentic evaluation. Its authors report that "while state-of-the-art LLMs excel at single-turn calls, memory, dynamic decision-making, and long-horizon reasoning remain open challenges" ([BFCL paper](https://proceedings.mlr.press/v267/patil25a.html)).
- **τ-bench** measures reliability, not just skill: even strong agents "succeed on < 50% of the tasks, and are quite inconsistent (pass^8 < 25% in retail)" ([τ-bench](https://arxiv.org/abs/2406.12045)). Report `pass^k`, not just `pass^1`.

**Description quality is measurable, and rewriting is not free.** A study of 856 tools across 103 MCP servers found "97.1% of the analyzed tool descriptions contain at least one smell, with 56% failing to state their purpose clearly." Augmenting descriptions raised task success by a median of 5.85 percentage points but "increase[d] the number of execution steps by 67.46% and regress[ed] performance in 16.67% of cases." Compact variants preserved the gain with less token overhead ([MCP Tool Descriptions Are Smelly](https://arxiv.org/abs/2602.14878)). A larger study of 10,831 servers found "73% repeated tool names," and in competitive settings "standard-compliant descriptions reach 72% selection probability (260% over a 20% baseline)" ([From Docs to Descriptions](https://arxiv.org/abs/2602.18914)).

**Evaluate every tier.** A catalog that scores well on your frontier model can fail below the floor set by a 3B model. Run the same held-out suite against each supported model and record selection accuracy, argument accuracy, calls, tokens, latency, and recovery.

## Anti-Patterns

- One generated tool per API endpoint.
- Near-duplicate tools distinguished only by description.
- More than ~20–30 always-loaded tools without retrieval.
- Free-form string parameters where an enum would do.
- Deeply nested schemas and contradictory boolean flags.
- Unbounded search, list, or query results.
- Opaque error codes or stack traces returned to the model.
- No negative guidance ("when not to use").
- Relying on the strongest model to compensate for a weak catalog.
- Identical prompt and catalog configuration for every model tier.

## Validation

Before shipping a toolset, confirm:

1. **Catalog budget measured.** Count the tokens your tool definitions consume per turn; confirm it stays within budget and that retrieval activates when it does not.
2. **Strict schema passes.** Validate every tool against strict-mode requirements (`additionalProperties: false`, all properties required, `null` unions for optional fields).
3. **Per-tier selection accuracy.** Run a held-out task set against every supported model; record selection and argument accuracy separately.
4. **Recovery works.** Inject invalid arguments and failing tools; confirm the model repairs the call from the returned error.
5. **Description rubric.** Score each description for purpose clarity, parameter meaning, return shape, and limitations.
6. **Over-call rate.** Measure tool calls on tasks that need no tools; excessive calls indicate missing negative guidance.

## References

- Anthropic — [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) (2025-09-11)
- Anthropic — [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) (2025-11-24)
- Anthropic — [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) (2025-11-04)
- Claude Platform — [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- OpenAI — [Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- Together AI — [Function calling best practices](https://docs.together.ai/docs/inference/function-calling/best-practices)
- GitHub — [Loading tools on demand with tool search (Copilot CLI)](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/copilot-cli/tool-search)
- vLLM — [Tool calling](https://docs.vllm.ai/en/stable/features/tool_calling)
- llama.cpp — [Function calling](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md)
- Qwen — [Function call](https://github.com/QwenLM/Qwen3/blob/main/docs/source/framework/function_call.md)
- Google — [Function calling with the Gemini API](https://ai.google.dev/gemini-api/docs/function-calling)
- Patil et al. — [Berkeley Function Calling Leaderboard](https://proceedings.mlr.press/v267/patil25a.html) (2025)
- Yao et al. — [τ-bench](https://arxiv.org/abs/2406.12045) (ICLR 2025)
- Gan & Sun — [RAG-MCP](https://arxiv.org/abs/2505.03275) (2025)
- Repantis et al. — [How Many Tools Should an LLM Agent See?](https://arxiv.org/abs/2605.24660) (2026)
- [The Tool-Overuse Illusion](https://arxiv.org/abs/2604.19749) (2026)
- Chen — [Looking Is Not Picking](https://arxiv.org/abs/2606.16364) (2026)
- Hasan et al. — [MCP Tool Descriptions Are Smelly!](https://arxiv.org/abs/2602.14878) (2026)
- Wang et al. — [From Docs to Descriptions](https://arxiv.org/abs/2602.18914) (2026)
- [LongFuncEval](https://arxiv.org/abs/2505.10570) (2025)
