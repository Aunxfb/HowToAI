---
title: "AI vs DAST Comparison: Vulnerability Deep Dives"
description: "Per-vulnerability-type descriptions for all 30 AI-delegated and DAST-delegated categories, with examples, reasoning, and validation steps."
status: active
tags: [security, penetration-testing, dast, ai-testing, vulnerability-assessment, web-security, deep-dive]
last_verified: 2026-07-29
layer: cold
applies_to: "web application security testing, penetration testing workflow"
---

# AI vs DAST Comparison: Vulnerability Deep Dives

## Overview

This file provides the full per-vulnerability-type descriptions for both AI-delegated and DAST-delegated categories referenced in the main decision framework. Each vulnerability type includes examples, an explanation of why the assigned tool is best suited, and the validation steps required to confirm the finding. Use this file when you need detailed technical grounding for a specific vulnerability class.

## Background

The main decision framework assigns each vulnerability type a default delegation (AI, DAST, or human). This file contains the detailed rationale for each of the 15 AI-delegated types and 15 DAST-delegated types. For the decision matrix, workflow, and counter-evidence, see the main document.

---

## 1. Vulnerability Types Best Delegated to AI

AI is most useful where the problem is **semantic** rather than purely technical. These findings often involve valid application behavior used in an unintended way.

## 1. Business Logic Flaws

### Examples

- Refund before payment settlement
- Cancel after shipment
- Reuse coupon after cancellation
- Approve your own request
- Skip onboarding, KYC, or approval steps

### Why AI Helps

Traditional scanners do not understand the expected business process. They can mutate requests, but they usually cannot infer that a workflow action is invalid in a given business state.

AI can review:

- user stories
- API traces
- OpenAPI specifications
- workflow diagrams
- role descriptions
- application documentation

Then generate abuse cases such as:

```text
Can payment be skipped?
Can approval be self-issued?
Can a cancelled object still be acted on?
Can a one-time benefit be reused?
```

### Validation Needed

AI-generated business logic issues are hypotheses until manually proven with controlled requests.

---

## 2. Broken Object Level Authorization / IDOR

### Examples

- User A accesses User B's invoice
- Tenant A accesses Tenant B's workspace
- Changing `userId`, `accountId`, `invoiceId`, or `projectId` exposes another user's data

### Why AI Helps

BOLA/IDOR requires understanding **ownership**. A scanner can change IDs, but it often cannot determine whether the returned object belongs to another user or tenant.

AI can build an object ownership model:

```text
resource -> owner -> tenant -> allowed roles -> test accounts
```

### Validation Needed

Use at least two accounts with different ownership contexts and confirm the returned object belongs to the wrong user or tenant.

---

## 3. Broken Function Level Authorization / RBAC Gaps

### Examples

- Auditor can edit records
- Regular user can call admin endpoint
- Manager can delete objects outside their department
- Support role can export sensitive data

### Why AI Helps

This requires comparing expected permissions against observed behavior. AI can infer likely permission boundaries from endpoint names, role descriptions, and documentation.

### Useful AI Output

```text
endpoint x HTTP method x role x expected access x test result
```

### Validation Needed

Test each role using real credentials or controlled authorization tokens.

---

## 4. Cross-Tenant Isolation Failures

### Examples

- `tenantId` accepted from client input
- Workspace ID can be swapped
- Organization-scoped resources exposed across customers

### Why AI Helps

AI is good at identifying tenant-boundary parameters such as:

```text
tenantId
orgId
workspaceId
companyId
accountId
projectId
```

A scanner may treat these as ordinary parameters.

### Validation Needed

Confirm cross-tenant access with separate tenant-owned accounts.

---

## 5. State-Machine and Workflow Bypass

### Examples

- Ship unpaid order
- Withdraw before approval
- Submit rejected request again
- Modify beneficiary after verification
- Call final API step without completing earlier steps

### Why AI Helps

The vulnerability is not in one request. It is in the sequence.

AI can infer state transitions:

```text
created -> pending -> approved -> paid -> shipped -> closed
```

Then suggest illegal transitions to test.

### Validation Needed

Replay requests out of order and confirm whether the backend enforces state.

---

## 6. Function-Use Limit Abuse

### Examples

- OTP resend unlimited
- Referral reward farming
- Trial reset abuse
- Coupon reuse
- Download quota bypass

### Why AI Helps

The key question is not whether the endpoint works. The question is whether it works **too many times** or under the wrong conditions.

AI can identify features that should be one-time, rate-limited, quota-limited, or state-limited.

### Validation Needed

Confirm the repeated action produces real benefit, bypass, or security impact.

---

## 7. API Documentation vs Implementation Inconsistency

### Examples

