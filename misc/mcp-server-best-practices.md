---
title: MCP Server Best Practices
description: Practical rules and release checks for designing reliable, efficient, secure, and agent-usable Model Context Protocol servers.
status: active
tags: [mcp, servers, tools, security, evaluation, reliability]
last_verified: 2026-08-07
layer: warm
applies_to: Model Context Protocol servers and agent-facing tools
---

# MCP Server Best Practices

> Design MCP servers as agent-facing products, not protocol-shaped wrappers around existing APIs.

## Overview

This guide gives architects, tool designers, and AI engineers a compact procedure for designing and reviewing Model Context Protocol (MCP) servers. It targets MCP `2026-07-28` and emphasizes reliable tool selection, bounded context use, server-enforced safety, recoverable failures, and realistic evaluation.

**Audience:** MCP server architects, AI-agent engineers, API designers, and security reviewers.

Use the [deep reference](mcp-server-best-practices-deep-reference.md) when you need protocol details, evidence, implementation templates, threat models, or evaluation methodology.

## Recommendations

### Twelve Core Rules

1. **Design from user workflows.** Start from jobs users need to complete rather than mapping one tool to every API endpoint.
2. **Keep the visible surface small and coherent.** Remove overlapping tools and hide capabilities the caller cannot use.
3. **Treat tool metadata as prompts.** Names, descriptions, schemas, and server instructions directly affect model behavior.
4. **Constrain inputs syntactically and semantically.** Validate units, identifiers, scope, permissions, and cross-field rules on the server.
5. **Return concise text and stable structured output.** Make results understandable to models and reliable for downstream calls.
6. **Bound every variable-size result.** Apply pagination, limits, filters, truncation rules, and artifact links.
7. **Make failures recoverable.** Identify the invalid field, explain the constraint, and state the next safe action.
8. **Separate discovery, reading, preview, and mutation.** Make side effects and approval boundaries obvious.
9. **Enforce least privilege on every call.** Treat annotations as hints, never as authorization controls.
10. **Implement the claimed protocol profile correctly.** Do not mix modern stateless behavior with legacy session assumptions.
11. **Observe semantic behavior.** Measure selection, arguments, outcomes, recovery, latency, cost, and safety.
12. **Release through held-out, multi-model, adversarial evaluation.** Happy-path protocol tests are necessary but insufficient.

### Decide Whether MCP Fits

MCP is a strong fit when several conditions hold:

- Multiple hosts or agent frameworks need the same capabilities.
- Capabilities must be discoverable at runtime.
- Tools, resources, or prompts form a coherent domain boundary.
- Remote access needs standardized, scoped authorization.
- The organization can operate, observe, version, and evaluate the server.

Reconsider MCP when any of these dominate:

- One fixed client needs one trivial operation.
- The design mechanically exposes every endpoint of a large API.
- Useful tasks require long chains of low-level calls.
- Deterministic bulk work is better represented as a job, CLI, or SDK.
- Per-user, per-tenant, per-object authorization cannot be enforced.
- The team cannot maintain semantic regression tests.

Record the decision before implementation. Include the top user jobs, intended hosts, alternatives considered, expected visible tool count, context budget, consequential actions, and operational owner.

## Patterns

### Workflow-First Capability Design

For each high-value user job:

1. Capture realistic requests from novice and expert users.
2. Identify the minimum information needed to complete the job.
3. Map the shortest safe sequence of tools, resources, and prompts.
4. Separate reads, previews, writes, and destructive actions.
5. Remove tools that duplicate another capability without a distinct contract.
6. Test the workflow with distractor tools present.

Prefer semantic operations such as `search_issues` or `preview_deployment` over transport-shaped operations such as `post_v2_query`. Consolidate operations only when they share the same intent, authorization, side effects, and output shape.

### Tool Contracts

A tool contract should make five facts explicit:

- when to use the tool;
- when not to use it;
- what every parameter means and which units apply;
- what side effects, permissions, and approvals are involved;
- what result or recovery action the caller should expect.

Use strict JSON Schema, reject unknown fields where practical, constrain strings and arrays, and validate semantic rules after schema validation. Avoid unsafe implicit defaults for tenant, environment, branch, account, or destructive scope.

**[Conceptual]** A mutation contract separates preview from commit and requires concurrency protection:

```json
{
  "name": "commit_deployment",
  "inputSchema": {
    "type": "object",
    "properties": {
      "preview_id": { "type": "string", "minLength": 1 },
      "expected_revision": { "type": "string", "minLength": 1 },
      "idempotency_key": { "type": "string", "minLength": 16 }
    },
    "required": ["preview_id", "expected_revision", "idempotency_key"],
    "additionalProperties": false
  }
}
```

### Bounded Outputs and Recoverable Errors

Return high-signal fields first. Include stable identifiers, status, provenance, freshness, applied scope, and a concise summary. Use cursor pagination for mutable collections and return large artifacts through resources or bounded links.

A recoverable execution error should include:

