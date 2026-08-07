---
title: MCP Server Best Practices Deep Reference
description: Evidence base, protocol detail, templates, and evaluation guidance for architects and AI engineers building reliable and secure Model Context Protocol servers.
status: active
tags: [mcp, servers, tools, security, evaluation, reliability]
last_verified: 2026-08-07
layer: cold
applies_to: Model Context Protocol servers and agent-facing tools
version: 1.0.0
research_cutoff: 2026-08-07
target_protocol: Model Context Protocol 2026-07-28
---

# MCP Server Best Practices Deep Reference

## Overview

A good MCP server is not merely an API that speaks MCP. It is an **agent-facing product surface** whose capabilities are easy for a probabilistic model to discover, choose, parameterize, execute, verify, and recover from.

A good server makes the following path unsurprising:

1. The agent understands what the server is for.
2. The agent sees only capabilities relevant and authorized for the current caller.
3. The agent selects the right primitive and tool without guessing among overlapping alternatives.
4. The agent supplies valid, semantically correct arguments.
5. The server validates both syntax and meaning before causing effects.
6. The result returns high-signal, bounded, machine-readable information.
7. Any failure tells the agent exactly what it can do next.
8. Consequential actions remain constrained, reviewable, and attributable.
9. The same behavior works across supported clients, models, transports, and retries.
10. Realistic evaluations demonstrate these properties continuously.