- OpenAPI says endpoint requires admin but regular user can call it
- Deprecated endpoint lacks authorization
- API documentation requires tenant scoping but backend ignores it
- Request schema suggests a field is server-controlled but client can modify it

### Why AI Helps

AI can compare:

- OpenAPI / Swagger definitions
- actual traffic
- role descriptions
- route names
- controller logic
- documentation

Traditional DAST usually sees behavior but not documented intent.

### Validation Needed

Demonstrate a documented security expectation being violated at runtime.

---

## 8. GraphQL Authorization Issues

### Examples

- Global object IDs expose unauthorized records
- Nested resolver leaks cross-tenant data
- Mutation accepts foreign object ID
- Query allows overbroad object traversal

### Why AI Helps

GraphQL authorization issues often involve relationships between objects, resolvers, and nested fields. AI can reason over the schema and identify sensitive object paths.

### Validation Needed

Use controlled users and compare accessible object graphs.

---

## 9. Account Recovery, Invite, and Password Reset Logic Flaws

### Examples

- Reset token not bound to user
- Invite token reusable
- Email change does not require re-authentication
- MFA reset weaker than login
- Recovery flow bypasses stronger authentication

### Why AI Helps

These flows involve identity proofing and multi-step trust transitions. Scanners often struggle because the flows require email, tokens, timing, and multiple accounts.

### Validation Needed

Safely test token binding, expiry, reuse, account switching, and privilege changes.

---

## 10. Privilege Escalation Through Chained Weaknesses

### Examples

```text
User can invite members
Invited member can select role
Role update endpoint lacks approval
Result: admin creation
```

### Why AI Helps

AI is useful at connecting weak signals that are not critical alone but become serious together.

### Validation Needed

Prove the full chain end-to-end or document the missing step clearly.

---

## 11. Semantic Sensitive Information Exposure

### Examples

- Internal hostnames in JavaScript
- Admin email patterns
- Staging URLs
- Feature flags
- Source maps exposing route structure
- Internal bucket names

### Why AI Helps

Secret scanners are strong for tokens and keys. AI is better for contextually sensitive information that is not a classic secret.

### Validation Needed

Classify whether the exposed information enables attack, reconnaissance, phishing, or access expansion.

---

## 12. Asynchronous and Background Job Abuse

### Examples

- Report generator renders attacker-controlled HTML
- PDF generator fetches internal URLs
- CSV import triggers delayed formula injection
- Queue worker trusts callback URLs
- Webhook processor lacks authorization

### Why AI Helps

The security impact may occur later in a different component. AI can reason about delayed processing and trust boundaries from architecture and documentation.

### Validation Needed

Trace the full lifecycle from input submission to backend processing.

---

## 13. Architecture Trust Boundary Violations

### Examples

- Frontend controls price or role
- Gateway trusts `X-User-Role`
- Internal API exposed externally
- Backend trusts client-supplied tenant ID
- Service-to-service calls lack authentication

### Why AI Helps

This is design-level reasoning. Traditional DAST sees external symptoms but not the architecture assumptions.

### Validation Needed

Map the trust boundary and prove user-controlled input crosses it unsafely.

---

## 14. LLM / AI Application Security Issues

### Examples

- Prompt injection
- Indirect prompt injection through documents or websites
- Tool abuse by AI agent
- Retrieval-augmented generation data leakage
- Excessive agency
- System prompt or hidden context leakage

### Why AI Helps

These issues are language and behavior driven. Traditional DAST does not understand whether an AI model followed malicious instructions or invoked an unsafe tool.

### Validation Needed

Record prompt, model response, tool action, data exposure, and business impact.

---

## 15. Scanner Finding Triage and Exploitability Reasoning

### Examples

- Group duplicate findings
- Identify noisy low-impact issues
- Prioritize exploitable findings
- Suggest safe validation steps
- Convert raw scanner output into test plans

### Why AI Helps

Scanners are optimized to detect. AI is better at summarizing, clustering, and reasoning over evidence.

### Validation Needed

Do not accept AI severity or exploitability claims without evidence.

---

## 2. Vulnerability Types Best Delegated to Traditional DAST Scanners

Traditional DAST scanners are strongest where detection is **dynamic, repeatable, payload-driven, and measurable**.

## 1. SQL Injection

### Why Scanners Are Better

SQL injection can often be detected through:

- SQL error messages
- boolean response differences
- time delays
- out-of-band callbacks
- database-specific behavior

DAST tools can test many payloads across many parameters consistently.

### AI Role

AI can help explain or craft targeted payloads, but the scanner should perform the broad dynamic testing.

---

## 2. Reflected XSS

### Why Scanners Are Better

Reflected XSS is usually detectable by injecting payloads and observing whether they are reflected and executable in browser-relevant contexts.

### AI Role