- a stable error category;
- the field or object that failed;
- the relevant constraint;
- whether retrying is safe;
- the next valid action;
- uncertainty about side effects, when applicable.

Do not expose stack traces, secrets, internal topology, or upstream credentials. Do not suggest retrying a mutation unless duplicate effects are prevented or explicitly understood.

### Explicit State and Safe Mutation

Pass application state through explicit, opaque handles rather than hidden cross-request server state. Scope handles to the caller and tenant, set an expiry, prevent tampering, and document whether a handle is single-use.

For mutations:

- provide preview before commit when impact is consequential;
- require idempotency keys for safely retryable writes;
- use optimistic concurrency for mutable objects;
- verify the resulting state after the write;
- record an immutable audit event;
- report partial or uncertain completion honestly.

### Context Efficiency

Set budgets for both tool catalogs and tool results. Keep catalogs deterministic and cacheable. Filter visible capabilities by authorization and relevance without relying on filtering as the authorization control.

Use progressive disclosure for large surfaces:

1. expose a compact discovery layer;
2. return summaries and stable identifiers;
3. fetch details only when needed;
4. place large payloads in resources or artifacts;
5. measure total tokens and calls for complete workflows.

Do not optimize only the schema size. A smaller catalog that forces extra calls or hides necessary distinctions may cost more end to end.

### Security Boundaries

Define trust boundaries before coding. Treat tool descriptions, external content, resource text, upstream errors, and generated artifacts as untrusted data.

Enforce these invariants on the server:

- authenticate the caller and authorize every action and object;
- bind credentials and handles to the correct user, tenant, audience, and environment;
- never pass caller tokens through to unrelated upstream services;
- keep secrets out of model-visible fields, URLs, errors, and telemetry;
- validate outbound URLs against server-side request forgery and redirect attacks;
- isolate code execution and apply time, memory, filesystem, and network limits;
- require approvals and policy checks for destructive, financial, access-control, communication, and deployment actions;
- log consequential actions without logging sensitive payloads.

Tool annotations can describe risk but cannot enforce policy.

## Anti-Patterns

Avoid these designs:

- one generated tool per API endpoint;
- many near-duplicate tools distinguished only by descriptions;
- generic tools such as `execute` or `run_action` with broad free-form inputs;
- hidden tenant, environment, or branch defaults;
- unbounded search, query, batch, file, or command results;
- raw upstream errors or stack traces returned to the model;
- mutable server-side state keyed only by a transport session;
- catalogs that disappear when a dependency is temporarily unavailable;
- retries of non-idempotent writes without duplicate-effect protection;
- authorization based on model instructions, client identity text, or annotations;
- evaluations that provide exact tool names and only test successful calls.

## Validation

Test five layers independently:

1. **Protocol:** claimed versions, transports, discovery, schemas, result types, caching, and cancellation.
2. **Contract:** schema validity, semantic validation, bounded output, stable errors, and authorization.
3. **Agent usability:** retrieval, tool selection, arguments, ordering, stopping, and recovery.
4. **Workflow outcome:** end state, side effects, latency, calls, and token cost.
5. **Security:** injection, tool poisoning, name collision, authorization bypass, replay, race, and data leakage.

Build evaluation cases from realistic requests. Include expert, novice, vague, ambiguous, no-tool, impossible, and adversarial cases. Keep acceptance cases held out from contract tuning and test every supported model-host-transport-auth combination.

**[Copy-Safe]** Run the official inspector and conformance suite using the commands supported by the server's SDK and protocol profile. Record the exact command, version, expected result, and date in the release evidence bundle. See the [deep reference protocol validation section](mcp-server-best-practices-deep-reference.md#protocol-baseline-mcp-2026-07-28) for current examples and constraints.

Release only when:

- retrieval and argument accuracy meet the documented target;
- workflows complete within call, latency, and context budgets;
- recoverable errors lead to successful repair;
- consequential actions are authorized, previewable where appropriate, idempotent or explicitly non-retryable, and auditable;
- security invariants hold under adversarial tests;
- rollback and kill-switch paths have been exercised.

Block release for any protocol conformance failure in a claimed profile, cross-tenant access, token audience confusion, secret exposure, unapproved high-impact action, unbounded execution or output, unsafe duplicate effects, hidden unscoped state, unauditable consequential action, known injection path to forbidden effects, missing held-out evaluation, or untested rollback.

## Related Documents

- [MCP Server Best Practices Deep Reference](mcp-server-best-practices-deep-reference.md) - full evidence base, protocol details, templates, threat model, and evaluation program.
- [Nanobot Skills](../skills/nanobot-skills.md) - guidance for pairing skills with MCP servers.
- [Skills Best Practices for AI Assistants](../skills/skills-best-practices.md) - design rules for tool-dependent skills.
- [LLM Budget-Friendly Design Patterns](llm-budget-friendly-design-patterns.md) - context, state, and interface patterns for efficient AI systems.
- [Reference File Standards](reference-standards.md) - repository documentation conventions.