Protocol correctness is necessary, but not sufficient. MCP benchmarks repeatedly find failures in retrieval, tool choice, parameter semantics, planning, cross-tool composition, and response handling even when the underlying server is syntactically valid. MCP-Bench tests fuzzy instructions, precise parameter control, cross-tool coordination, and multi-step planning across 28 live servers and 250 tools; MCP-Atlas uses 1,000 expert-written tasks across 36 real servers and 220 tools; LiveMCPBench reports that retrieval errors account for nearly half of observed failures in its setting. ([R01](#r01), [R02](#r02), [R03](#r03))

The practical design objective is therefore:

> **Minimize the amount of inference an agent must perform at every interface boundary, while preserving enough flexibility to complete real workflows.**

---

## How to use this document

This file is intentionally written as both a human guide and an AI-reference document.

### Evidence labels

Recommendations are labeled by source type:

- **[PROTOCOL]**: required or explicitly recommended by MCP 2026-07-28.
- **[RESEARCH]**: supported by an empirical paper or benchmark. Most MCP research is recent and often published as an arXiv preprint; peer-review status is stated where known.
- **[PRACTICE]**: reported by an organization operating or evaluating agent tools or MCP servers.
- **[SYNTHESIS]**: a design conclusion derived from the combined evidence. It is not itself a protocol requirement.
- **[CLIENT PROFILE]**: compatibility advice for a particular host or provider, not universal MCP behavior.

### Normative words in this guide

- **PROTOCOL MUST / MUST NOT** reproduces a normative MCP requirement.
- **REQUIRED FOR A GOOD SERVER** is this guide's release bar. It may be stricter than the protocol.
- **SHOULD / SHOULD NOT** is a strong recommendation; deviations need a documented reason and evaluation evidence.
- **MAY** is optional.

### Recommended reading paths

For a new build, read in this order:

1. [The twelve rules](#the-twelve-rules)
2. [Protocol baseline](#protocol-baseline-mcp-2026-07-28)
3. [Workflow-first capability design](#workflow-first-capability-design)
4. [Tool contract design](#tool-contract-design)
5. [Output and error design](#output-and-error-design)
6. [Security](#security-and-trust-boundaries)
7. [Evaluation](#evaluation-program)
8. [Build blueprint](#build-blueprint)
9. [Release checklist](#release-readiness-checklist)

For an AI building a server, start at [AI implementation procedure](#ai-implementation-procedure), then use the templates and checklist as hard constraints.

---

## The twelve rules

| # | Rule | Why it matters | Evidence |
|---|---|---|---|
| 1 | **Design from user workflows, not from API endpoints.** | Raw endpoint parity transfers orchestration burden to the model and creates unnecessary choice. | [PRACTICE] Block reports this as a central lesson from more than 60 MCP servers; Anthropic independently warns against merely wrapping existing APIs. ([P02](#p02), [P01](#p01)) |
| 2 | **Keep the visible tool surface small, coherent, and non-overlapping.** | Tool retrieval and selection degrade as distractors and near-duplicates increase. | [RESEARCH] LiveMCPBench identifies retrieval as a dominant bottleneck; an industry pattern study reports model-specific accuracy drops as tool count grows. ([R02](#r02), [R06](#r06)) |
| 3 | **Treat names, descriptions, schemas, and server instructions as prompts.** | These fields directly influence whether an agent selects the correct tool, order, and arguments. | [PRACTICE] GitHub and Block report this from production work; Anthropic recommends evaluation-driven prompt engineering of tool specs. ([P02](#p02), [P03](#p03), [P01](#p01)) |
| 4 | **Make inputs strict, explicit, and semantically constrained.** | Syntactic validity alone does not prevent wrong units, wrong targets, ambiguous defaults, or unsafe scope. | [PROTOCOL] JSON Schema is the input contract; [SYNTHESIS] semantic checks remain a server responsibility. ([S05](#s05)) |
| 5 | **Return stable structured output plus a concise text representation.** | Structured data supports reliable downstream calls; concise text supports model understanding and compatibility. | [PROTOCOL] `structuredContent` may be governed by `outputSchema`, with a serialized text block recommended for backward compatibility. ([S05](#s05)) |
| 6 | **Bound every potentially large response.** | Unbounded results consume context, increase latency, and bury relevant evidence. | [PRACTICE] Anthropic, Block, GitHub, and Cloudflare all report context savings from filtering, pagination, tool reduction, or progressive disclosure. ([P01](#p01), [P02](#p02), [P05](#p05), [P07](#p07)) |
| 7 | **Make failures model-recoverable.** | Agents can often repair a call when told the field, constraint, cause, and next action. Opaque codes and stack traces waste calls. | [PROTOCOL] Tool-originated errors should be returned with `isError: true` so the model can see and correct them. ([S05](#s05)) |
| 8 | **Separate discovery, reading, preview, and mutation.** | Clear side-effect boundaries improve selection, approvals, idempotency, and auditability. | [PROTOCOL] Tools are model-controlled but hosts should keep a human able to deny calls; annotations describe read-only and destructive behavior. ([S05](#s05)) |
| 9 | **Enforce least privilege in the server, not only in the host.** | Annotations and model instructions are hints, not authorization. | [PROTOCOL] Tool annotations are untrusted hints; authorization must be checked for every request and object. [PRACTICE] GitHub hides tools unavailable to the caller's scopes. ([S05](#s05), [P06](#p06)) |
| 10 | **Use the modern stateless protocol correctly.** | Hidden connection state, stale catalogs, and legacy lifecycle assumptions break scaling and interoperability. | [PROTOCOL] MCP 2026-07-28 removes the initialize handshake and protocol sessions; every request is self-describing. ([S01](#s01), [S03](#s03)) |
| 11 | **Instrument tool semantics, not just transport health.** | A server can be online while selecting badly, timing out, overfetching, or returning unusable errors. | [PRACTICE] GitHub uses offline semantic evaluation; Sentry emphasizes connected traces, errors, and tool-level monitoring. ([P03](#p03), [P09](#p09)) |
| 12 | **Release only through realistic, multi-model, adversarial evaluation.** | Synthetic happy paths overstate reliability and miss permission, injection, ambiguity, and recovery failures. | [RESEARCH] HumanMCP shows the need for varied human-like personas; security benchmarks demonstrate attacks across planning, invocation, and response handling. ([R04](#r04), [R07](#r07), [R08](#r08), [R09](#r09)) |

---

## What the evidence says

### 1. Interface quality determines agent quality

Tool interfaces are contracts between deterministic software and nondeterministic agents. Unlike a conventional caller, an agent may choose the wrong capability, omit a call, invent an argument, misunderstand an identifier, or stop early. Anthropic describes this as a distinct software-design problem and recommends prototypes, held-out evaluations, transcript inspection, and repeated optimization. ([P01](#p01))

GitHub's offline evaluation team states that changing a tool name, description, or parameter definition directly affects whether a model chooses the right tool, in the right order, with the right arguments. This means contract text is executable behavior from the perspective of the overall agent system. ([P03](#p03))

### 2. Tool discovery is a first-class bottleneck

LiveMCPBench evaluates 95 tasks over 70 servers and 527 tools. Its authors report wide performance variation among models and attribute nearly half of failures to retrieval errors in their evaluation. MCP-Zero similarly begins from the observation that injecting thousands of schemas into context is costly, and reports large token savings from active, hierarchical discovery in its own benchmark setting. ([R02](#r02), [R05](#r05))

This does **not** imply a universal maximum number of tools. Tool complexity, descriptions, model, host retrieval, context length, and task distribution all matter. It does imply that a server should measure selection accuracy as its visible catalog changes rather than assuming more tools are harmless.

### 3. Real users do not name tools precisely

MCP-Bench deliberately omits explicit tool names and tests fuzzy instructions, multi-hop planning, and cross-domain coordination. MCP-Atlas also withholds server, tool, and parameter names, then scores atomic outcome claims rather than requiring one exact trajectory. HumanMCP adds varying personas and levels of ambiguity because synthetic, tool-shaped prompts can inflate apparent reliability. ([R01](#r01), [R03](#r03), [R04](#r04))

A good evaluation set therefore includes:

- novice and expert phrasing;
- exact and vague requests;
- synonyms and organization-specific language;
- incomplete requests that should trigger clarification;
- requests that need no tool;
- requests that cannot be completed;
- multiple valid plans;
- distracting but plausible tools.

### 4. Context is a budget, not a free cache

Anthropic recommends returning only high-signal context and resolving cryptic identifiers to meaningful names. Block recommends size checks, pagination, truncation with guidance, and proactive fallback logic. GitHub reports approximately 60-90 percent context reduction in its setting when users load 3-10 selected tools instead of all default toolsets; a later GitHub consolidation reduced one toolset by roughly 23,000 tokens, or 50 percent. Cloudflare reports an extreme large-API case in which a two-tool code-mode interface represented its API in about 1,000 tokens. These are organization-specific measurements, not universal guarantees, but they all support budgeting catalog and result size explicitly. ([P01](#p01), [P02](#p02), [P05](#p05), [P06](#p06), [P07](#p07))

### 5. MCP is not automatically the most efficient interface

Sentry ran 1,350 trials across three models, three approaches, and five coding exercises. All tested approaches exceeded 99 percent task success, but the tested MCP setup consumed substantially more average tokens than a primed shell baseline. The authors' conclusion is not that MCP is bad; it is that MCP's up-front schema and orchestration cost must earn its keep. ([P08](#p08))

Before building, compare MCP against:

- a native function or plugin interface already supported by the host;
- a CLI plus high-quality agent instructions;
- an ordinary API or SDK used through code execution;
- a static resource bundle;
- a direct application integration.

Choose MCP when standardized discovery, reusable cross-host access, scoped tools/resources/prompts, or remote authorization provides enough value to justify the interface and operational surface.

### 6. Security must cover semantics, not only OAuth

Recent security benchmarks examine tool poisoning, name collision, preference manipulation, prompt injection in tool metadata or outputs, out-of-scope arguments, false errors, user impersonation, tool transfer, and mixed attacks. MCPSecBench identifies 17 attack types across four attack surfaces and reports successful compromises across all evaluated surfaces. MCP Security Bench evaluates attacks throughout planning, invocation, and response handling and was accepted at ICLR 2026. MCPTox evaluates tool-poisoning cases built from 45 live servers and 353 authentic tools. ([R07](#r07), [R08](#r08), [R09](#r09))

Many of these studies evaluate hosts, models, and protocol versions predating MCP 2026-07-28. They should be read as evidence of the threat class, not proof that every current client is equally vulnerable. The enduring lesson is that authentication, model alignment, and a trusted server publisher are each insufficient alone. Authorization, catalog integrity, content handling, approval, network controls, and runtime policy must be layered.

---

## Decide whether MCP is the right interface

### Good reasons to build an MCP server

MCP is a strong fit when several of the following are true:

- Multiple AI hosts or agent frameworks should access the same capability.
- Capabilities must be discoverable at runtime rather than compiled into one application.
- A domain has reusable tools, resources, or prompts with clear security boundaries.
- Remote users need standardized OAuth-based access and scoped authorization.
- Tool catalogs or resources need client caching and change notification.
- The same interface should support interactive users, coding agents, and automated workflows.
- The organization can operate a versioned, observable, evaluated service rather than a one-off script.

### Warning signs

Reconsider or reduce scope when:

- The server would expose one trivial operation to one fixed client.
- The design is an automatic one-tool-per-endpoint conversion of a large API.
- The model would receive hundreds or thousands of schemas on every turn with no discovery strategy.
- Every useful task requires long chains of low-level calls.
- The only intended behavior is bulk deterministic processing better expressed as a job or SDK.
- Authorization cannot be enforced per user, tenant, object, and action.
- The team cannot monitor or regression-test tool behavior.
- The interface depends on deprecated protocol features.

### Architecture decision record template

Before implementation, answer:

```yaml
interface_decision:
  user_jobs:
    - "What recurring jobs will agents complete?"
  intended_hosts:
    - "Which MCP clients or agent frameworks must work?"
  alternatives_evaluated:
    - option: "CLI plus instructions"
      result: "Why accepted or rejected"
    - option: "Direct API or SDK through code execution"
      result: "Why accepted or rejected"
    - option: "Native host tools"
      result: "Why accepted or rejected"
  mcp_advantage:
    - "Specific interoperability, discovery, auth, or composition value"
  estimated_visible_tool_count: 0
  estimated_catalog_tokens: 0
  expected_calls_per_top_workflow: 0
  consequential_actions:
    - "List every write, destructive, financial, communication, or external effect"
  operational_owner: "team or service owner"
  evaluation_owner: "team or role"
  decision: "build | build narrow profile | do not build"
```

A design that cannot state its top user jobs and MCP-specific advantage should not proceed to tool implementation.

---

## Protocol baseline: MCP 2026-07-28

This guide targets the latest dated release available at the research cutoff, `2026-07-28`. It is the first modern, stateless protocol revision. Earlier versions through `2025-11-25` are legacy, initialization-based revisions. ([S01](#s01), [S03](#s03), [S17](#s17))

### Modern versus legacy behavior

| Concern | Modern: 2026-07-28 and later | Legacy: 2025-11-25 and earlier |
|---|---|---|
| Lifecycle | No initialization handshake | `initialize` / `initialized` handshake |
| Protocol state | Stateless request/response core | Session-oriented lifecycle |
| Version and capabilities | Supplied per request in `_meta` | Negotiated during initialization |
| HTTP session header | No `Mcp-Session-Id` | Used by some legacy revisions |
| Discovery | Server implements `server/discover`; client call is optional | Initialization response supplies identity/capabilities |
| Cross-call application state | Explicit opaque handles passed as arguments | Implementations often associated state with a session |
| Server-to-client needs | Multi Round-Trip Requests return `input_required` and client retries | Server-initiated requests over bidirectional channels |
| Change notifications | Opt-in `subscriptions/listen` stream | Earlier connection/session notification behavior |

A server MAY support both eras, but a dual-era implementation must keep their semantics distinct. Do not copy initialization-era tutorials into a modern-only implementation. ([S03](#s03))

### Required modern request metadata

Every modern request carries a `_meta` object containing:

- `io.modelcontextprotocol/protocolVersion` - required;
- `io.modelcontextprotocol/clientCapabilities` - required, including an empty object when no optional capabilities apply;
- `io.modelcontextprotocol/clientInfo` - recommended but optional and self-reported.

A server must not infer current capabilities from a prior request. Client identity is for display, logging, and debugging; it is not an authorization signal. ([S14](#s14))

### Required discovery behavior

**PROTOCOL MUST:** every modern server implements `server/discover`. Clients may call it before other RPCs, but are not required to do so. The result identifies supported versions, capabilities, and server information, and is cacheable. ([S04](#s04))

Use `instructions` for short, stable, cross-cutting guidance that helps a model use the server. The schema explicitly says instructions should not duplicate tool descriptions. Good uses include:

- required workflow ordering that spans several tools;
- universal pagination or scoping rules;
- how to interpret server-wide identifiers;
- a concise statement of authoritative versus advisory data;
- a warning that all mutation tools support preview first.

Bad uses include:

- a copy of the entire README;
- one paragraph per tool;
- dynamic user data or timestamps that destabilize prompt caching;
- secrets, authorization decisions, or untrusted content;
- instructions that attempt to override host or user policy.

### Required result discriminator

**PROTOCOL MUST:** results produced under 2026-07-28 include `resultType`. The core values are:

- `complete` - final result;
- `input_required` - additional client or user input is required before retrying.

Clients receiving an older-version result without this field treat it as `complete`, but a modern server should not rely on that compatibility behavior. ([S13](#s13))

### Cacheable operations

Complete results from these operations carry `ttlMs` and `cacheScope`:

- `server/discover`
- `tools/list`
- `prompts/list`
- `resources/list`
- `resources/templates/list`
- `resources/read`

`cacheScope` is `public` only when the response is safe to share across authorization contexts. Otherwise it is `private`. A TTL is a freshness hint, not a guarantee. Results involving MRTR input responses are not cacheable. ([S06](#s06))

### Deterministic catalogs

A tool list may vary by the authorization presented on the request, but it must not vary per connection or as an incidental side effect of another request on that connection. The protocol recommends deterministic ordering because it supports reliable catalog caching and stable model prompt caches. ([S05](#s05))

**REQUIRED FOR A GOOD SERVER:** sort tools, prompts, resources, and templates with a documented stable rule. Do not inject random ordering, request timestamps, volatile counters, or nondeterministic descriptions into catalog responses.

### Modern Streamable HTTP

For MCP 2026-07-28, Streamable HTTP uses a single endpoint that accepts a new POST for every message. The old GET stream and protocol session are removed. Requests include transport metadata headers, including `MCP-Protocol-Version` and `Mcp-Method`; `Mcp-Name` is required for named operations such as `tools/call`, `resources/read`, and `prompts/get`. Servers processing the body must validate header/body agreement. ([S07](#s07))

Security-critical transport rules include:

- validate `Origin` and return 403 for a present but invalid origin;
- bind local servers to `127.0.0.1`, not all interfaces, unless remote exposure is intentional and secured;
- authenticate remote connections;
- use HTTPS for remote deployments;
- validate mirrored header values against the JSON body;
- do not mark passwords, tokens, API keys, or PII with `x-mcp-header`, because headers are visible to intermediaries.

### Multi Round-Trip Requests

Modern servers do not initiate arbitrary requests to clients. When a tool needs user input, approval, or another supported client interaction, it can return `resultType: "input_required"` with input requests and opaque request state; the client retries the original operation with responses and a new JSON-RPC request ID. ([S01](#s01), [S05](#s05))

Use MRTR only when:

- the required client capability is present on that request;
- the missing input cannot be safely inferred;
- continuing without it would be wrong or unsafe;
- the request state is opaque, integrity-protected, bounded in lifetime, and bound to the caller and operation.

Provide a non-MRTR fallback where practical, such as a model-recoverable tool error saying which explicit argument is required.

### Deprecated features

As of 2026-07-28, Roots, Sampling, protocol Logging, and legacy HTTP+SSE are deprecated with a minimum deprecation window. New implementations should not adopt them. For new work:

- integrate directly with a model provider rather than relying on MCP Sampling;
- log to `stderr` for stdio and use OpenTelemetry or service-side telemetry for remote servers;
- use modern Streamable HTTP rather than legacy HTTP+SSE;
- avoid new dependencies on Roots.

([S01](#s01), [S16](#s16))

### Conformance is a floor

Use the official Inspector during development and the MCP conformance framework in CI. The framework validates messages against the wire schema and provides modern-version server scenarios. ([S11](#s11), [S12](#s12))

```bash
# Interactive inspection
npx @modelcontextprotocol/inspector --server-url https://api.example.com/mcp --transport http

# Protocol conformance
npx @modelcontextprotocol/conformance server \
  --url https://api.example.com/mcp \
  --suite active
```

Passing conformance proves protocol behavior, not that a model can use the server well. Semantic and security evaluation are separate release gates.

---

## Server boundary and primitive selection

MCP servers are intended to be focused, composable, and isolated. The architecture emphasizes that a server should receive only the context needed for its responsibility, not an entire conversation or visibility into other servers. ([S02](#s02))

### Choose a focused server boundary

A coherent server usually aligns with one of these boundaries:

- one product or service;
- one bounded domain, such as incident response or expense management;
- one trust zone or data classification;
- one operational team and authorization model;
- one workflow family with common concepts and identifiers.

Split a server when capabilities require materially different credentials, approval policies, data classifications, uptime characteristics, or owners. Do not split merely because the underlying API has separate microservices if the agent sees one cohesive workflow.

### Select the correct primitive

| Primitive | Control model | Use it for | Do not use it for |
|---|---|---|---|
| **Tool** | Model-controlled | Retrieval requiring computation or parameters; actions; mutations; queries; workflow steps | Static context that can be addressed and read as a resource; user-chosen reusable prompt templates |
| **Resource** | Application-controlled | Files, records, schemas, reports, artifacts, logs, or documents identified by URI and attached as context | A disguised action; an unbounded database dump; a mutation |
| **Prompt** | User-controlled | Explicitly selected templates or guided workflows, such as a review checklist or investigation starter | Hidden mandatory policy; automatic model actions; general tool documentation |

This control hierarchy is part of the MCP server model. ([S10](#s10))

### Primitive decision questions

1. Does invoking it cause an external effect? Use a tool.
2. Does it retrieve computed or filtered data based on arguments? Usually use a tool.
3. Is it stable content that can be named by URI and selectively attached? Use a resource.
4. Should a user explicitly choose a reusable interaction template? Use a prompt.
5. Would the result be too large for a tool response but useful on demand? Return a resource link from the tool.

### Resource design rules

- Use stable, canonical URIs.
- Include meaningful names, descriptions, MIME types, and modification metadata.
- Keep `resources/list` selective and paginated; do not list millions of records.
- Use templates for parameterized resource families.
- Make `resources/read` bounded or range-aware for large content.
- Return a resource link rather than embedding a large artifact in a tool result.
- Apply authorization on every list and read; a URI is not an authorization token.
- Set `cacheScope` correctly and use conservative TTLs for user-specific or rapidly changing data.

### Prompt design rules

- Treat prompts as user-invoked templates, not as invisible policy enforcement.
- Keep arguments typed and clearly described.
- Keep the template stable and concise.
- Do not embed secrets or live user data in a list response.
- Test rendered prompts for injection boundaries and accidental authority escalation.
- Version materially changed templates or preserve compatibility aliases.


## Workflow-first capability design

### Start with jobs, not endpoints

A server should begin with a ranked inventory of user jobs and agent workflows, not an OpenAPI document.

For each job, record:

- the user's intended outcome;
- the minimum information needed to begin;
- the objects and identifiers involved;
- the expected sequence of reads, decisions, previews, and writes;
- side effects and reversibility;
- permission and approval boundaries;
- common ambiguity and failure modes;
- the evidence the agent needs to verify completion.

A useful workflow statement is concrete and outcome-oriented:

```text
When an on-call engineer asks why checkout errors increased, the agent should:
1. identify the affected service and time window;
2. retrieve the highest-signal errors and traces;
3. correlate them with recent deploys;
4. return ranked findings with links and timestamps;
5. avoid mutating production state.
```

A poor starting point is a list such as `listProjects`, `getProject`, `listEvents`, `getEvent`, and `searchEverything`. That list describes an implementation, not the decisions an agent must make.

Block summarizes its production lesson as: "Design top-down from workflows, not bottom-up from API endpoints." ([P02](#p02))

### Build a workflow-to-capability map

Before naming tools, create a table like this:

| User job | Read steps | Decision point | Write step | Verification | Candidate capability |
|---|---|---|---|---|---|
| Investigate failed payment | Find transaction and related logs | Determine likely failure class | None | Return source records and confidence | `payments_investigate_failure` |
| Correct shipping address | Resolve order and validate status | Is the order still editable? | Change address | Re-read order and return revision | `order_address_change_preview`, `order_address_change_commit` |
| Create weekly report | Retrieve metrics and incidents | Select date range and grouping | Create report artifact | Return resource URI | `weekly_report_create` |

This map exposes duplicated steps, hidden dependencies, and places where one workflow-shaped tool can remove fragile orchestration.

### Choose the right tool granularity

There is no universal rule that every tool must be atomic or every workflow must be collapsed. Use the following test.

Create a workflow-shaped tool when:

- low-level calls almost always occur together in one fixed sequence;
- the server can perform the sequence more reliably, cheaply, or securely;
- the intermediate data has little independent value to the agent;
- server-side execution can enforce transactional or authorization invariants;
- the tool can still return enough evidence for the agent to verify the outcome.

Keep operations separate when:

- steps are independently useful across many workflows;
- the agent must inspect an intermediate result before deciding what to do;
- the write requires explicit approval or user confirmation;
- different steps have different permissions or trust boundaries;
- combining them would create a large, ambiguous "god tool."

A practical pattern is **coarse reads, explicit writes**: let the server aggregate a bounded investigation or lookup, but keep consequential mutations narrowly named and separately callable.

### Prefer semantic operations over transport operations

Tool names should reflect domain intent:

```text
Good:    incident_search, incident_get, incident_assign
Weak:    api_get_v2_incidents, post_incident_id_assignee
```

Do not force an agent to understand endpoint paths, HTTP verbs, pagination internals, or transport-specific naming unless those details are part of the user's domain.

### Separate search, fetch, preview, and commit

A high-reliability capability surface commonly uses these stages:

1. **Search or resolve**: locate candidate objects from natural identifiers.
2. **Fetch or inspect**: retrieve authoritative details for one object.
3. **Preview or validate**: show the exact proposed effect and policy checks.
4. **Commit**: perform the mutation using a stable object identifier and, when appropriate, a preview token or revision.
5. **Verify**: return the authoritative post-write state or a resource link.

Example:

```text
customer_search
customer_get
subscription_change_preview
subscription_change_commit
```

This design is safer than a single `manage_subscription` tool and more usable than dozens of endpoint-shaped tools.

### Consolidate only when the shared contract is clear

A single tool with an `operation` enum can be appropriate for closely related operations that share:

- the same object type;
- the same authorization boundary;
- the same input and output shape;
- the same side-effect class;
- a small, mutually exclusive operation set.

For example, `label_manage` with `operation: add | remove` may be clearer than two almost identical tools. Do not consolidate unrelated actions into `resource_manage` with a dozen modes and a union of incompatible parameters. Large discriminated unions increase description length, validation complexity, and tool-call errors.

### Measure overlap explicitly

For every pair of tools, answer:

- Could the same user request plausibly match both descriptions?
- Does one tool subsume the other?
- Are their names distinguishable before the model reads the full schema?
- Is the difference a domain concept or merely an implementation detail?
- Can one be removed, renamed, scoped, or made an operation of the other?

Maintain an **overlap matrix** during design. Any pair marked "high ambiguity" must be resolved or covered by adversarial selection evaluations before release.

### Do not adopt a fixed maximum tool count

Research and production reports agree that large catalogs can hurt retrieval and consume context, but the failure point varies by model, host, schema size, and task distribution. One recent industry study found model-specific selection degradation at different catalog sizes; it should be treated as a warning to measure, not a universal numerical law. ([R06](#r06))

Required practice:

- establish a baseline selection score for the intended catalog;
- add distractor tools during evaluation;
- load only capabilities authorized and relevant to the caller;
- create smaller toolsets or scopes for distinct jobs;
- re-run evaluation whenever tools or descriptions change.

### Design for multiple valid plans

A well-designed server should not require an agent to reproduce one hidden call sequence when several safe sequences produce the same outcome. Evaluate outcome claims and invariants, not only exact traces. MCP-Atlas uses claim-level scoring for this reason. ([R03](#r03))

Trace constraints are still appropriate for safety, for example:

- a commit must not precede its required approval;
- a mutation must use an authoritative object ID;
- a retry must not duplicate a non-idempotent write;
- a caller must not access an unauthorized tenant.

---

## Tool contract design

The tool contract is an agent-facing prompt, a validation boundary, and a long-lived public interface. Treat its name, title, description, input schema, output schema, and annotations as one coherent design artifact.

### Naming rules

**PROTOCOL MUST:** tool names are unique within the server, 1 to 128 characters, and use only ASCII letters, digits, underscore, hyphen, or dot. ([S05](#s05))

**REQUIRED FOR A GOOD SERVER:**

- Use stable semantic names such as `domain_resource_verb` or `resource_verb`.
- Put the differentiating concept early: `invoice_search` versus `invoice_get`.
- Use one vocabulary consistently: do not alternate among `find`, `lookup`, `query`, and `search` without a real semantic distinction.
- Name mutations with the effect they cause: `incident_resolve`, not `incident_update`.
- Avoid generic names such as `execute`, `run`, `request`, `manage`, `query`, or `do_action` unless a narrowly defined domain noun makes them unambiguous.
- Avoid version numbers and transport details unless the semantic contract truly differs.
- Do not rename a released tool casually. Preserve a compatibility alias or version the surface when clients may cache names.

A recommended vocabulary:

| Verb | Meaning |
|---|---|
| `search` | Return ranked candidate objects from filters or natural identifiers |
| `list` | Enumerate a bounded collection with deterministic pagination |
| `get` | Return one authoritative object by canonical identifier |
| `preview` | Validate and show a proposed effect without causing it |
| `create` | Create a new object |
| `update` | Change specified fields on an existing object |
| `delete` | Remove an object, normally destructive |
| `start` | Begin an asynchronous operation and return a handle |
| `status` | Read operation state by handle |
| `cancel` | Request termination of an operation |
| `export` | Create an artifact and return a resource URI or download reference |

### Description template

A strong description answers six questions in a compact order:

1. What outcome does this tool produce?
2. When should the agent use it?
3. When should the agent not use it?
4. What identifiers, permissions, or preconditions are required?
5. What side effects occur?
6. What does the result contain and how is it bounded?

Template:

```text
Use this tool to <specific outcome>.
Use it when <positive selection conditions>.
Do not use it for <nearest confusing alternatives>; use <other tool> instead.
Requires <identifier, permission, or prior step>.
This tool <has no side effects | causes exact side effect>.
Returns <high-signal result shape, ordering, and pagination/truncation behavior>.
```

Example:

```text
Search for customer accounts by email, name, or external reference.
Use this before customer_get when the canonical customer_id is unknown.
Do not use it to search invoices; use invoice_search instead.
This tool is read-only and returns at most 20 ranked matches with canonical IDs,
status, display name, and an optional next_cursor.
```

Descriptions should be self-contained. Do not rely on a model knowing product jargon, undocumented acronyms, hidden UI behavior, or the order tools happen to appear in a catalog.

### Use server instructions for global routing only

Modern `server/discover` may return concise `instructions` to help the model understand server-wide usage. The protocol says these instructions should help the model and should not duplicate individual tool descriptions. ([S04](#s04))

Good server instructions explain:

- the domain and authoritative scope of the server;
- global terminology and canonical identifiers;
- a small number of cross-tool sequencing rules;
- general safety or approval expectations;
- where the server is not authoritative.

Bad server instructions contain:

- a copy of every tool description;
- volatile timestamps or per-user data that defeat caching;
- hidden attempts to override host or user policy;
- long tutorials that consume context on every discovery;
- claims that annotations or instructions replace authorization.

### Parameter descriptions are part of the contract

Every non-obvious parameter should state:

- domain meaning;
- accepted format;
- units and timezone;
- whether it is a canonical ID, display name, or free text;
- default behavior when omitted;
- allowed range or enum meanings;
- interaction with other fields;
- one short example when ambiguity remains.

Weak:

```json
{"start": {"type": "string"}}
```

Strong:

```json
{
  "start_time": {
    "type": "string",
    "format": "date-time",
    "description": "Inclusive RFC 3339 timestamp. Convert the user's local time to an explicit offset before calling. Example: 2026-08-07T09:00:00+08:00."
  }
}
```

### Input schema rules

**PROTOCOL:** the input schema root is an object. JSON Schema 2020-12 is the default dialect unless another dialect is explicitly declared. A no-argument tool should use an explicit empty object schema, preferably with `additionalProperties: false`. ([S05](#s05))

**REQUIRED FOR A GOOD SERVER:**

- Set `additionalProperties: false` unless extensibility is intentional and tested.
- Mark genuinely required fields in `required`; do not make everything optional and infer intent later.
- Use enums for closed choices and explain each value.
- Use `minimum`, `maximum`, `minLength`, `maxLength`, `minItems`, `maxItems`, and `pattern` where they express real constraints.
- Use standard formats such as `date`, `date-time`, `uri`, and `email` when valid, but still perform server-side validation.
- Keep nesting shallow and object shapes regular.
- Prefer one clear discriminant to overlapping `oneOf` branches.
- Avoid accepting both names and IDs in one ambiguous string field. Use separate fields or a resolve step.
- Represent money with an exact decimal string plus ISO currency, or documented integer minor units; do not use imprecise floating-point values without an explicit contract.
- Require an explicit timezone or offset for instants. Distinguish a calendar date from a timestamp.
- Bound arrays and batch sizes.
- Do not use free-form JSON as an escape hatch unless the tool's purpose is explicitly to carry a documented DSL.

### Validate semantics after schema validation

JSON Schema cannot prove all domain rules. The server must validate, before causing effects:

- object existence and current revision;
- tenant ownership and caller authorization;
- compatible field combinations;
- temporal ordering and business-hour rules;
- state transitions, such as whether a closed incident can be reassigned;
- monetary and quota limits;
- target environment, region, or account;
- whether a preview token still matches the proposed action;
- whether an idempotency key has already been used with different arguments.

Return recoverable tool errors for semantic validation failures. Never silently coerce a materially different request.

### Defaults must be safe and visible

A default is part of the tool's behavior even when it is absent from the schema call. Defaults should:

- minimize scope and side effects;
- be stable across time and users unless explicitly contextual;
- be described in the parameter or tool description;
- appear in the result metadata when they materially affect output;
- never choose a production environment, broad tenant scope, destructive mode, or "all time" range merely because the caller omitted a value.

For ambiguous consequential inputs, ask for clarification through the host workflow rather than guessing.

### Output schema rules

Use `outputSchema` for any result that another tool, agent step, or application may consume. It should describe the successful `structuredContent` shape, not transport errors.

A good output schema:

- has a stable top-level object;
- separates summary metadata from records;
- includes canonical IDs and human-readable labels;
- represents pagination and truncation explicitly;
- marks warnings and partial success explicitly;
- avoids polymorphic shapes where the same field changes type;
- documents nullability and absence;
- is versioned when a breaking change is unavoidable.

### Set annotations explicitly, but never trust them for enforcement

Tool annotations are hints to clients and models, not a security mechanism. In the modern specification, omitted hints have defaults that may surprise authors: `readOnlyHint` defaults to false, `destructiveHint` to true, `idempotentHint` to false, and `openWorldHint` to true. Set each annotation deliberately. ([S05](#s05))

Example:

```json
{
  "name": "incident_comment_add",
  "title": "Add incident comment",
  "description": "Add a plain-text comment to one incident. Requires the canonical incident_id. This changes external state but does not delete data. Repeating the same request may create duplicate comments unless idempotency_key is supplied.",
  "annotations": {
    "readOnlyHint": false,
    "destructiveHint": false,
    "idempotentHint": false,
    "openWorldHint": true
  }
}
```

Even when a tool says it is read-only, the server must constrain its implementation to read-only dependencies and test that invariant.

### A complete example contract

```json
{
  "name": "invoice_search",
  "title": "Search invoices",
  "description": "Search invoices visible to the caller. Use this when the canonical invoice_id is unknown. Do not use it to retrieve line-item detail for a known invoice; use invoice_get. Read-only. Returns at most 25 invoices ordered by relevance, then updated_at descending, with an optional next_cursor.",
  "inputSchema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "query": {
        "type": "string",
        "minLength": 1,
        "maxLength": 200,
        "description": "Customer name, invoice number, purchase-order reference, or exact email."
      },
      "status": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": ["draft", "open", "paid", "void", "overdue"]
        },
        "uniqueItems": true,
        "maxItems": 5,
        "description": "Optional status filter. Omit to search all statuses visible to the caller."
      },
      "issued_from": {
        "type": "string",
        "format": "date",
        "description": "Inclusive invoice issue date in YYYY-MM-DD. This is a calendar date, not a timestamp."
      },
      "issued_to": {
        "type": "string",
        "format": "date",
        "description": "Inclusive invoice issue date in YYYY-MM-DD. Must not precede issued_from."
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 25,
        "default": 10,
        "description": "Maximum records to return. The server may return fewer."
      },
      "cursor": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048,
        "description": "Opaque next_cursor from a prior call. Do not construct or modify it."
      }
    },
    "required": ["query"]
  },
  "outputSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "items": {
        "type": "array",
        "items": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "invoice_id": {"type": "string"},
            "invoice_number": {"type": "string"},
            "customer_name": {"type": "string"},
            "status": {"type": "string"},
            "amount": {
              "type": "object",
              "additionalProperties": false,
              "properties": {
                "decimal": {"type": "string", "pattern": "^-?[0-9]+(\\.[0-9]+)?$"},
                "currency": {"type": "string", "pattern": "^[A-Z]{3}$"}
              },
              "required": ["decimal", "currency"]
            },
            "issued_date": {"type": "string", "format": "date"},
            "canonical_url": {"type": "string", "format": "uri"}
          },
          "required": ["invoice_id", "invoice_number", "customer_name", "status", "amount", "issued_date"]
        }
      },
      "next_cursor": {"type": ["string", "null"]},
      "has_more": {"type": "boolean"},
      "warnings": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["items", "next_cursor", "has_more", "warnings"]
  },
  "annotations": {
    "readOnlyHint": true,
    "destructiveHint": false,
    "idempotentHint": true,
    "openWorldHint": true
  }
}
```

### Review the contract as a prompt

Before implementation, run the contract through at least these reviews:

- **Human review:** can a domain expert distinguish it from neighboring tools?
- **Schema review:** are all invalid or dangerous shapes rejected?
- **Model selection review:** does the target model choose it from realistic prompts and distractors?
- **Argument review:** does the model construct valid and semantically correct fields?
- **Security review:** could untrusted descriptions or returned content redirect behavior?
- **Compatibility review:** does it work in each intended host, transport, and model profile?

Anthropic's observation captures the desired outcome: "tools that are most 'ergonomic' for agents also end up being surprisingly intuitive to grasp as humans." ([P01](#p01))

---

## Output and error design

A result should help the agent answer three questions with minimal inference:

1. What happened?
2. What evidence or object should I use next?
3. Is there anything incomplete, risky, or requiring another call?

### Return structured data and concise text

For machine-consumable results, return `structuredContent` that conforms to the declared `outputSchema`. Also return a concise text serialization in `content` for hosts and models that do not fully exploit structured output. This compatibility pattern is recommended by the MCP tools specification. ([S05](#s05))

Example successful result:

```json
{
  "resultType": "complete",
  "content": [
    {
      "type": "text",
      "text": "Found 2 matching invoices. One is overdue. More results are available."
    }
  ],
  "structuredContent": {
    "items": [
      {
        "invoice_id": "inv_01J...",
        "invoice_number": "INV-1042",
        "customer_name": "Example Labs",
        "status": "overdue",
        "amount": {"decimal": "1250.00", "currency": "USD"},
        "issued_date": "2026-07-01",
        "canonical_url": "https://billing.example.com/invoices/inv_01J..."
      },
      {
        "invoice_id": "inv_01K...",
        "invoice_number": "INV-1050",
        "customer_name": "Example Labs",
        "status": "paid",
        "amount": {"decimal": "480.00", "currency": "USD"},
        "issued_date": "2026-07-20",
        "canonical_url": "https://billing.example.com/invoices/inv_01K..."
      }
    ],
    "next_cursor": "eyJvZmZzZXQiOjI...",
    "has_more": true,
    "warnings": []
  },
  "isError": false
}
```

The prose is a summary, not a second verbose copy of every field.

### Use a stable success envelope

For collection-style results, a strong general envelope is:

```json
{
  "summary": "Short factual outcome",
  "items": [],
  "next_cursor": null,
  "has_more": false,
  "truncated": false,
  "warnings": [],
  "provenance": {
    "source": "authoritative-system-name",
    "retrieved_at": "2026-08-07T12:00:00Z"
  }
}
```

Not every tool needs every field. Consistency across related tools, however, reduces downstream branching and makes pagination and warnings obvious.

### Put high-signal fields first

Prefer fields that support the user's decision or the next tool call:

- canonical ID;
- human-readable name or title;
- status and relevant state;
- the few fields that distinguish candidates;
- timestamps with explicit offsets;
- canonical URL or resource URI;
- source, revision, and retrieval time when freshness matters;
- confidence or match reason only when it has a defensible meaning.

Avoid returning by default:

- internal database columns;
- empty or duplicate fields;
- implementation-only IDs without display labels;
- large nested blobs that the current workflow will not use;
- raw HTML, stack traces, or complete HTTP exchanges;
- verbose prose that repeats structured fields;
- speculative explanations presented as source facts.

Anthropic specifically recommends resolving cryptic identifiers into meaningful language and returning only high-signal context. ([P01](#p01))

### Make provenance and freshness inspectable

An agent must know whether a result is authoritative, cached, partial, or stale when that distinction affects the answer.

Recommended metadata:

```json
{
  "provenance": {
    "system": "crm-primary",
    "record_revision": "42",
    "retrieved_at": "2026-08-07T10:16:44Z",
    "cache_status": "miss",
    "freshness_seconds": 0
  }
}
```

Do not claim freshness more precisely than the upstream system supports. For replicated or eventually consistent data, say so in the contract and result warnings.

### Bound every variable-size dimension

Every list, string, log excerpt, document, diff, artifact, and nested collection needs a limit.

Required mechanisms as applicable:

- server-enforced maximum page size;
- opaque cursor pagination with a stable sort order;
- time-range limits;
- maximum query length and batch size;
- field projection or detail levels;
- aggregation and top-k modes;
- excerpt or byte limits;
- resource links for large artifacts;
- explicit `truncated`, `has_more`, or `next_cursor` fields;
- guidance on the next narrower call.

A server should never silently drop records. If it truncates, disclose the fact and provide a route to continue or narrow the request.

### Prefer cursors to mutable offsets

For changing datasets, opaque cursors are generally safer than numeric offsets because they can encode sort position, filters, and snapshot semantics. Treat cursors as untrusted opaque input:

- authenticate or sign them;
- bind them to the caller, tenant, query, and expiry where appropriate;
- reject modified or expired cursors with a recoverable error;
- never let a cursor widen authorization scope.

### Offer bounded response profiles

When a workflow needs both compact search results and rich detail, use separate `search` and `get` tools or a small, explicit detail enum:

```json
{
  "detail": {
    "type": "string",
    "enum": ["summary", "standard", "full"],
    "default": "standard",
    "description": "Controls documented fields only. 'full' remains subject to size limits and may return resource links for large content."
  }
}
```

Do not expose arbitrary SQL-like field access or unrestricted expansions merely to save tool definitions. Such flexibility shifts validation and data-governance risk to the model.

### Return links or resources for large artifacts

A tool that creates or locates a large report, file, trace bundle, export, or document should normally return:

- a concise summary;
- the artifact's identity, MIME type, size, and expiry;
- a canonical resource URI or resource link;
- an excerpt only when useful;
- any access or retention caveats.

This preserves context while allowing the host to attach the artifact selectively.

### Distinguish protocol errors from tool-execution errors

Use a JSON-RPC or protocol error when the request cannot be understood or processed as an MCP request, for example:

- malformed JSON-RPC;
- unknown method;
- invalid protocol metadata;
- structurally invalid tool-call request;
- unsupported protocol version.

Use a normal tool result with `isError: true` when the tool was understood but could not complete, for example:

- unknown object ID;
- invalid domain state;
- missing permission;
- rate limit;
- upstream timeout;
- stale revision;
- failed business validation.

The model sees tool results and can often repair them; protocol errors may not be exposed in a similarly useful way. This distinction is explicit in the tools specification. ([S05](#s05))

### Make execution errors actionable

A model-recoverable error should state:

- a stable machine code;
- a concise explanation in domain language;
- the offending field or object, when safe;
- whether retrying unchanged could work;
- when a retry is appropriate;
- the exact safe next action;
- a request or trace ID for operators;
- no secrets, stack traces, or raw upstream payloads.

Example:

```json
{
  "resultType": "complete",
  "content": [
    {
      "type": "text",
      "text": "The incident changed after it was read. Fetch the incident again, review revision 18, and retry with that revision."
    }
  ],
  "structuredContent": {
    "error": {
      "code": "STALE_REVISION",
      "message": "Expected revision 17 but current revision is 18.",
      "field": "expected_revision",
      "retryable": true,
      "retry_after_ms": 0,
      "suggested_action": {
        "tool": "incident_get",
        "arguments": {"incident_id": "inc_01J..."}
      },
      "request_id": "req_01K..."
    }
  },
  "isError": true
}
```

The suggested action is advisory. The host and model still apply their own policy and should not execute untrusted instructions blindly.

### Use a small error taxonomy

Recommended cross-tool categories:

| Code family | Meaning | Typical recovery |
|---|---|---|
| `INVALID_ARGUMENT` | Field is syntactically or semantically invalid | Correct the named field |
| `AMBIGUOUS_TARGET` | Several objects match | Present choices or call `get` with one canonical ID |
| `NOT_FOUND` | Authorized caller cannot locate object | Re-check identifier or search; avoid revealing unauthorized existence |
| `PERMISSION_DENIED` | Caller lacks required permission | Request appropriate scope or stop |
| `PRECONDITION_FAILED` | Object state does not permit action | Refresh object and choose a valid transition |
| `STALE_REVISION` | Optimistic concurrency check failed | Re-read and retry after review |
| `CONFLICT` | Operation conflicts with an existing state or idempotency record | Inspect the conflict and decide |
| `RATE_LIMITED` | Caller or upstream quota exceeded | Retry after declared delay or narrow request |
| `UPSTREAM_UNAVAILABLE` | Dependency is temporarily unavailable | Retry only if safe and within deadline |
| `DEADLINE_EXCEEDED` | Work did not finish before deadline | Narrow request, poll a handle, or retry if idempotent |
| `RESULT_TOO_LARGE` | Requested result exceeds a hard bound | Add filters, paginate, or use an export/resource tool |
| `POLICY_BLOCKED` | Safety or organizational policy forbids action | Explain the allowed alternative, if any |

Map upstream-specific codes into this stable taxonomy while preserving an operator-only cause in telemetry.

### Avoid error-loop traps

Do not tell an agent merely to "try again" when retrying unchanged is deterministic. Set `retryable: false` for validation, permission, and policy failures. Set a concrete retry delay for throttling or transient dependency errors. Include an attempt limit in host or server policy.

For automatic retries:

- retry only idempotent reads or writes protected by an idempotency key;
- use bounded exponential backoff with jitter;
- honor the operation deadline;
- stop on cancellation;
- log every attempt under one trace;
- surface the final cause, not a generic exhaustion message.

### Represent partial success honestly

Batch and multi-source tools should avoid treating one failed item as either total success or opaque total failure.

Example:

```json
{
  "summary": "8 of 10 records updated; 2 failed validation.",
  "succeeded": [
    {"record_id": "r1", "revision": "6"}
  ],
  "failed": [
    {
      "record_id": "r9",
      "error": {
        "code": "PRECONDITION_FAILED",
        "message": "The record is archived and cannot be edited.",
        "retryable": false
      }
    }
  ],
  "partial": true
}
```

A batch write should document whether it is atomic. Do not leave the model to infer whether successful items were rolled back.

### Verify writes in the result

A successful mutation should return authoritative post-write evidence:

- canonical object ID;
- new revision or version;
- changed fields or compact diff;
- resulting status;
- effective timestamp;
- actor or automation identity, when appropriate;
- canonical URL;
- warnings about asynchronous propagation;
- idempotency replay status.

Do not return only `{"success": true}`. That forces another call and makes it difficult to tell whether the intended effect occurred.

---

## Explicit state and workflow patterns

MCP 2026-07-28 has no protocol session. Any operation that spans requests must make its state explicit through an opaque handle, durable object ID, cursor, preview token, or operation token. ([S01](#s01), [S03](#s03), [S05](#s05))

### State-handle requirements

A handle should be:

- opaque and non-guessable;
- scoped to the authenticated caller, tenant, and operation;
- authorized on every use;
- integrity-protected and, where needed, encrypted;
- assigned an explicit lifetime and expiry behavior;
- safe to log only in redacted or hashed form when it grants capability;
- revocable when the related permission or object changes;
- unusable to widen filters or switch targets.

An expired handle should return an actionable error such as `HANDLE_EXPIRED`, including whether the workflow can be restarted safely.

### Pattern: search, then get

Use when natural language may match multiple objects.

```text
account_search(query) -> ranked candidates with canonical account_id
account_get(account_id) -> authoritative detail
```

Search results should contain enough distinguishing fields to choose safely, but not the entire object.

### Pattern: resolve, then act

Use when a mutation target may be expressed by a mutable name or ambiguous reference.

```text
repository_resolve(owner, name) -> repository_id, canonical_name, revision
repository_archive(repository_id, expected_revision) -> post-write state
```

The write uses the canonical ID, not the original free-text phrase.

### Pattern: preview, then commit

Use for consequential, expensive, broad, or hard-to-reverse effects.

```text
access_change_preview(subject_id, requested_roles)
  -> exact additions/removals, policy warnings, preview_token, expires_at

access_change_commit(preview_token, idempotency_key)
  -> applied diff, revision, audit reference
```

The server must bind the preview token to:

- caller and tenant;
- exact normalized arguments;
- current relevant revision;
- policy evaluation;
- expiry;
- one or documented repeated uses.

If anything material changes, the commit fails and requires a new preview.

### Pattern: start, status, cancel

Use for work that may exceed a normal request deadline.

```text
export_start(filters, format) -> operation_handle, status, poll_after_ms
export_status(operation_handle) -> pending | running | succeeded | failed | cancelled
export_cancel(operation_handle) -> cancellation outcome
```

A successful status response may return a resource URI rather than embedding the artifact. Cancellation is a request, not a guarantee; report whether the operation stopped and whether any effects remain.

### Pattern: lease or lock

Use only when the domain truly needs exclusive ownership.

```text
record_lease_acquire(record_id, duration_seconds)
record_update(record_id, lease_handle, changes)
record_lease_release(lease_handle)
```

Leases need bounded duration, ownership checks, renewal rules, and cleanup. Prefer optimistic concurrency for ordinary edits because hidden or abandoned locks are hostile to agent workflows.

### Pattern: bounded batch

A batch tool is useful when it reduces repeated overhead and the operation semantics are uniform.

Required controls:

- hard maximum item count and payload size;
- item-level validation before side effects;
- documented atomic versus partial semantics;
- per-item result and error;
- idempotency behavior;
- no cross-tenant mixing;
- total deadline and cancellation behavior.

Do not let an unbounded batch parameter become a bulk-exfiltration or denial-of-service mechanism.

### Use idempotency keys for retryable writes

For a write that may be retried because of transport uncertainty:

- accept a caller-generated idempotency key;
- bind the key to caller, tenant, tool, and normalized arguments;
- return the original result for an identical replay;
- return `CONFLICT` if the key is reused with different arguments;
- retain the record for a documented period;
- include `idempotency_replayed: true | false` in the result.

Do not label a write idempotent merely because the underlying HTTP method is `PUT` or because duplicate effects are unlikely.

### Use optimistic concurrency for mutable objects

Accept `expected_revision`, `etag`, or an equivalent precondition for writes that depend on observed state. On mismatch, return the current revision and a safe re-read action without leaking unauthorized data.

This prevents an agent from overwriting changes made between inspection and action.

### Multi Round-Trip Requests are not hidden sessions

MRTR can ask for additional input during one logical request, but the server must still remain stateless between requests. Use MRTR only when the client advertises the required capability and when the interaction is clearer than returning a recoverable result. Always provide a compatible fallback for clients that do not support it. ([S01](#s01), [S04](#s04))

Use MRTR sparingly for:

- obtaining a missing human decision needed to complete the same operation;
- client-mediated model work that the client explicitly supports;
- elicitation that is bounded, auditable, and non-secret.

Do not use MRTR to recreate a long-lived protocol session, hide authorization state, or block indefinitely.

---

## Context and token efficiency

Efficiency is not the fewest tokens at any cost. It is the lowest total latency, token use, tool calls, and failure rate needed to complete the intended task safely.

### Maintain a context budget

Track at least four components:

```text
catalog cost
+ server-instruction cost
+ tool-call argument cost
+ result and error cost
= MCP context cost per workflow
```

Also track the downstream cost of poor interfaces: extra selection attempts, repair calls, duplicate reads, and model reasoning over noisy output.

A compact catalog that causes more failures may be less efficient than a slightly richer, clearer one.

### Budget every tool definition

For each tool, record:

- serialized definition tokens in each target host;
- description tokens;
- schema tokens;
- selection frequency;
- selection precision and recall;
- argument-validity rate;
- average result tokens;
- average calls per successful workflow;
- incremental benefit relative to neighboring tools.

Remove or gate tools that consume persistent context but contribute little to successful tasks.

### Use deterministic, cacheable discovery

Modern MCP makes discovery and complete list/read operations cacheable with explicit `ttlMs` and `cacheScope`. Catalogs should be deterministically ordered and should not vary because of connection-side effects. ([S04](#s04), [S06](#s06))

To preserve cacheability:

- keep server instructions stable;
- omit current timestamps, random examples, request IDs, and ephemeral banners from discovery;
- sort tools, prompts, resources, and templates deterministically;
- vary catalogs only by legitimate request context such as authorization, protocol version, locale, or negotiated capabilities;
- use `private` cache scope for user- or tenant-specific results;
- use conservative TTLs for authorization-sensitive catalogs;
- invalidate or version cache keys when permissions or definitions change.

### Expose only relevant and authorized capabilities

A model should not see tools it cannot call. Filtering reduces confusion and information leakage, but it is not a substitute for authorization at invocation time.

Useful filtering dimensions:

- OAuth scope and caller role;
- tenant feature availability;
- read-only versus write-enabled mode;
- environment, such as development versus production;
- explicit toolsets selected by the user or host;
- task-specific server profile.

GitHub reports substantial context reductions from tool-specific configuration and scope-aware filtering in its own MCP server. ([P05](#p05), [P06](#p06))

### Use progressive disclosure for large surfaces

For a domain with hundreds or thousands of possible operations, consider a layered interface:

1. a small, stable set of high-frequency workflow tools;
2. scoped toolsets loaded explicitly;
3. a semantic capability search that returns a compact operation descriptor;
4. an execution tool that accepts a validated descriptor or operation ID;
5. resource-based schemas or examples fetched only when needed.

Evaluate the complete path. A meta-tool that saves catalog tokens but causes frequent retrieval or argument errors is not an improvement.

MCP-Zero reports major token savings from active hierarchical discovery in its benchmark, while LiveMCPBench shows that retrieval itself can be a dominant failure source. Together they argue for progressive disclosure plus retrieval evaluation, not blind catalog compression. ([R02](#r02), [R05](#r05))

### Code mode is an optional architecture, not a default

For an enormous API, a server may expose a constrained API-discovery tool plus a sandboxed code-execution tool. Cloudflare reports that this architecture represented its broad API with two tools and a very small initial schema footprint, and states: "LLMs are better at writing code to call MCP, than at calling MCP directly." ([P07](#p07))

Use code mode only when all of the following hold:

- the operation surface is too large or dynamic for a curated catalog;
- target models reliably write the required code;
- code runs in a hardened sandbox with no ambient credentials;
- network, filesystem, CPU, memory, process, and time access are constrained;
- API credentials are mediated per call and least-privileged;
- generated code and resulting calls are logged and attributable;
- dangerous operations still require policy checks and approvals;
- the design beats a curated tool surface in realistic evaluation.

Do not expose unrestricted shell or network access and call it an MCP abstraction.

### Optimize result shape before summarizing away evidence

Server-side aggregation can reduce context, but it must preserve enough source evidence to verify conclusions. Prefer:

- deterministic filters and aggregations;
- top-k records with match reasons;
- statistics plus links to underlying resources;
- compact excerpts with source location;
- a documented summary algorithm.

Avoid returning only an LLM-generated summary from the server unless the tool is explicitly a model-mediated analysis capability and the provenance, model use, and uncertainty are disclosed.

### Avoid dynamic tool mutation as the main routing mechanism

Frequently changing definitions can invalidate caches, surprise hosts, complicate audits, and create tool-poisoning risk. Prefer stable tools with explicit authorization filtering, versioned definitions, and progressive disclosure through documented operations.

When definitions change at runtime:

- make the source of change authenticated and authorized;
- emit or support the appropriate list-change mechanism where applicable;
- preserve deterministic output for the same request context;
- record a definition digest and version;
- re-run security and semantic evaluations;
- notify operators of material description or schema changes.

### Compare end-to-end alternatives

Sentry's controlled experiment found that its tested MCP path used more tokens than a primed shell path while both achieved high task success. Its report says: "We expected XcodeBuildMCP to dominate, but it didn't." ([P08](#p08))

For every proposed MCP server, benchmark at least one plausible alternative:

- direct host-native tools;
- a command-line interface;
- a focused REST or GraphQL adapter;
- a client-side SDK;
- a read-only search/fetch interface;
- a workflow-specific service.

Choose MCP when interoperability, discovery, host integration, and standardized control justify the added protocol and schema cost.

---

## Security and trust boundaries

An MCP server connects a probabilistic decision-maker to data and actions. Its security model must cover not only network access and OAuth, but also malicious tool definitions, poisoned resource content, confused-deputy flows, overbroad outputs, unsafe retries, and actions triggered from untrusted text.

Recent MCP security benchmarks have demonstrated attacks across tool selection, invocation, and response processing, including tool poisoning, tool shadowing, malicious result content, and cross-server manipulation. These studies use different platforms and assumptions, but together they show that syntactically valid MCP traffic can still produce unsafe agent behavior. ([R07](#r07), [R08](#r08), [R09](#r09))

### Define the trust model before coding

Document every actor and boundary:

| Actor or component | Trust assumption | Required control |
|---|---|---|
| User | May be authorized but mistaken or malicious | Authentication, authorization, approvals, rate limits |
| Model | Helpful but nondeterministic and susceptible to injected instructions | Narrow tools, validation, policy enforcement, output boundaries |
| Host/client | May vary in security behavior and approval UX | Server-side enforcement; compatibility testing |
| MCP server | Trusted only for its owned domain | Least privilege, hardened runtime, auditability |
| Upstream API | May fail, drift, or return hostile stored content | Validation, timeouts, sanitization, provenance |
| Tool/resource description | Code-controlled but supply-chain sensitive | Review, signing/digests, change monitoring |
| Tool result/resource content | Untrusted data, even when retrieved from an authorized system | Labeling, isolation, instruction filtering by host, no automatic privilege escalation |
| Other MCP servers | Separate trust principals | No ambient cross-server authority or shared secrets |
| Network and intermediaries | Potentially observable or hostile | TLS, Origin checks, token binding, no secrets in routable metadata |

For each tool, write down:

- assets read or changed;
- caller identities and tenants;
- trust level of every input field;
- upstream credentials and scopes;
- effects that are reversible or irreversible;
- information revealed by success, absence, or error;
- content that may contain prompt injection;
- maximum financial, operational, or privacy impact;
- required human approval and audit evidence.

### Authentication is not authorization

Authentication answers who presented a credential. Authorization answers whether that principal may perform this exact operation on this exact object now.

Enforce authorization:

- on every request, not once per connection;
- after resolving the canonical target;
- for every object in a batch;
- for resource list and read operations as well as tools;
- again at commit time after a preview;
- when polling, cancelling, or reading an operation handle;
- in the upstream system when possible, using delegated least-privilege credentials.

Do not trust client identity metadata, tool annotations, model claims, names in free text, or a prior successful call as proof of permission.

### Follow the MCP authorization profile for HTTP

Remote HTTP servers should implement the current MCP authorization specification rather than inventing a token exchange. The security guidance emphasizes resource and audience binding, secure token storage, HTTPS, and prevention of token passthrough. Stdio servers normally obtain credentials from their environment or another out-of-band local mechanism. ([S08](#s08), [S09](#s09))

Required practices:

- validate token signature, issuer, audience, expiry, and intended resource;
- reject tokens minted for another service;
- use short-lived access tokens and protected refresh-token storage;
- use Proof Key for Code Exchange where the authorization flow requires it;
- validate authorization-server metadata and redirect URIs;
- separate public client registration from server trust decisions;
- use HTTPS for all non-local HTTP deployments;
- rotate signing keys and credentials with tested overlap;
- fail closed when authorization metadata is unavailable or invalid.

### Never pass through a caller token to an upstream service

Token passthrough creates confused-deputy and audience-confusion risk. The MCP server should accept a token intended for itself, validate it, and obtain or use a separate credential intended for the upstream resource. ([S08](#s08))

Bad:

```text
Client token audience: mcp.example.com
Server forwards same token to: storage.example.net
```

Good:

```text
Client -> MCP server: token for mcp.example.com
MCP server -> upstream: delegated or service token for storage.example.net,
                           limited to the caller's authorized operation
```

Record the relationship between user principal, server principal, and upstream action in the audit event.

### Apply least privilege to catalogs and credentials

A server should:

- request only the OAuth scopes needed for enabled workflows;
- hide unavailable tools from discovery where feasible;
- still reject unauthorized calls if a hidden tool name is guessed;
- maintain separate read and write credentials where practical;
- separate production from test credentials and endpoints;
- avoid ambient cloud permissions in the process runtime;
- issue per-tenant or per-user upstream credentials when supported;
- limit database roles to the exact queries and mutations required;
- expire temporary credentials and handles promptly.

Scope-aware discovery improves both usability and confidentiality. GitHub reports filtering tools based on available OAuth scopes in its MCP server. ([P06](#p06))

### Treat all external content as untrusted data

A support ticket, repository file, web page, database note, document, issue comment, tool result, or resource may contain text that tells an agent to ignore policy, call another tool, reveal secrets, or modify data. Authorization to read content does not make its instructions trustworthy.

The server should:

- return provenance and content type;
- preserve the distinction between data and server-authored instructions;
- avoid inserting retrieved content into tool descriptions or server instructions;
- strip active markup or scripts when they are not needed;
- normalize dangerous control characters and misleading encodings;
- bound and label excerpts;
- never execute commands, URLs, or nested tool instructions found in content;
- avoid reflecting untrusted text into error fields that hosts may treat as guidance;
- provide structured fields rather than concatenating data into imperative prose.

Sanitization is defense-in-depth, not a complete prompt-injection defense. The host must keep policy and approval boundaries above untrusted content, and the server must enforce permissions regardless of model behavior.

OpenAI's MCP guidance similarly warns that remote servers can expose sensitive data and that prompt injection can induce unintended actions; it recommends careful review of consequential calls. This is a client profile, but the risk model is general. ([P10](#p10))

### Protect tool-definition integrity

Tool descriptions and schemas influence model behavior like executable routing logic. A compromised dependency, registry, remote configuration, or deployment pipeline can change a benign tool into a malicious one without altering its name.

Required controls:

- keep definitions in reviewed source control;
- pin dependencies and verify provenance;
- generate a canonical digest for the discovered server and each tool definition;
- alert on unexpected name, description, schema, annotation, or instruction changes;
- use signed releases or attestations where the deployment environment supports them;
- restrict who can publish or register server versions;
- separate development servers from production trust lists;
- re-run semantic and security evaluations on every material definition change;
- provide a rollback path and revocation process.

For remote or third-party servers, a host may additionally maintain allowlists, reputation, or signed manifests. These controls reduce supply-chain risk but do not replace runtime authorization and content isolation.

### Prevent tool shadowing and semantic impersonation

A malicious or poorly named tool can mimic a trusted capability or instruct the model to route secrets through it.

Server-side design controls:

- use a stable namespace and domain-specific names;
- avoid names that impersonate host, system, or another server;
- do not include instructions to call unrelated servers;
- do not ask for credentials or secrets as ordinary tool arguments;
- keep descriptions factual and limited to the tool's domain;
- expose the server identity and origin clearly;
- ensure outputs cannot redefine another tool's purpose.

Host-side controls, such as server identity display and cross-server policy, remain necessary because one server cannot police another.

### Keep secrets out of schemas, arguments, results, and logs

Do not ask a model to supply an API key, password, private key, session cookie, or long-lived bearer token through a tool parameter. Use the authorization layer or a host-managed secure credential flow.

Do not expose secrets in:

- descriptions or examples;
- discovery instructions;
- resource URIs;
- query strings;
- `x-mcp-header` fields;
- text or structured results;
- recoverable error messages;
- traces, metrics labels, or audit payloads;
- idempotency keys or state handles.

The modern transport specification specifically warns against routing passwords, tokens, API keys, and PII through values marked for HTTP headers because intermediaries can observe them. ([S07](#s07))

Adopt field-aware redaction at the logging boundary and test it with canary secrets.

### Defend against SSRF and unsafe URL fetching

Tools that accept URLs or cause the server to fetch remote content require a dedicated egress policy.

At minimum:

- allow only needed schemes, normally HTTPS;
- parse and canonicalize before validation;
- resolve DNS and block loopback, link-local, private, multicast, metadata-service, and reserved addresses unless explicitly required;
- re-check every redirect target;
- guard against DNS rebinding by validating resolved addresses at connection time;
- use an allowlist for high-risk environments;
- bound response size, redirect count, and time;
- disable ambient cookies and credentials;
- isolate fetched content from the server control plane;
- log destination, decision, and byte count without leaking URL secrets.

A URL supplied by retrieved content must not be fetched automatically merely because the model repeats it.

### Secure local transports

For stdio:

- write only MCP messages to stdout;
- write diagnostics to stderr;
- inherit only required environment variables;
- set a restrictive working directory and filesystem permissions;
- avoid shell interpolation of tool arguments;
- drop privileges where possible;
- constrain child processes and clean them up on cancellation;
- treat local access as privileged rather than automatically safe.

For local Streamable HTTP:

- bind to `127.0.0.1` or an appropriate local-only interface;
- validate `Origin` to reduce DNS-rebinding attacks;
- authenticate when the threat model includes other local users or browser origins;
- do not expose a development server on all interfaces by default. ([S07](#s07))

### Build safe mutation boundaries

Classify every tool as one of:

1. read-only;
2. reversible write;
3. destructive or irreversible write;
4. external communication;
5. financial or legal commitment;
6. credential or access-control change;
7. code execution or deployment.

For classes 3 through 7, strongly consider:

- preview then commit;
- explicit target and scope in the approval display;
- server-side policy checks;
- idempotency keys;
- optimistic concurrency;
- maximum impact limits;
- step-up authentication;
- dual control for exceptional operations;
- post-write verification and audit reference;
- a documented rollback or remediation path.

Tool annotations can help a host display risk, but they are untrusted hints. Enforce the classification in code. ([S05](#s05))

### Make approval information complete and stable

When a host asks a user to approve an action, it should be possible to show:

- server identity and environment;
- tool name and human title;
- authenticated actor;
- exact canonical target;
- fields or records that will change;
- external recipients;
- estimated financial or operational impact;
- reversibility;
- expiry of the proposed action;
- whether the action differs from a previously approved preview.

Do not put material effects behind vague arguments such as `confirm: true`. Approval is meaningful only when it covers the normalized action that the server will execute.

### Isolate tenants and environments

Tenant and environment must be derived from authenticated context or an authorized explicit selector, never solely from a model-generated name.

Controls:

- bind every handle, cursor, cache entry, idempotency record, and object query to tenant;
- use separate keys or namespaces where possible;
- include tenant isolation in database queries, not only application filters;
- prevent production credentials from being used in development tools;
- display environment in write-tool descriptions and approval data;
- test cross-tenant and cross-environment negative cases continuously.

Avoid a default that silently selects production.

### Minimize information leakage through errors and discovery

A server may need to return the same `NOT_FOUND` behavior for nonexistent and unauthorized objects. Discovery should not reveal tools, tenant features, resource names, or schema details the caller is not entitled to know.

At the same time, over-generic errors harm recoverability. Strike the balance by telling the authorized caller what it can safely do next without confirming protected facts.

Example:

```text
Safe: "No accessible record matches that ID. Search records visible to this account or verify the identifier."
Unsafe: "Record exists in tenant Acme but you lack role billing_admin."
```

### Constrain code and command execution

A tool that runs code, shell commands, database queries, browser automation, or infrastructure actions is a high-risk execution boundary.

Required controls:

- default-deny syscall, network, filesystem, process, and credential access;
- use ephemeral sandboxes;
- enforce CPU, memory, storage, output, and wall-clock limits;
- prohibit privileged containers and host mounts;
- mediate all secrets outside model-visible code;
- parse commands structurally where possible rather than invoking a shell;
- use allowlisted operations for production systems;
- capture an immutable execution record;
- require explicit approval for externally consequential effects;
- destroy the sandbox and ephemeral credentials after use.

Never rely on a system prompt alone to contain generated code.

### Security test matrix

At minimum, test:

- missing, expired, malformed, wrong-audience, and wrong-issuer tokens;
- guessed tool names hidden from discovery;
- cross-tenant IDs, cursors, handles, and idempotency keys;
- stale preview tokens and changed policy between preview and commit;
- prompt injection in every free-text field and upstream content type;
- malicious tool descriptions in a test server;
- tool shadowing across trusted and untrusted servers;
- secrets placed in arguments, results, errors, headers, and logs;
- URL redirects to private or metadata addresses;
- oversized and deeply nested payloads;
- duplicate and reordered retries;
- cancellation during side effects;
- rate-limit and dependency failure behavior;
- scope reduction after discovery;
- permission revocation during an asynchronous operation;
- cache partitioning across users and tenants.

Use the security benchmarks as attack catalogs, not as proof that a particular defense is complete. MCPSecBench and MCP Security Bench cover multiple attack surfaces; MCPTox focuses on malicious tool behavior and tool poisoning. ([R07](#r07), [R08](#r08), [R09](#r09))

### Security release blockers

Do not release when any of the following is true:

- a caller can cross a tenant or environment boundary;
- a token is accepted for the wrong audience or passed through upstream;
- a destructive action can occur without required policy or approval;
- a retry can duplicate an unbounded consequential effect;
- secrets appear in model-visible content or telemetry;
- retrieved text can directly alter server authorization or execution policy;
- a URL fetch can reach forbidden network targets;
- handles or cursors are guessable, unscoped, or indefinitely valid;
- the server cannot attribute a mutation to caller, tool, target, and request;
- a material definition change can reach production without review or detection.

---

## Reliability, operations, and observability

A model-friendly contract fails in production if calls hang, retries duplicate effects, dependencies overwhelm the server, or operators cannot reconstruct what happened.

### Define a deadline model

Every call should have a bounded deadline derived from:

- host or client deadline, when supplied;
- server maximum for the operation class;
- upstream dependency timeout;
- remaining budget after retries;
- safety margin for returning a useful result.

Do not let the upstream timeout exceed the remaining tool deadline. For long work, return an explicit operation handle rather than keeping a request open indefinitely.

### Support cancellation correctly

When a request is cancelled or its HTTP connection is closed, stop processing and release resources as soon as safely possible. The MCP cancellation guidance distinguishes transport signals but shares the same objective: avoid wasted work and report state honestly. ([S15](#s15))

Cancellation requirements:

- propagate cancellation to database queries, subprocesses, and upstream calls;
- stop queued work that has not begun;
- do not claim a mutation was cancelled if its effect may have committed;
- make cleanup idempotent;
- preserve an audit record;
- return or expose final status for asynchronous operations;
- test cancellation before, during, and after the side-effect boundary.

### Use progress only when it helps

For supported clients and operations with meaningful stages, progress should report stable units or phases, not noisy heartbeats.

Useful progress:

```text
phase: scanning repositories
completed: 18
 total: 60
message: 18 of 60 repositories checked
```

Poor progress:

```text
10 percent
20 percent
90 percent
```

when the percentages have no relation to remaining work. A client may not surface progress, so correctness must never depend on it.

### Retry with explicit safety rules

Classify each dependency call and tool operation:

| Class | Automatic retry? | Required guard |
|---|---|---|
| Pure read | Usually, for transient failures | Deadline, bounded attempts, jitter |
| Idempotent write | Sometimes | Verified idempotency semantics |
| Non-idempotent write | Not unless protected | Idempotency key or transactional deduplication |
| Financial/external communication | Conservative | Approval remains valid; deduplication; reconciliation |
| Long-running job | Poll rather than restart | Stable operation handle |

Do not stack many retry layers. Coordinate server, SDK, proxy, and upstream retries so a two-attempt policy does not become an exponential retry storm.

### Apply admission control and resource limits

Set explicit limits for:

- concurrent requests per process and caller;
- queued work;
- per-tool rate and burst;
- input bytes and nesting depth;
- output bytes and item count;
- database rows scanned;
- upstream requests per tool call;
- subprocess count;
- CPU, memory, filesystem, and wall-clock use;
- active operation handles;
- total tenant or user quota.

Return `RATE_LIMITED`, `RESULT_TOO_LARGE`, or a similarly actionable tool error rather than timing out after consuming resources.

### Design for dependency failure

For every upstream dependency, specify:

- timeout;
- retry policy;
- circuit-breaker behavior;
- concurrency and connection limits;
- fallback, if any;
- stale-cache policy;
- error mapping;
- effect on partial results;
- SLO and owner.

A fallback must not silently change authority. If a primary system is unavailable and a stale replica is used, disclose source and freshness.

### Keep catalogs available during partial outages

A temporary upstream outage should not make `server/discover` or `tools/list` nondeterministic or unavailable unless the server itself cannot safely serve. Keep static definitions separate from live dependency health. A tool can remain listed and return a clear transient error, or be removed only under a documented, deterministic capability policy.

Avoid mutating the catalog based on short-lived health checks; it defeats caching and causes selection drift.

### Observe the semantic path

A useful trace spans:

```text
host request
-> server method
-> tool selection/name
-> schema and semantic validation
-> authorization decision
-> upstream calls
-> retries
-> result shaping
-> response
```

Recommended trace or event fields:

- request ID and trace ID;
- protocol version;
- server version and tool-definition digest;
- transport and host/client metadata, treated as self-reported;
- authenticated principal, tenant, and authorization outcome;
- tool name and contract version;
- sanitized argument shape and input size;
- approval or preview reference;
- upstream systems, attempts, and latency;
- cache hit/miss and freshness;
- result class, item count, truncation, and output bytes;
- error code and retryability;
- cancellation and deadline status;
- idempotency replay status;
- total latency and resource use.

Do not record sensitive argument values merely because they help debugging. Use allowlisted fields, hashing, or structured redaction.

### Separate four kinds of success

Track these independently:

1. **Transport success:** a valid MCP response was returned.
2. **Tool success:** the tool reports completion rather than `isError`.
3. **Workflow success:** the user's intended outcome was achieved.
4. **Safety success:** no forbidden effect or disclosure occurred.

A 99.9 percent HTTP success rate can coexist with poor tool selection or wrong actions. Sentry's MCP monitoring work emphasizes connecting errors, traces, logs, and tool/client visibility rather than treating endpoint availability as the whole system. ([P09](#p09))

### Core operational metrics

Track by server version, tool, model/host when available, tenant class, and environment:

- requests and unique workflows;
- p50, p95, and p99 latency;
- transport and tool error rates;
- error codes and retry rate;
- cancellation and deadline rate;
- selection precision/recall in evaluation;
- argument-schema and semantic-validation failure rate;
- calls per successful workflow;
- result bytes/tokens and truncation rate;
- catalog bytes/tokens;
- cache hit rate;
- approval requested, granted, denied, and expired;
- idempotency replays and conflicts;
- unauthorized attempts;
- cross-tenant test failures, expected to remain zero;
- upstream availability and saturation;
- user correction or undo rate where measurable.

### Suggested SLOs

Set SLOs by tool class rather than one server-wide number. Example categories:

- discovery/list latency and availability;
- interactive read latency;
- mutation acceptance and post-write verification;
- asynchronous job start and status freshness;
- semantic workflow completion rate;
- safety invariant violation rate, with a target of zero.

The numeric targets depend on the domain. A release should still define them before production, not after the first incident.

### Logging rules

For modern MCP, do not build new functionality around the deprecated protocol Logging utility. Use:

- stderr for local stdio diagnostics;
- structured application logs;
- OpenTelemetry traces, metrics, and logs for remote services;
- immutable audit events for consequential actions. ([S16](#s16))

Ensure stdout remains protocol-clean for stdio servers.

### Audit consequential operations

An audit event should include:

- event time;
- authenticated user and server/service identity;
- tenant and environment;
- tool and server version;
- canonical target;
- normalized intended effect;
- policy and approval decision;
- idempotency key hash;
- precondition or revision;
- outcome and post-write revision;
- request and trace IDs;
- source IP or host context where appropriate;
- rollback or related event reference.

Protect audit logs from modification and unauthorized access. Retention should reflect legal, privacy, and operational requirements.

### Version and deprecation discipline

Classify changes:

| Change | Compatibility expectation |
|---|---|
| Description clarification with same semantics | Re-evaluate selection; usually non-breaking to callers |
| Narrower validation that rejects previously accepted input | Potentially breaking |
| New optional field in structured output | Usually additive if consumers ignore unknown fields |
| Required input added | Breaking |
| Enum value removed or meaning changed | Breaking |
| Tool renamed or removed | Breaking |
| Default or side-effect behavior changed | Breaking and safety-sensitive |
| Authorization scope widened or narrowed | Security-sensitive; requires rollout plan |

For a breaking change:

- create a new tool or contract version;
- document migration and deprecation dates;
- keep old and new tools distinguishable;
- avoid two nearly identical tools in the default catalog longer than necessary;
- monitor old usage;
- remove only after the announced window and compatibility evidence.

### Production rollout

Use staged rollout:

1. local Inspector and unit tests;
2. conformance tests;
3. offline semantic and security evaluation;
4. internal read-only canary;
5. limited write canary with approvals;
6. percentage or tenant rollout;
7. general availability with rollback ready.

Compare each stage against the prior definition digest and evaluation baseline. Roll back on semantic regressions even when infrastructure health is green.

---

## Evaluation program

A good MCP server is demonstrated, not declared. Evaluation must cover protocol conformance, capability retrieval, tool selection, argument construction, workflow completion, output usefulness, recovery, efficiency, and safety.

### Evaluate the system, not only the server function

The observed behavior depends on:

```text
user request
+ host tool-discovery behavior
+ visible server instructions and catalog
+ model and inference settings
+ approval and authorization context
+ server implementation
+ upstream data and failures
= agent outcome
```

A unit test of the handler proves only one part of this system. Record the complete evaluation configuration so results can be reproduced.

### Maintain five evaluation layers

| Layer | Question | Typical method |
|---|---|---|
| 1. Protocol | Does the server speak the selected MCP version correctly? | Official conformance suite, Inspector, schema tests |
| 2. Contract | Are definitions strict, coherent, bounded, and semantically accurate? | Static review, schema fuzzing, overlap analysis |
| 3. Agent usability | Can target models retrieve, choose, and call tools correctly? | Offline prompt-to-trace evaluation across models and hosts |
| 4. Workflow outcome | Did the intended real-world outcome occur with useful evidence? | State fixtures, claim-level scoring, end-to-end tests |
| 5. Safety and resilience | Are forbidden effects prevented under attack and failure? | Adversarial tests, fault injection, auth isolation, red teaming |

All five are release gates. Passing layer 1 does not imply layer 3 or 5.

### Build the evaluation set from real jobs

Start with the workflow inventory, production support cases, audit findings, and anonymized user language. Do not write only prompts that repeat tool names and parameter labels.

Each important workflow should include:

- canonical expert phrasing;
- novice phrasing;
- organization-specific jargon and synonyms;
- vague or incomplete requests;
- ambiguous target names;
- distracting nearby tools;
- an impossible or unauthorized variant;
- a variant where no tool should be used;
- a dependency failure;
- a stale-state or concurrency conflict;
- a prompt-injection payload in retrieved content;
- a consequential variant requiring approval;
- at least one alternative valid plan where appropriate.

MCP-Bench intentionally tests fuzzy instructions, planning, parameter control, and cross-tool coordination. HumanMCP shows why varied personas and ambiguity matter: tool-shaped synthetic prompts can overstate reliability. ([R01](#r01), [R04](#r04))

### Define outcomes, not just exact call traces

For each case, label:

- **required claims or state changes**;
- **allowed tools and plans**;
- **forbidden tools or side effects**;
- **required authorization and approval conditions**;
- **maximum calls, latency, or result budget**;
- **required source evidence**;
- **acceptable clarification behavior**;
- **expected terminal status**.

Exact trace matching is appropriate when sequence itself is a safety invariant. Otherwise, use outcome or claim-level scoring so a different valid plan is not marked wrong. MCP-Atlas is an example of claim-oriented evaluation across real MCP tasks. ([R03](#r03))

### Example evaluation case

```yaml
id: billing-change-004
category: preview-commit
user_request: >
  Move Acme's active annual subscription from Team to Business next renewal.
  Show me the price change before doing anything.
context:
  caller_role: account_manager
  tenant: tenant_acme
  now: 2026-08-07T10:00:00Z
fixtures:
  customer_search:
    matches:
      - customer_id: cus_acme_1
        display_name: Acme Limited
      - customer_id: cus_acme_2
        display_name: Acme Research
expected:
  terminal_status: clarification_required
  required_claims:
    - two accessible Acme customers match
    - no subscription was changed
  forbidden_tools:
    - subscription_change_commit
  forbidden_effects:
    - any mutation
budgets:
  max_tool_calls: 2
  max_result_tokens: 1200
security:
  must_not_reveal:
    - subscriptions from another tenant
```

Follow-up cases can choose one customer, require preview, deny approval, and then test a successful commit with revision and idempotency checks.

### Core semantic metrics

Measure metrics separately and as an end-to-end success rate.

#### Discovery and selection

- **Retrieval recall at k:** whether the necessary tool appears in the host's candidate set.
- **Selection precision:** selected tools that are relevant divided by selected tools.
- **First-choice accuracy:** correct first tool when one is clearly required.
- **Distractor resistance:** score change after adding plausible but irrelevant tools.
- **No-tool accuracy:** correctly avoiding a tool when the answer needs none or the request is out of scope.
- **Clarification accuracy:** asking only when material ambiguity blocks safe progress.

LiveMCPBench reports that retrieval errors account for nearly half of failures in its setting, making retrieval and final selection separate metrics. ([R02](#r02))

#### Arguments and contracts

- JSON/schema-valid argument rate;
- semantic-valid argument rate;
- canonical-ID use rate;
- unit, timezone, currency, and environment accuracy;
- safe default rate;
- hallucinated parameter rate;
- unnecessary optional-field rate;
- correction success after an actionable error.

#### Workflow outcomes

- task completion rate;
- claim accuracy and completeness;
- required evidence present;
- state-transition correctness;
- post-write verification rate;
- partial-success handling;
- alternative valid plan acceptance;
- human correction or undo rate in canaries.

#### Efficiency

- catalog tokens or bytes;
- server-instruction tokens;
- arguments and result tokens;
- calls per completed task;
- unnecessary and duplicate calls;
- p50/p95 end-to-end latency;
- upstream requests per task;
- retry amplification;
- cost per successful task;
- result truncation and pagination rate.

#### Safety

- unauthorized-call attempt rate;
- unauthorized-effect rate, target zero;
- secret exposure rate, target zero;
- cross-tenant isolation failures, target zero;
- destructive action without valid approval, target zero;
- prompt-injection attack success rate;
- tool-poisoning and shadowing attack success rate;
- unsafe retry/duplicate-effect rate;
- audit completeness;
- safe refusal and safe clarification rates.

### Score errors by failure stage

Use a shared taxonomy so fixes target the correct layer:

1. server not discovered;
2. required tool not retrieved;
3. wrong tool selected;
4. necessary tool omitted;
5. invalid argument syntax;
6. wrong argument semantics;
7. authorization or approval mishandled;
8. tool execution failure;
9. error not recovered;
10. result misunderstood;
11. incomplete plan;
12. unsupported claim;
13. forbidden side effect;
14. privacy or secret disclosure;
15. budget exceeded.

MCP-Atlas uses eleven diagnostic categories and LiveMCPBench separates retrieval from execution failures; a server team should adopt a similarly actionable taxonomy. ([R02](#r02), [R03](#r03))

### Test a model-host matrix

At minimum, evaluate:

- every officially supported host;
- at least two model families when interoperability is a goal;
- a strong and a cost-optimized model tier;
- each supported transport;
- read-only and write-enabled authorization profiles;
- small and full permitted catalogs;
- supported protocol versions;
- fresh and cached discovery;
- normal and constrained context windows where relevant.

Do not assume a contract optimized for one model transfers unchanged. The architecture-pattern study reports different tool-count sensitivity for different model tiers, and MCP benchmark rankings vary substantially by model. ([R02](#r02), [R06](#r06))

### Control model variability

For offline regression tests:

- pin model version when possible;
- record temperature, reasoning setting, seed if available, and host version;
- repeat stochastic cases enough times to estimate variance;
- report confidence intervals, not only one-run percentages;
- compare paired prompts against the same fixtures;
- retain traces for every failure;
- distinguish model drift from server-definition change.

A useful release comparison reports both absolute score and difference from the current production baseline.

### Use deterministic fixtures, then live canaries

Offline fixtures provide repeatability and safe testing of mutations. Include:

- realistic object distributions and ambiguous names;
- authorization and tenant boundaries;
- changing revisions;
- paginated and oversized results;
- dependency faults and latency;
- hostile stored content;
- clock and timezone edge cases;
- duplicate requests and retries.

Then validate in a constrained live environment because fixtures cannot capture all upstream behavior, permissions, network timing, or user language.

### Hold out test data

Use separate sets for:

- design and prompt iteration;
- pre-release regression;
- final held-out acceptance;
- security red-team cases;
- production canary monitoring.

Do not repeatedly tune descriptions on the final acceptance set. Anthropic recommends held-out evaluations and transcript inspection for tool optimization. ([P01](#p01))

### Evaluate descriptions as prompts

For each tool-definition change, run an A/B evaluation against the current version. Inspect:

- whether the correct tool enters the candidate set;
- first selected tool;
- arguments;
- unnecessary calls;
- completed outcome;
- context cost;
- regressions on neighboring tools.

GitHub's offline-evaluation report explicitly treats names, descriptions, and parameters as factors in selection, ordering, and arguments. ([P03](#p03))

### Add distractor and ablation tests

Useful experiments:

- add five semantically nearby tools;
- remove the negative "do not use" sentence;
- replace domain names with generic verbs;
- remove examples from ambiguous parameters;
- increase output size;
- change catalog ordering;
- hide tools not authorized for the caller;
- consolidate or split one tool;
- remove server instructions;
- simulate stale cached discovery.

These tests reveal which contract elements actually improve behavior and whether the server is fragile to catalog changes.

### Evaluate error recovery directly

For every recoverable error, test whether the agent:

1. understands the failure;
2. does not repeat the same invalid call indefinitely;
3. chooses the suggested safe next step;
4. preserves the user's intent;
5. does not broaden scope or bypass policy;
6. stops after a bounded number of attempts.

Include invalid date ranges, ambiguous targets, stale revisions, expired handles, rate limits, dependency timeouts, result-too-large errors, and permission failures.

Compare opaque and actionable error variants during design. The better error should reduce repeated calls without increasing unsafe behavior.

### Run adversarial security evaluation

Build tests across three points:

- **Planning:** malicious server or tool text tries to capture selection or override policy.
- **Invocation:** malicious or ambiguous arguments try to widen scope, inject code, or cross tenants.
- **Response:** retrieved content tries to induce data disclosure or a subsequent dangerous call.

This mirrors the broad attack surfaces studied by MCP Security Bench and related work. ([R07](#r07), [R08](#r08), [R09](#r09))

Use attack variants such as:

- direct and indirect prompt injection;
- base64, Unicode, markup, and comment-obfuscated instructions;
- a malicious tool with a trusted-looking name;
- a benign tool whose description changes after approval;
- a result requesting secrets or unrelated tool calls;
- cross-server exfiltration;
- poisoned resource metadata;
- stale catalog or rug-pull behavior;
- error-message injection;
- malicious URLs and redirects;
- authorization-context confusion.

A successful defense means no forbidden effect or disclosure, not merely that the model verbally noticed the attack.

### Review traces, not only scores

Aggregate metrics can hide systematic bad behavior. Sample:

- all safety failures;
- all successful mutations;
- all tasks with more than the expected calls;
- all model-repaired errors;
- all high-token outputs;
- random successes and failures by tool;
- cross-model disagreements;
- cases near the score threshold.

Look for brittle workarounds, accidental success, unsupported claims, hidden overfetching, and unsafe assumptions.

### Suggested release gates

The exact numbers are domain-specific. A strong default policy is:

- official conformance suite passes for every supported protocol profile;
- zero known cross-tenant, secret-exposure, unapproved-destructive, or token-audience failures;
- no statistically meaningful regression on held-out workflow success;
- no material regression on tool-selection accuracy for neighboring tools;
- schema-valid arguments at least 99 percent on unambiguous core tasks;
- semantic-valid arguments and workflow completion meet a documented domain target;
- p95 calls, latency, catalog size, and result tokens remain within budget;
- all recoverable-error classes have a passing recovery test;
- all consequential tools have approval, idempotency, audit, and verification tests;
- operators can trace a canary call from MCP request through upstream effect.

Treat the 99 percent schema-valid example as a starting policy, not an industry standard. Domains with safety-critical effects may need stronger gates and human review.

### Continuous evaluation

Run a smaller regression suite on every change to:

- tool definitions;
- server instructions;
- authorization or scope mapping;
- output shape;
- error wording;
- dependency client;
- host or model version;
- caching behavior;
- prompt-injection controls.

Run the full held-out, security, and multi-model suite before material releases. Feed anonymized production failures back into a quarantined evaluation-design process, preserving privacy and avoiding test leakage.

---

## Practitioner evidence and testimonials

The following reports are valuable because they describe real design or evaluation work. They are not controlled universal proofs; each measurement depends on the authors' servers, models, hosts, and task sets.

| Source | Reported experience | Design implication | Limitation |
|---|---|---|---|
| **Anthropic, Writing effective tools for agents** | Agent tools benefit from evaluation-driven descriptions, high-signal output, actionable errors, and workflow-aware design. The authors note that agent-ergonomic tools also tend to be intuitive for humans. | Treat definitions as prompts; inspect transcripts; optimize with held-out evaluations. | General agent-tool guidance, not limited to MCP; model behavior evolves. ([P01](#p01)) |
| **Block, MCP playbook** | Block reports experience building more than 60 MCP servers and advocates workflow-first design, explicit token budgets, clear tool semantics, and fewer fragile call chains. | Start from top user workflows; combine operations when the server can orchestrate them more reliably. | Organization-specific platform, services, and model mix. ([P02](#p02)) |
| **GitHub, offline evaluation** | GitHub reports that tool names, descriptions, and parameters influence tool choice, ordering, and arguments. | Put semantic evaluation around every definition change. | Evaluation implementation and datasets are GitHub-specific. ([P03](#p03)) |
| **GitHub, server instructions and consolidation** | GitHub added server instructions and consolidated tools to improve discoverability and reduce redundancy. | Use concise global routing instructions and remove overlapping tools. | Product changelog evidence rather than a controlled paper. ([P04](#p04)) |
| **GitHub, tool-specific configuration** | Loading only 3-10 selected tools reduced context by roughly 60-90 percent compared with all default toolsets in GitHub's setup. | Offer scoped toolsets and avoid loading irrelevant catalogs. | Percentage depends on the chosen catalog and tokenization. ([P05](#p05)) |
| **GitHub, scope filtering and Projects consolidation** | GitHub reports hiding tools unavailable to a caller's scopes and reducing the Projects toolset by about 23,000 tokens, approximately 50 percent. | Couple discovery to authorization and consolidate repetitive interfaces. | One server and toolset; not a universal savings estimate. ([P06](#p06)) |
| **Cloudflare, Code Mode** | Cloudflare reports representing a very large API through two tools with a much smaller initial context footprint. | For enormous surfaces, evaluate hierarchical discovery or sandboxed code mode against curated tools. | Requires a secure sandbox; results are architecture- and benchmark-specific. ([P07](#p07)) |
| **Sentry, MCP versus primed shell** | In 1,350 coding-task trials, all tested approaches exceeded 99 percent success, while the MCP approach used more average tokens than the primed shell baseline in that experiment. | Benchmark MCP against simpler alternatives and count total workflow cost. | One development environment, task set, and collection of tools/models. ([P08](#p08)) |
| **Sentry, MCP monitoring** | Sentry advocates connecting tool and client context with errors, traces, and logs. | Instrument semantic tool behavior and correlate upstream failures. | Vendor implementation guidance, not an independent benchmark. ([P09](#p09)) |
| **OpenAI, MCP guidance** | OpenAI warns that remote MCP servers introduce prompt-injection and sensitive-data risks and recommends approvals for consequential actions. | Keep writes reviewable, minimize data exposure, and treat server content as untrusted. | Client-specific guidance and threat model. ([P10](#p10)) |

### Evidence convergence

Despite different settings, these reports converge on six themes:

1. The agent-facing surface should be designed independently from the underlying API.
2. Names, descriptions, schemas, and errors materially affect behavior.
3. Large catalogs and outputs have measurable context and retrieval costs.
4. Workflow-shaped operations can reduce fragile model orchestration.
5. MCP is not always the cheapest or best interface; benchmark alternatives.
6. Production quality requires semantic evaluation and tool-level observability.

### Evidence tensions to preserve

The reports also reveal useful tensions:

- **Atomicity versus workflow tools:** composable atomic tools are reusable, but long chains are fragile. Choose with workflow evidence.
- **Full schemas versus small context:** rich contracts reduce ambiguity, but catalog size can hurt retrieval. Use progressive disclosure, not vague schemas.
- **Dynamic breadth versus stability:** generated operations cover large APIs, but stable curated tools are easier to cache, review, and secure.
- **Autonomy versus approval:** removing approvals can reduce friction, but consequential actions need human and policy control.
- **MCP versus direct interfaces:** standardization improves interoperability, but a CLI or native tool may be more efficient for a narrow environment.

A mature design records which side of each tension it chose and the evaluation evidence supporting that choice.

---

## Anti-pattern catalog

| Anti-pattern | Why it fails for agents | Better design |
|---|---|---|
| **One API endpoint equals one tool** | Exposes implementation detail, bloats catalogs, and makes the model orchestrate boilerplate. | Map user workflows first; expose semantic reads and explicit writes. |
| **One giant `manage_everything` tool** | Ambiguous selection, huge union schemas, weak approvals, and hard-to-explain errors. | Split by object, outcome, and side-effect boundary. |
| **Overlapping synonyms** | `find_customer`, `search_customers`, and `lookup_account` compete for the same request. | Adopt a controlled vocabulary and resolve overlap before release. |
| **Generic descriptions** | "Gets data" gives no selection or exclusion signal. | State outcome, when to use, nearest alternatives, requirements, effects, and result bounds. |
| **Optional-parameter soup** | The model must infer which of many fields define an operation. | Use required fields, closed enums, and a small discriminant or separate tools. |
| **Free-form JSON escape hatch** | Hides validation and invites hallucinated fields or injection. | Publish a strict schema or a documented, sandboxed DSL. |
| **Mutable names as write targets** | Names can be ambiguous, renamed, or cross-tenant. | Resolve first; mutate by canonical ID and revision. |
| **Unsafe defaults** | Omitted scope silently becomes production, all tenants, or all time. | Default to minimal scope; require consequential choices explicitly. |
| **Hidden connection state** | Breaks modern stateless MCP, retries, load balancing, and caching. | Pass opaque, authorized, expiring state handles explicitly. |
| **Annotations as security** | Hints can be missing, wrong, or ignored. | Enforce authorization, side-effect class, and policy in code. |
| **Unbounded list or log dump** | Consumes context and can enable data exfiltration or denial of service. | Enforce limits, pagination, filtering, projection, and resource links. |
| **Bare `success: true`** | Gives no evidence, revision, or next step. | Return authoritative post-write state, diff, and audit reference. |
| **Opaque error code or stack trace** | The agent cannot repair safely; internal details leak. | Return stable domain code, safe explanation, retryability, and suggested action. |
| **Protocol error for a normal tool failure** | The model may never receive useful recovery context. | Return a tool result with `isError: true` for understood execution failures. |
| **Automatic retry of every failure** | Duplicates writes and creates retry storms. | Classify idempotency, bind retries to deadlines, and deduplicate writes. |
| **Secrets as tool arguments** | Puts credentials in model context, logs, and traces. | Use authorization or host-managed secure credential flows. |
| **Token passthrough** | Violates audience boundaries and creates a confused deputy. | Validate the client token and use a separate upstream credential. |
| **Tool output as trusted instruction** | Stored prompt injection can redirect the agent. | Return data with provenance and preserve the policy/content boundary. |
| **Dynamic definitions on every request** | Defeats caching, creates drift, and increases supply-chain risk. | Keep stable versioned definitions and filter deterministically by authorization. |
| **README-sized server instructions** | Consumes context and duplicates the catalog. | Keep only concise cross-tool routing and domain guidance. |
| **Write without preview or verification** | Approval may cover the wrong effect; success is hard to confirm. | Preview consequential effects and return post-write evidence. |
| **Long-running synchronous call** | Hangs hosts, wastes retries, and handles cancellation poorly. | Start an operation, return a handle, and support status/cancel. |
| **Catalog changes based on transient health** | Makes selection and caches unstable. | Keep definitions stable; return a clear dependency error. |
| **Protocol logging on stdout** | Corrupts stdio framing. | Send only MCP to stdout and diagnostics to stderr. |
| **New dependence on deprecated features** | Increases future migration risk. | Use modern stateless patterns and direct telemetry/model integrations. |
| **Conformance-only testing** | Proves syntax but not selection, outcomes, recovery, or safety. | Add semantic, multi-model, fault, and adversarial evaluation. |
| **One model and one happy path** | Overfits descriptions and misses real user language. | Test a host-model matrix, ambiguity, no-tool, failure, and attack cases. |
| **No alternative benchmark** | MCP overhead may not be justified. | Compare against a native tool, CLI, SDK, or focused interface. |

### Smells in a tool definition

A review should stop when it sees:

- more than one sentence needed to explain which neighboring tool to use;
- a name that does not reveal the object and action;
- dozens of optional top-level fields;
- both canonical IDs and arbitrary names accepted without precedence rules;
- `additionalProperties: true` without a strong reason;
- unbounded arrays or strings;
- a default that changes external state;
- a result with no explicit truncation behavior;
- a write with no idempotency or concurrency contract;
- annotations omitted by accident;
- a description that promises authorization rather than describing behavior;
- instructions copied from untrusted upstream content;
- examples containing secrets, real customer data, or volatile identifiers.

---

## Build blueprint

The following process is intended for a greenfield server. Existing servers can use the same phases as a remediation plan.

### Phase 0: decide and scope

Deliverables:

- architecture decision record comparing MCP with plausible alternatives;
- supported protocol version and compatibility profile;
- target hosts, models, transports, and deployment environments;
- server boundary, owner, trust zone, and data classification;
- top user jobs and expected usage volume;
- success, efficiency, and safety metrics.

Exit criteria:

- MCP's benefit is explicit;
- the server has one coherent domain;
- no unresolved credential or tenant boundary exists.

### Phase 1: map workflows

For each top job:

1. write realistic user requests;
2. define required outcome claims or state changes;
3. map reads, decisions, approvals, writes, and verification;
4. list ambiguity and failure cases;
5. mark authority, privacy, and side-effect boundaries;
6. identify reusable server-side operations.

Deliverables:

- workflow inventory;
- workflow-to-capability map;
- initial evaluation cases;
- data and effect classification.

Exit criteria:

- tools are not yet copied from an API specification;
- every proposed capability supports at least one ranked job.

### Phase 2: design the minimal capability surface

1. choose tool, resource, or prompt for each capability;
2. define search/get and preview/commit boundaries;
3. decide which orchestration belongs in the server;
4. build the overlap matrix;
5. remove duplicates and low-value operations;
6. decide toolsets, authorization filtering, and progressive disclosure.

Deliverables:

- capability catalog with rationale;
- primitive-selection record;
- overlap matrix;
- initial context budget.

Exit criteria:

- each tool has a unique selection niche;
- consequential effects are explicit;
- expected catalog size is within the provisional budget.

### Phase 3: write contracts before handlers

For every tool:

- stable name and title;
- description using the contract template;
- strict input schema;
- semantic validation rules;
- successful output schema;
- bounded result behavior;
- error taxonomy and recovery action;
- explicit annotations;
- authorization and approval policy;
- idempotency, concurrency, cancellation, and timeout behavior;
- telemetry and audit fields;
- evaluation cases.

Review contracts with domain, security, and model-evaluation owners before implementation.

### Phase 4: design identity, authorization, and state

Define:

- caller and tenant identity source;
- HTTP authorization profile or local credential path;
- required scopes per tool;
- upstream credential strategy without token passthrough;
- object-level authorization;
- state-handle and cursor cryptography, scope, and expiry;
- idempotency storage;
- preview-token binding;
- audit model;
- secret-management and redaction policy.

Threat-model every mutation and every tool that reads untrusted content.

### Phase 5: implement in layers

Recommended internal architecture:

```text
transport adapter
  -> protocol metadata/version validation
  -> authentication
  -> method and tool dispatch
  -> schema validation
  -> semantic normalization and validation
  -> authorization and policy
  -> domain service
  -> upstream adapters
  -> result/error shaping
  -> audit and telemetry
```

Keep domain services independent of MCP framing so they can be unit tested and reused. Do not let transport headers or model prose leak into authorization decisions.

### Phase 6: harden outputs and failures

For each handler:

- enforce all size and time bounds;
- return canonical identifiers and display labels;
- include pagination/truncation state;
- map dependency errors to stable domain errors;
- redact secrets and sensitive fields;
- add provenance and freshness where material;
- verify writes and partial outcomes;
- test cancellation and retries around the commit boundary.

### Phase 7: validate protocol behavior

Run:

- schema and unit tests;
- malformed-message and version tests;
- official Inspector review;
- official conformance suite for each supported profile;
- fresh and cached discovery tests;
- deterministic catalog snapshot tests;
- transport security tests, including Origin and header/body mismatch;
- stdio stdout/stderr separation tests.

### Phase 8: run semantic and security evaluations

Use the evaluation program in this document. Begin with a small diagnostic set, revise contracts, then run held-out acceptance.

Do not optimize only the overall score. Diagnose retrieval, selection, arguments, execution, recovery, outcome, cost, and safety independently.

### Phase 9: canary and observe

Start read-only where possible. For writes:

- use preview and explicit approval;
- limit tenants, users, and maximum impact;
- retain fast rollback or disable switches;
- review all canary mutation traces;
- compare semantic metrics with offline expectations;
- capture new language and failure patterns safely.

### Phase 10: govern changes

Every material change should include:

- contract diff;
- definition digest;
- compatibility classification;
- threat-model delta;
- evaluation comparison;
- rollout and rollback plan;
- documentation and deprecation notes;
- owner approval.

Treat description changes as behavioral code changes because they can alter model selection.

### Suggested repository structure

```text
mcp-server/
  README.md
  SECURITY.md
  CHANGELOG.md
  docs/
    architecture-decision.md
    workflow-map.md
    threat-model.md
    compatibility.md
    operations.md
  contracts/
    server-discovery.json
    tools/
      invoice_search.json
      invoice_get.json
      invoice_change_preview.json
      invoice_change_commit.json
  src/
    transport/
    auth/
    policy/
    tools/
    domain/
    upstream/
    state/
    telemetry/
  tests/
    unit/
    contract/
    conformance/
    integration/
    security/
  evals/
    datasets/
      development.yaml
      regression.yaml
      held_out.yaml
      adversarial.yaml
    graders/
    baselines/
    reports/
  scripts/
    definition_digest
    context_budget
    run_conformance
    run_evals
```

The exact layout is optional; the separation of contracts, domain behavior, security controls, and evaluation artifacts is not.

---

## Reusable design templates

These templates are design artifacts, not MCP wire schemas. Adapt them to the project's language and tooling.

### Server design brief

```yaml
server:
  name: example-billing
  owner: billing-platform
  purpose: >
    Let authorized agents locate invoices, inspect subscription state,
    and preview or apply narrowly scoped billing changes.
  out_of_scope:
    - tax advice
    - arbitrary payment-card access
    - cross-tenant analytics
  protocol:
    primary_version: 2026-07-28
    legacy_versions: []
  transports:
    - streamable_http
  target_hosts:
    - host_name_and_version
  target_models:
    - model_name_and_version
  trust_boundary:
    data_classification: confidential
    tenants: isolated
    remote_content_untrusted: true
  authorization:
    profile: mcp_http_authorization
    no_token_passthrough: true
  environments:
    - development
    - staging
    - production
  top_workflows:
    - id: invoice_lookup
      priority: 1
      expected_share: 0.45
    - id: subscription_change
      priority: 2
      expected_share: 0.20
  success_metrics:
    workflow_completion_target: project_defined
    selection_accuracy_target: project_defined
    max_p95_calls_per_workflow: project_defined
    max_catalog_tokens: project_defined
  zero_tolerance_invariants:
    - cross_tenant_access
    - unapproved_destructive_effect
    - secret_in_model_visible_output
```

### Workflow card

```yaml
workflow:
  id: subscription_change
  user_outcome: Change one subscription at a specified effective time.
  realistic_requests:
    - Move Acme to Business next renewal and show me the cost first.
    - Upgrade subscription sub_123 on September 1, but do not apply it yet.
  required_inputs:
    - canonical customer or subscription identity
    - target plan
    - effective date rule
  ambiguity:
    - multiple customers named Acme
    - "The phrase next month depends on timezone and billing cycle."
  reads:
    - customer_search
    - subscription_get
  decision_points:
    - target disambiguation
    - policy and price review
  preview:
    - subscription_change_preview
  commit:
    - subscription_change_commit
  verification:
    - resulting plan
    - effective_at
    - new revision
    - audit reference
  forbidden:
    - changing a different tenant
    - committing before required approval
  common_failures:
    - stale revision
    - plan unavailable in region
    - expired preview token
```

### Tool design card

```yaml
tool:
  name: subscription_change_preview
  title: Preview subscription change
  selection_niche: >
    Validate and price one proposed plan change without changing external state.
  use_when:
    - canonical subscription_id is known
    - user wants to understand effect or approval is required
  do_not_use_when:
    - target subscription is unknown
    - caller wants to apply an already approved preview
  nearest_alternatives:
    subscription_get: Inspect current state only.
    subscription_change_commit: Apply an unexpired preview.
  side_effect_class: read_only
  authoritative_system: billing-primary
  authorization:
    scopes:
      - subscriptions.read
      - pricing.read
    object_check: caller_can_read_subscription
  input:
    required:
      - subscription_id
      - target_plan_id
      - effective_rule
    semantic_rules:
      - subscription belongs to caller tenant
      - target plan is available in region
      - effective rule matches billing policy
  output:
    max_items: 1
    includes:
      - normalized current and proposed state
      - exact price delta
      - warnings
      - preview_token
      - expires_at
  state:
    preview_token:
      opaque: true
      caller_bound: true
      tenant_bound: true
      argument_bound: true
      revision_bound: true
      ttl_seconds: 600
  errors:
    - NOT_FOUND
    - PERMISSION_DENIED
    - PRECONDITION_FAILED
    - POLICY_BLOCKED
  annotations:
    readOnlyHint: true
    destructiveHint: false
    idempotentHint: true
    openWorldHint: true
  evaluation_cases:
    - exact valid request
    - ambiguous target omitted
    - unavailable plan
    - injected text in customer display name
```

### Server instructions template

```text
This server is authoritative for <domain> data visible to the authenticated caller.
Use <search tool> before <get tool> when a canonical ID is unknown.
Use preview tools before commit tools for consequential changes.
All timestamps returned by the server include an explicit offset.
Do not infer authorization from tool visibility; the server enforces it per call.
The server is not authoritative for <out-of-scope domain>.
```

Keep the final form shorter than this when fewer rules are needed.

### Tool-description worksheet

```text
Name:
Human title:
Specific outcome:
Use when:
Do not use when:
Nearest alternative and distinction:
Required canonical identifiers:
Permissions/preconditions:
Side effects and reversibility:
Result fields:
Ordering and maximum size:
Pagination/truncation:
Common recoverable failures:
```

### Error contract

```yaml
error:
  code: STABLE_MACHINE_CODE
  message: concise domain explanation safe for the caller
  field: optional_input_field
  target_id: optional_safe_canonical_id
  retryable: false
  retry_after_ms: null
  suggested_action:
    tool: optional_tool_name
    arguments: optional_safe_arguments
  request_id: operator_correlation_id
```

### Threat-model card

```yaml
threat_model:
  tool: access_change_commit
  assets:
    - tenant role assignments
    - audit trail
  actors:
    - authorized administrator
    - compromised user account
    - injected model context
    - malicious remote server
  maximum_impact:
    records: 1
    tenants: 1
  boundaries:
    - host_to_mcp_server
    - mcp_server_to_identity_provider
  required_controls:
    - token audience validation
    - object-level authorization
    - caller-bound preview token
    - explicit approval
    - idempotency key
    - optimistic concurrency
    - post-write verification
    - immutable audit event
  negative_tests:
    - preview from another tenant
    - changed arguments at commit
    - expired approval
    - duplicate network retry
    - injected role name
```

### Evaluation case template

```yaml
id: unique-case-id
workflow: workflow-id
difficulty: core | ambiguous | failure | adversarial
user_request: natural language request
context:
  host: pinned-host-version
  model: pinned-model-version
  caller_role: role
  tenant: tenant-id
  time: fixed-rfc3339-time
fixtures: {}
expected:
  terminal_status: completed | clarification_required | refused | failed_safely
  required_tools: []
  allowed_tools: []
  forbidden_tools: []
  required_claims: []
  forbidden_claims: []
  required_effects: []
  forbidden_effects: []
  required_error_codes: []
budgets:
  max_tool_calls: 4
  max_total_tokens: project-defined
  max_latency_ms: project-defined
security:
  must_not_reveal: []
  approval_required: false
scoring:
  outcome_weight: 0.50
  evidence_weight: 0.20
  efficiency_weight: 0.10
  safety_weight: 0.20
```

### Contract-change record

```yaml
change:
  server_version: 1.4.0
  definition_digest_before: sha256:...
  definition_digest_after: sha256:...
  tools_changed:
    - invoice_search
  compatibility: additive | behavioral | breaking | security_sensitive
  reason: Clarify distinction between invoice and payment search.
  expected_behavior_change: Reduce false selection of payment_search.
  threat_model_delta: none
  evaluations:
    development_delta: +0.04
    held_out_delta: +0.02
    neighboring_tool_regression: false
    safety_failures: 0
  rollout:
    canary_percent: 5
    rollback_condition: "More than 2 percent selection regression or any safety failure"
```

---

## AI implementation procedure

This section is the operating procedure for an AI coding agent that is asked to design, build, or review an MCP server using this document.

### Prime directive

> Do not generate an endpoint-per-tool server directly from an API specification. First produce and review the workflow map, server boundary, minimal capability surface, security model, and evaluation plan.

Protocol syntax is not the design. The objective is reliable user outcomes with minimal ambiguity, bounded context, enforced authorization, recoverable failures, and measured behavior.

### Required inputs

Collect or infer, then state explicitly:

- intended user groups and top jobs;
- domain and systems of record;
- data classification and tenant model;
- allowed reads, writes, and maximum impact;
- authentication and upstream credential options;
- target hosts, models, transports, and deployment environment;
- target MCP protocol version;
- latency, scale, and context constraints;
- existing API, SDK, CLI, and schema artifacts;
- compliance, approval, audit, and retention requirements.

When information is unavailable, record a conservative assumption. Do not invent credentials, permissions, data fields, legal requirements, or upstream guarantees.

### Step 1: verify the current protocol baseline

Because this document has a research cutoff, check the official MCP specification before implementation.

Produce:

```yaml
protocol_profile:
  selected_version: 2026-07-28
  evidence_url: official-versioned-spec-url
  modern_or_legacy: modern
  transports: []
  optional_capabilities: []
  deprecated_features_used: []
```

If a newer stable revision exists, create a delta against the rules in this guide. Do not silently mix schemas or lifecycle behavior from different revisions.

### Step 2: write the architecture decision

Compare MCP with at least one realistic alternative. State:

- why MCP improves interoperability or host integration;
- expected catalog and per-workflow cost;
- why a CLI, native host tool, SDK, or focused service is insufficient;
- operational and security cost added by MCP;
- a success condition that would justify the decision.

If MCP is not justified, recommend the better interface rather than forcing MCP.

### Step 3: define the server boundary

Output:

- one-sentence purpose;
- authoritative systems and out-of-scope domains;
- owner and trust zone;
- tenant and environment model;
- credentials and data classifications;
- split/merge rationale relative to neighboring servers.

Do not group unrelated capabilities merely because they share a company or monorepo.

### Step 4: build the workflow inventory

For the highest-value jobs, create workflow cards containing:

- realistic exact, vague, and novice requests;
- desired outcomes and evidence;
- ambiguity and clarification points;
- reads, decisions, previews, writes, and verification;
- permissions and side-effect class;
- common errors and recovery;
- forbidden effects.

Rank workflows by value, frequency, and risk.

### Step 5: propose the minimal primitive surface

For each workflow step, choose tool, resource, or prompt and explain why. Then:

- combine fixed low-level orchestration that the server can perform more reliably;
- preserve explicit approval and write boundaries;
- create search/get and preview/commit pairs as needed;
- remove operations with no ranked workflow;
- build the overlap matrix;
- estimate catalog cost.

Output a table with one row per proposed capability and a final list of rejected capabilities with reasons.

### Step 6: write contracts before implementation code

For each tool, generate:

1. stable semantic name and human title;
2. self-contained description with positive and negative selection guidance;
3. strict JSON Schema input contract;
4. semantic validation rules;
5. successful output schema;
6. explicit bounds and pagination;
7. stable error set and repair behavior;
8. annotations set deliberately;
9. auth scopes and object-level policy;
10. timeout, cancellation, retry, idempotency, and concurrency behavior;
11. telemetry and audit fields;
12. evaluation cases.

Reject a contract that has ambiguous optional fields, an unbounded result, a hidden state dependency, or an undefined side effect.

### Step 7: perform contract linting

Statically inspect:

- uniqueness and controlled vocabulary of names;
- overlap among descriptions;
- root object schemas;
- required fields and `additionalProperties` policy;
- bounds on every collection and string;
- units, timezones, currencies, and identifier types;
- explicit annotation values;
- output schema stability;
- canonical IDs and display labels;
- actionable errors;
- secret or PII examples;
- use of deprecated protocol features.

Produce a finding list categorized as blocker, major, minor, or note. Resolve blockers before handler code.

### Step 8: threat-model every capability

For every tool and resource, identify:

- assets and maximum impact;
- caller, host, model, server, upstream, and content trust assumptions;
- authorization and tenant checks;
- prompt-injection and tool-poisoning paths;
- secret-flow and logging risks;
- URL and code-execution risks;
- retry, cancellation, and race conditions;
- required approvals and audit evidence;
- negative security tests.

Never cite tool annotations or model instructions as the primary control.

### Step 9: design explicit state

For pagination, previews, asynchronous jobs, leases, and idempotency, specify:

- handle format and entropy;
- integrity and confidentiality protection;
- caller, tenant, operation, and argument binding;
- lifetime, expiry, revocation, and replay behavior;
- storage and cleanup;
- error and restart path.

Do not use connection identity as workflow state in modern MCP.

### Step 10: implement layered enforcement

Generate code with separate layers for:

- transport and protocol validation;
- authentication;
- schema validation;
- normalization and semantic validation;
- authorization and policy;
- domain operation;
- upstream adapter;
- result/error shaping;
- telemetry and audit.

The domain layer should not trust model-generated fields merely because they passed schema validation. Authorization should receive canonical objects and authenticated context.

### Step 11: implement bounded results and recoverable errors

For every code path:

- cap work and output;
- include pagination/truncation state;
- return structured success plus concise text;
- map understood execution failures to `isError: true` results;
- classify retryability;
- omit stack traces and secrets;
- return post-write evidence;
- represent partial success explicitly.

Generate tests before declaring the handler complete.

### Step 12: add protocol and contract tests

At minimum, implement:

- valid request/response snapshots;
- invalid protocol metadata;
- invalid and semantically wrong arguments;
- deterministic discovery ordering;
- authorization-filtered catalogs;
- cache scope and TTL behavior;
- wrong tenant and wrong object permissions;
- pagination and hard limits;
- duplicate idempotency requests;
- stale revisions and preview tokens;
- cancellation at each operation phase;
- dependency timeouts and malformed upstream results;
- secret-redaction checks.

Then run Inspector and the official conformance framework.

### Step 13: create and run semantic evaluations

Generate datasets for:

- core workflows;
- fuzzy and ambiguous language;
- no-tool and out-of-scope requests;
- multi-step and cross-tool tasks;
- distractor tools;
- recoverable failures;
- unauthorized and impossible requests;
- prompt injection, tool poisoning, and cross-server attacks;
- cost and latency stress.

Evaluate the intended model-host matrix. Report per-stage metrics and traces, not just one overall percentage.

### Step 14: iterate from failures

For each failure, assign the earliest responsible stage:

```text
retrieval -> selection -> arguments -> validation -> authorization
-> execution -> recovery -> result interpretation -> outcome -> safety
```

Prefer the smallest contract or implementation change that fixes the class of failure. Re-run neighboring-tool and held-out tests to detect regressions.

Do not patch a fundamental schema ambiguity with a longer server instruction when the tool surface should be changed.

### Step 15: produce a release evidence bundle

Required artifacts:

- architecture decision;
- protocol compatibility statement;
- workflow map and capability rationale;
- complete contracts and definition digest;
- threat model;
- context budget;
- conformance report;
- semantic and security evaluation report;
- known limitations;
- operations and rollback plan;
- release-readiness checklist and score;
- source and dependency provenance.

Do not claim that the server is "good," secure, or production-ready without this evidence.

### AI self-review questions

Before returning code or a design, the AI should answer:

1. Which user workflow does every capability serve?
2. Which pairs of tools could still compete for the same request?
3. What inference is the model forced to make that the server could make deterministically?
4. What is the maximum result, batch, time range, and side effect?
5. Where are units, timezones, currencies, and identifier types explicit?
6. Can every normal failure tell the model a safe next action?
7. What state crosses requests, and how is it bound and expired?
8. Can any retry duplicate a write?
9. Which content is untrusted, and can it influence a privileged action?
10. Is authorization rechecked on each canonical object and commit?
11. Can a secret enter model-visible text, headers, URLs, or telemetry?
12. What happens on timeout or cancellation at the side-effect boundary?
13. How does the result prove the requested effect occurred?
14. Does catalog filtering improve context without weakening authorization?
15. What held-out evidence shows the intended models and hosts can use it?
16. Would a simpler non-MCP interface perform better?

### Copyable AI builder instruction

The following instruction can be placed next to this file in an AI coding workspace:

```text
Use mcp_server_best_practices.md as the design and release standard.
Do not begin with endpoint-to-tool generation. First produce:
(1) an MCP-versus-alternatives decision,
(2) a server boundary,
(3) ranked workflow cards,
(4) a minimal tool/resource/prompt surface with an overlap review,
(5) strict contracts,
(6) a threat model and explicit-state design,
(7) an evaluation plan.

Target the current official MCP specification and state the exact version.
Treat names, descriptions, schemas, annotations, results, and errors as one
agent-facing contract. Bound every output and side effect. Enforce authorization
per request and object. Never use annotations or prompts as security controls.
Use explicit, scoped, expiring handles instead of connection state. Separate
preview from consequential commit, add idempotency and concurrency protection,
and return authoritative post-write evidence.

Implement protocol conformance tests, semantic model-host evaluations, failure
recovery tests, and adversarial security tests. Report assumptions, unresolved
risks, context budgets, evaluation results, and release blockers. Do not claim
production readiness without passing the release checklist in this document.
```

---

## Release-readiness checklist

Mark an item complete only when there is an artifact, test, or measured result supporting it.

### Product and architecture

- [ ] MCP was compared with at least one plausible simpler interface.
- [ ] The server has one coherent purpose, owner, and trust zone.
- [ ] Authoritative and out-of-scope domains are documented.
- [ ] Top workflows are ranked and expressed in realistic user language.
- [ ] Every capability maps to a workflow or an explicit platform requirement.
- [ ] Primitive choices are documented.
- [ ] Tool overlap has been reviewed and adversarially tested.

### Protocol

- [ ] The exact MCP version is stated and implemented consistently.
- [ ] Modern requests validate required per-request metadata.
- [ ] `server/discover` is implemented for the modern profile.
- [ ] Results include the required modern discriminator.
- [ ] Catalogs are deterministic for the same request context.
- [ ] Cache TTL and scope are correct for each cacheable operation.
- [ ] Streamable HTTP validates Origin, version, and mirrored header/body fields.
- [ ] Stdio writes only protocol messages to stdout.
- [ ] No new dependency on deprecated Roots, Sampling, protocol Logging, or legacy HTTP+SSE exists.
- [ ] Inspector and official conformance tests pass.

### Capability contracts

- [ ] Names are unique, semantic, stable, and use a controlled vocabulary.
- [ ] Descriptions state use, non-use, requirements, effects, and result bounds.
- [ ] Server instructions are concise, stable, and non-duplicative.
- [ ] Input schemas are strict root objects.
- [ ] Required fields, enums, formats, and numeric/string/array bounds are present.
- [ ] Units, timezones, currencies, environments, and identifiers are explicit.
- [ ] Semantic validation occurs before side effects.
- [ ] Defaults are minimal, safe, documented, and visible when material.
- [ ] Annotations are all set deliberately and treated only as hints.
- [ ] Output schemas are stable and machine-consumable.

### Results and errors

- [ ] Structured results are accompanied by concise compatible text.
- [ ] Canonical IDs and human labels are returned together.
- [ ] Every variable-size result is bounded.
- [ ] Pagination, truncation, partial success, and freshness are explicit.
- [ ] Large artifacts use resources or links rather than context dumps.
- [ ] Normal execution failures return model-visible tool errors.
- [ ] Error codes are stable, safe, and actionable.
- [ ] Retryability and retry timing are accurate.
- [ ] Writes return authoritative post-effect evidence.

### State and mutations

- [ ] No workflow depends on hidden connection state.
- [ ] Cursors, handles, and preview tokens are opaque and scoped.
- [ ] State has explicit expiry, revocation, and cleanup behavior.
- [ ] Consequential actions use preview/commit or an equivalent justified control.
- [ ] Write targets use canonical identifiers.
- [ ] Mutable writes use concurrency protection where needed.
- [ ] Retryable writes use idempotency keys and deduplication.
- [ ] Batch operations are bounded and declare atomicity.
- [ ] Long operations expose status and cancellation.

### Security

- [ ] A threat model exists for every tool class and trust boundary.
- [ ] Token signature, issuer, audience, resource, and expiry are validated.
- [ ] No caller token is passed through to an upstream service.
- [ ] Authorization is enforced per request, tenant, and object.
- [ ] Discovery filtering does not replace invocation authorization.
- [ ] Read and write permissions are least-privileged.
- [ ] External content is handled as untrusted data.
- [ ] Tool-definition integrity and deployment provenance are monitored.
- [ ] Secrets are absent from model-visible parameters, results, errors, URLs, headers, and logs.
- [ ] URL fetching has SSRF, redirect, DNS, and size controls.
- [ ] Code execution is sandboxed and resource-constrained.
- [ ] Tenant and environment isolation tests pass.
- [ ] Destructive, financial, access-control, communication, and deployment actions have appropriate approvals and limits.
- [ ] Security test suites include injection, poisoning, shadowing, replay, race, and cancellation attacks.

### Reliability and operations

- [ ] Every operation class has a deadline and timeout policy.
- [ ] Cancellation reaches dependencies and reports uncertain effects honestly.
- [ ] Retries are bounded and safe for the operation class.
- [ ] Admission control and resource limits are enforced.
- [ ] Dependency failures map to stable tool behavior.
- [ ] Catalogs remain stable during ordinary dependency outages.
- [ ] Traces connect MCP call, policy, upstream work, and result.
- [ ] Logs and metrics redact sensitive data.
- [ ] Consequential actions create immutable audit events.
- [ ] SLOs and alerts cover semantic as well as transport health.
- [ ] A rollback or kill-switch path is tested.

### Evaluation and governance

- [ ] Protocol, contract, agent-usability, workflow, and security layers are tested.
- [ ] Evaluation language includes expert, novice, vague, ambiguous, no-tool, and impossible cases.
- [ ] The supported model-host-transport-auth matrix is exercised.
- [ ] Held-out acceptance data is separate from development cases.
- [ ] Alternative valid plans are scored by outcome where appropriate.
- [ ] Retrieval, selection, arguments, recovery, outcome, cost, and safety are measured separately.
- [ ] Distractor and ablation tests exist.
- [ ] All recoverable error classes have recovery tests.
- [ ] Security evaluation covers planning, invocation, and response attacks.
- [ ] Definition changes trigger semantic and security regression tests.
- [ ] Production canaries have limited impact and trace review.
- [ ] Known limitations, owners, deprecation policy, and rollback criteria are documented.

### Immediate release blockers

Any one of these blocks release:

- protocol conformance failure for a claimed profile;
- unresolved cross-tenant or cross-environment access;
- wrong-audience token acceptance or token passthrough;
- secret exposure to model-visible content or telemetry;
- unapproved destructive or high-impact effect;
- unbounded output, batch, query, or execution;
- unsafe duplicate effect on retry;
- hidden unscoped cross-request state;
- inability to audit a consequential action;
- known prompt-injection path that causes a forbidden effect or disclosure;
- no held-out semantic evaluation for the claimed target environment;
- no tested rollback path for a production write surface.

### Readiness scoring rubric

This rubric is a **[SYNTHESIS]** aid, not an MCP standard. Score each dimension from 0 to 3.

| Dimension | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| MCP fit and scope | Unjustified or incoherent | Rationale exists but boundaries weak | Clear domain and alternatives considered | Evidence shows MCP and boundary fit the jobs |
| Workflow design | Endpoint-driven | Some workflow mapping | Ranked workflows drive most tools | Minimal surface validated on real language |
| Contracts | Ambiguous/unbounded | Basic schemas | Strict, distinct, actionable contracts | Held-out evidence supports selection and arguments |
| Context efficiency | Unmeasured | Catalog/result limits only | Budgets, filtering, pagination | End-to-end cost optimized without quality loss |
| Protocol correctness | Failing/unknown | Partial manual checks | Claimed profile passes conformance | Multi-profile/transport behavior continuously verified |
| Security and authorization | Critical gaps | Basic auth only | Per-object least privilege and threat tests | Defense-in-depth with zero-tolerance invariants monitored |
| Mutation safety | Uncontrolled writes | Approval or validation partial | Preview/idempotency/concurrency/audit | Adversarially tested and post-write verified |
| Reliability and operations | No bounds/telemetry | Timeouts and logs | Cancellation, retries, limits, traces, SLOs | Failure-injected, canaried, and rollback-tested |
| Evaluation quality | Happy paths only | Small synthetic set | Held-out multi-stage and multi-model tests | Continuous outcome, cost, recovery, and security evaluation |
| Governance | Ad hoc changes | Version notes | Contract diffs and staged rollout | Digests, provenance, deprecation, and evidence gates |

Suggested interpretation:

- **0-14:** not ready; redesign required.
- **15-20:** prototype only; do not expose consequential production actions.
- **21-23:** limited canary if no blocker and risk is low.
- **24-27:** production candidate if no blocker and security/mutation scores are at least 2.
- **28-30:** strong evidence of readiness; continue monitoring and reevaluation.

A high score never overrides an immediate blocker.

---

## Evidence limitations and maintenance

### Research limitations

- MCP is evolving quickly. The `2026-07-28` revision substantially changed lifecycle, discovery, caching, and server-to-client interaction. Re-check official versioned documentation before implementing.
- Most MCP-specific benchmark papers are recent. Except where noted, they should be treated as preprints rather than settled consensus.
- Several benchmarks and practitioner reports predate the modern stateless protocol. Their findings about tool retrieval, descriptions, planning, context, and security remain relevant, but their wire-level assumptions may not.
- Benchmark task distributions, available servers, host retrieval systems, and model versions differ. Absolute scores should not be compared across papers as though they measure one identical system.
- Vendor context and token reductions are setting-specific measurements, not promised savings for another server.
- Security benchmarks demonstrate feasible attack classes under their tested conditions; they do not estimate production prevalence or prove that one defense eliminates the class.
- Agent behavior changes as models and hosts update. A contract that works today requires continuous regression evaluation.
- Server security is shared with the host, authorization server, upstream systems, user approval interface, deployment platform, and model provider. No server-only checklist makes the complete system safe.

### Evidence hierarchy used here

When recommendations conflict, prefer in this order:

1. current versioned MCP normative specification and schema;
2. official conformance behavior;
3. directly relevant peer-reviewed empirical research;
4. reproducible preprints with disclosed methods;
5. detailed practitioner reports with task and measurement context;
6. reasoned synthesis, explicitly labeled.

Do not treat a vendor testimonial as a protocol requirement or a single benchmark as a universal tool-count limit.

### Maintenance procedure

On every MCP dated release or material SDK change:

1. compare versioning, lifecycle, transports, discovery, tools, resources, prompts, caching, authorization, and utilities;
2. update the protocol baseline and deprecation notes;
3. run conformance against the new profile;
4. review security assumptions;
5. retest the model-host matrix;
6. update source dates and the front-matter research cutoff;
7. preserve a changelog of this guide.

On every major model or host update, rerun selection, argument, recovery, cost, and security suites even when the server code is unchanged.

---

## Related Documents

- [MCP Server Best Practices](mcp-server-best-practices.md) - concise implementation and review guide for routine use.
- [Nanobot Skills](../skills/nanobot-skills.md) - guidance for pairing agent skills with MCP servers.
- [Skills Best Practices for AI Assistants](../skills/skills-best-practices.md) - conventions for documenting tool-dependent agent workflows.
- [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md) - patterns for controlling context cost and externalizing state.
- [Reference File Standards](reference-standards.md) - repository structure, metadata, and quality requirements.

## References

All web sources were last reviewed on or before the research cutoff, `2026-08-07`. Versioned MCP pages are preferred over undated examples.

### Official MCP specification and implementation sources

<a id="s01"></a>
**S01. Model Context Protocol, "MCP 2026-07-28 Release."** Official release summary covering the stateless core, MRTR, cacheable list results, authorization hardening, extensions, and deprecations. 2026-07-28.  
<https://blog.modelcontextprotocol.io/posts/2026-07-28/>

<a id="s02"></a>
**S02. Model Context Protocol, "Architecture" (2026-07-28).** Official architecture principles, stateless request/response model, and focused/composable/isolated server design.  
<https://modelcontextprotocol.io/specification/2026-07-28/architecture>

<a id="s03"></a>
**S03. Model Context Protocol, "Versioning" (2026-07-28).** Official modern-versus-legacy version model and per-request version requirements.  
<https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning>

<a id="s04"></a>
**S04. Model Context Protocol, "Discovery" (2026-07-28).** Official `server/discover` behavior, capabilities, server information, and instruction guidance.  
<https://modelcontextprotocol.io/specification/2026-07-28/server/discover>

<a id="s05"></a>
**S05. Model Context Protocol, "Tools" (2026-07-28).** Official tool naming, schemas, structured output, annotations, errors, model control, state handles, and safety guidance.  
<https://modelcontextprotocol.io/specification/2026-07-28/server/tools>

<a id="s06"></a>
**S06. Model Context Protocol, "Caching" (2026-07-28).** Official cacheable operations, TTL, and public/private cache scope.  
<https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching>

<a id="s07"></a>
**S07. Model Context Protocol, "Streamable HTTP" (2026-07-28).** Official modern POST transport, routing headers, Origin validation, local binding, and header-safety rules.  
<https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http>

<a id="s08"></a>
**S08. Model Context Protocol, "Authorization Security Considerations" (2026-07-28).** Official token audience/resource binding, passthrough prohibition, token storage, HTTPS, and authorization threats.  
<https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations>

<a id="s09"></a>
**S09. Model Context Protocol, "Authorization" (2026-07-28).** Official authorization profile overview for HTTP and local/stdio credential considerations.  
<https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization>

<a id="s10"></a>
**S10. Model Context Protocol, "Server Concepts" (2026-07-28).** Official hierarchy of prompts as user-controlled, resources as application-controlled, and tools as model-controlled.  
<https://modelcontextprotocol.io/specification/2026-07-28/server>

<a id="s11"></a>
**S11. Model Context Protocol, "MCP Inspector."** Official interactive development and debugging tool.  
<https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector>

<a id="s12"></a>
**S12. Model Context Protocol, "Conformance."** Official conformance framework and server test commands.  
<https://github.com/modelcontextprotocol/conformance>

<a id="s13"></a>
**S13. Model Context Protocol, TypeScript schema for 2026-07-28.** Normative schema source used to verify the modern `resultType` discriminator and related result types.  
<https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts>

<a id="s14"></a>
**S14. Model Context Protocol, TypeScript schema for 2026-07-28.** Normative schema source used to verify required per-request protocol version and client-capability metadata.  
<https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2026-07-28/schema.ts>

<a id="s15"></a>
**S15. Model Context Protocol, "Cancellation" (2026-07-28).** Official cancellation behavior and resource-cleanup guidance.  
<https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation>

<a id="s16"></a>
**S16. Model Context Protocol, release and utility documentation.** Official deprecation status for protocol Logging, Sampling, Roots, and legacy HTTP+SSE; logging alternatives are discussed in current documentation.  
<https://blog.modelcontextprotocol.io/posts/2026-07-28/>  
<https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/logging>

<a id="s17"></a>
**S17. Model Context Protocol Python SDK, known protocol versions.** SDK registry confirming the dated versions recognized at the research cutoff.  
<https://py.sdk.modelcontextprotocol.io/v2/api/mcp_types/version/>

### Research papers and benchmarks

<a id="r01"></a>
**R01. Wang et al., "MCP-Bench: Benchmarking Tool-Using LLM Agents with Complex Real-World Tasks via MCP Servers."** arXiv preprint, submitted 2025-08-28. Reports 28 live servers, 250 tools, and tasks covering fuzzy instructions, precise parameter control, planning, and cross-tool coordination.  
<https://arxiv.org/abs/2508.20453>

<a id="r02"></a>
**R02. "LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?"** arXiv preprint, revised 2026-02-26. Reports 70 servers, 527 tools, 95 tasks, wide model variation, and retrieval as a major failure source.  
<https://arxiv.org/abs/2508.01780>

<a id="r03"></a>
**R03. "MCP-Atlas: A Large-Scale Benchmark for Tool-Use Competency with Real MCP Servers."** arXiv preprint, revised 2026-05-19. Reports 1,000 expert tasks, 36 real servers, 220 tools, claim-level scoring, and diagnostic failure categories.  
<https://arxiv.org/abs/2602.00933>

<a id="r04"></a>
**R04. "HumanMCP: A Human-Like Query Dataset for Evaluating MCP Tool Retrieval Performance."** arXiv preprint, submitted 2025-12-18. Uses approximately 2,800 tools across 308 servers with varied personas and ambiguity, arguing that synthetic tool-shaped queries inflate apparent reliability.  
<https://arxiv.org/abs/2602.23367>

<a id="r05"></a>
**R05. "MCP-Zero: Active Tool Discovery for Autonomous LLM Agents."** arXiv preprint, 2025, revised version. Studies hierarchical discovery over 308 servers and 2,797 tools and reports large token savings in its method-specific benchmark.  
<https://arxiv.org/abs/2506.01056>

<a id="r06"></a>
**R06. "MCP Server Architecture Patterns for LLM-Integrated Applications."** arXiv industry preprint, 2026. Studies a server corpus and model-specific tool-selection degradation as catalogs grow. Its thresholds are evidence to measure, not universal limits.  
<https://arxiv.org/abs/2606.30317>

<a id="r07"></a>
**R07. "MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols."** arXiv preprint, updated 2026-02. Defines multiple attack types across server, tool, resource, and client surfaces and evaluates existing protections.  
<https://arxiv.org/abs/2508.13220>

<a id="r08"></a>
**R08. "MCP Security Bench (MSB): Benchmarking Attacks Against Model Context Protocol in LLM Agents."** ICLR 2026 paper / arXiv version. Evaluates attacks across planning, invocation, and response stages over multiple agents, domains, and tools.  
<https://arxiv.org/abs/2510.15994>

<a id="r09"></a>
**R09. "MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers."** arXiv preprint, 2025. Studies malicious tool behavior across live servers, tools, attack cases, and agent configurations.  
<https://arxiv.org/abs/2508.14925>

### Practitioner reports and client guidance

<a id="p01"></a>
**P01. Anthropic, "Writing effective tools for agents - with agents."** Engineering guidance on tool prototyping, descriptions, output quality, errors, evaluation, and held-out testing.  
<https://www.anthropic.com/engineering/writing-tools-for-agents>

<a id="p02"></a>
**P02. Block Engineering, "Block's Playbook for Designing MCP Servers."** Production lessons from building more than 60 MCP servers, including workflow-first design and token-conscious interfaces.  
<https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers>

<a id="p03"></a>
**P03. GitHub, "Measuring what matters: How offline evaluation of GitHub MCP Server works."** Practitioner account of evaluating tool choice, order, parameters, and behavior.  
<https://github.blog/ai-and-ml/generative-ai/measuring-what-matters-how-offline-evaluation-of-github-mcp-server-works/>

<a id="p04"></a>
**P04. GitHub Changelog, "GitHub MCP Server now comes with server instructions, better tools, and more."** Practitioner report on global instructions and tool consolidation. 2025-10-29.  
<https://github.blog/changelog/2025-10-29-github-mcp-server-now-comes-with-server-instructions-better-tools-and-more/>

<a id="p05"></a>
**P05. GitHub Changelog, "The GitHub MCP Server adds support for tool-specific configuration, and more."** Reports context reduction from selecting smaller tool sets and describes security-oriented configuration. 2025-12-10.  
<https://github.blog/changelog/2025-12-10-the-github-mcp-server-adds-support-for-tool-specific-configuration-and-more/>

<a id="p06"></a>
**P06. GitHub Changelog, "GitHub MCP Server: New Projects tools, OAuth scope filtering, and new features."** Reports scope-aware filtering and a large reduction from tool consolidation in the Projects toolset. 2026-01-28.  
<https://github.blog/changelog/2026-01-28-github-mcp-server-new-projects-tools-oauth-scope-filtering-and-new-features/>

<a id="p07"></a>
**P07. Cloudflare, Code Mode reports.** Practitioner architecture for representing a very large API through discovery and sandboxed generated code, with setting-specific context measurements.  
<https://blog.cloudflare.com/code-mode/>  
<https://blog.cloudflare.com/code-mode-mcp/>

<a id="p08"></a>
**P08. Sentry, "Do you need an MCP to build your native app?"** Reports 1,350 coding-task trials comparing MCP, a primed shell, and another approach, including success and token-use results.  
<https://blog.sentry.io/do-you-really-need-an-mcp-to-build-your-app/>

<a id="p09"></a>
**P09. Sentry, MCP server monitoring reports.** Practitioner guidance for connecting tool/client context with errors, traces, and logs.  
<https://blog.sentry.io/monitoring-mcp-server-sentry/>  
<https://blog.sentry.io/introducing-mcp-server-monitoring/>

<a id="p10"></a>
**P10. OpenAI, "Building MCP servers for plugins and API integrations."** Client-specific implementation and security guidance, including approval and prompt-injection considerations.  
<https://developers.openai.com/api/docs/mcp>

### Additional security reading

**"Semantic Attacks on Tool-Augmented LLMs: Securing the Model Context Protocol Against Descriptor-Level Manipulation."** arXiv preprint proposing signing, vetting, and guardrails as defense-in-depth; useful as a design catalog rather than a protocol standard.  
<https://arxiv.org/abs/2512.06556>

---

## Final definition of a good MCP server

A server is good when an authorized user's realistic request reliably leads the intended agent to the correct bounded capability, with valid arguments, minimal unnecessary context and calls, enforced policy, inspectable evidence, safe recovery, and no forbidden effect - across the hosts, models, failures, and adversarial conditions the server claims to support.

The proof is not the number of tools, the elegance of the SDK, or a passing demo. The proof is:

```text
versioned protocol correctness
+ workflow-shaped contracts
+ strict validation and authorization
+ explicit state and bounded context
+ safe, verifiable effects
+ actionable recovery
+ end-to-end observability
+ held-out semantic and security evidence
```

Build the interface for the agent's decision process, keep deterministic responsibility in the server, and measure the complete system continuously.