AI can help interpret complex contexts, but browser-backed DAST is better for proof.

---

## 3. Stored XSS

### Why Scanners Are Better

Scanners can submit payloads, crawl later pages, and detect stored execution.

### AI Role

AI helps identify where stored payloads may later appear, especially in admin views, exports, notifications, or reports.

---

## 4. DOM XSS

### Why Scanners Are Better

DOM XSS requires runtime browser behavior, JavaScript execution, source-to-sink observation, and context handling.

### AI Role

AI can review JavaScript and suggest risky sinks, but dynamic browser instrumentation is stronger for confirmation.

---

## 5. Path Traversal / Local File Inclusion

### Why Scanners Are Better

Traversal is payloadable and measurable:

```text
../
..%2f
....//
%252e%252e%252f
```

Scanners can try many encodings and check for known file signatures.

### AI Role

AI can suggest bypasses, but scanners are better for systematic testing.

---

## 6. Command Injection

### Why Scanners Are Better

Command injection can be tested using:

- response output
- time delay
- DNS callbacks
- HTTP callbacks

### AI Role

AI can help identify likely parameters and explain impact, but dynamic confirmation belongs to scanners/tools.

---

## 7. XXE

### Why Scanners Are Better

XXE is usually payload-driven and confirmable through:

- file read
- SSRF
- error messages
- out-of-band callbacks

### AI Role

AI helps identify XML/SOAP/upload surfaces, but scanners are better for payload execution testing.

---

## 8. SSRF with Detectable Callback

### Why Scanners Are Better

When SSRF can be confirmed via DNS/HTTP interaction, scanner/OAST tooling is much stronger than AI speculation.

### AI Role

AI helps identify high-value SSRF parameters and likely impact paths.

---

## 9. HTTP Request Smuggling

### Why Scanners Are Better

Request smuggling depends on precise protocol behavior, request framing, timing, and front-end/back-end parsing differences.

### AI Role

AI can explain variants, but scanner tooling is needed for reliable testing.

---

## 10. Server-Side Template Injection

### Why Scanners Are Better

SSTI has strong dynamic signals:

```text
{{7*7}} -> 49
${7*7}
<%= 7*7 %>
```

Scanners can test multiple template syntaxes quickly.

### AI Role

AI can help fingerprint template engines and escalate confirmed SSTI safely.

---

## 11. Open Redirect

### Why Scanners Are Better

Open redirect is cheap and deterministic to test:

```text
?next=https://attacker.example
?redirect=//attacker.example
```

### AI Role

AI adds prioritization and explains phishing/OAuth impact.

---

## 12. CORS Misconfiguration

### Why Scanners Are Better

CORS can be tested by sending controlled `Origin` headers and checking:

```text
Access-Control-Allow-Origin
Access-Control-Allow-Credentials
Vary: Origin
```

### AI Role

AI helps assess whether the affected endpoint exposes sensitive data.

---

## 13. Security Headers and Cookie Flags

### Examples

- Missing `HttpOnly`
- Missing `Secure`
- Weak `SameSite`
- Missing or weak CSP
- Missing clickjacking protection
- Missing HSTS

### Why Scanners Are Better

These are passive deterministic HTTP checks.

### AI Role

AI can reduce noise by explaining which missing headers matter in the specific application context.

---

## 14. TLS and Certificate Configuration

### Examples

- Expired certificate
- Weak TLS version
- Weak cipher suite
- Insecure redirects
- Missing HSTS

### Why Scanners Are Better

TLS configuration is directly measurable through protocol negotiation and certificate inspection.

### AI Role

AI can summarize and prioritize remediation.

---

## 15. Known Vulnerable Components and Exposed Default Services

### Examples

- Old Tomcat, Jenkins, Apache, Nginx, WordPress, phpMyAdmin
- Exposed actuator endpoints
- Default admin consoles
- Version banners mapped to known CVEs

### Why Scanners Are Better

DAST scanners and template tools are better at fingerprinting versions, banners, known paths, and matching CVE databases.

### AI Role

AI can help determine whether the exposed component is reachable, relevant, exploitable, or duplicate noise.

---

## Related Documents

- [AI vs DAST Comparison: Main Document](ai-vs-dast-comparison.md) — decision framework, delegation matrix, workflow, and counter-evidence
- [AI vs DAST Comparison: Evidence Base](ai-vs-dast-comparison-evidence.md) — full evidence base, citation mapping, and references
- [AI vs SAST/SCA Delegation Model](ai-vs-sast-comparison.md) — counterpart for static analysis tool delegation
- [Reference File Standards](reference-standards.md) — structural standards for all reference files in this repository

## References

External sources supporting the delegation assignments are listed in the [Evidence Base](ai-vs-dast-comparison-evidence.md) file.
