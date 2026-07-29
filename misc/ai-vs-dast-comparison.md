# AI vs Traditional DAST Scanner: Vulnerability Delegation Summary

## Executive Summary

AI and traditional DAST scanners should not be treated as competing replacements. They are strongest in different parts of the pentest workflow.

**Delegate to AI when the test requires understanding context, intent, workflow, roles, ownership, state transitions, or cross-endpoint relationships.**

**Delegate to traditional DAST scanners when the vulnerability can be detected through payload injection, measurable response differences, protocol behavior, browser execution, or known signature checks.**

The strongest workflow is:

```text
Scanner = broad deterministic detection
AI = reasoning, prioritization, hypothesis generation
Human = validation, exploitability judgment, impact assessment
```

---

## Decision Rule

| Question | Best First Approach |
|---|---|
| Can this be detected by sending payloads and observing responses? | Traditional DAST scanner |
| Does this require understanding whether the application behavior is allowed or forbidden? | AI-assisted testing |
| Does this depend on user roles, object ownership, tenant boundaries, or workflow state? | AI-assisted testing |
| Does this map to a known CVE, missing header, TLS issue, or common injection pattern? | Traditional scanner |
| Does this require final severity, business impact, or safe proof of exploitability? | Human validation |

---

# 1. Vulnerability Types Best Delegated to AI

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

# 2. Vulnerability Types Best Delegated to Traditional DAST Scanners

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

# 3. Delegation Matrix

| Vulnerability / Test Type | AI | Traditional DAST | Human |
|---|---:|---:|---:|
| Business logic flaws | High | Low | High |
| BOLA / IDOR | High | Medium | High |
| RBAC / BFLA | High | Low-Medium | High |
| Cross-tenant isolation | High | Low-Medium | High |
| State-machine abuse | High | Low | High |
| SQL injection | Medium | High | Medium |
| Reflected XSS | Medium | High | Medium |
| Stored XSS | Medium | High | Medium |
| DOM XSS | Medium | High | Medium |
| Path traversal | Low-Medium | High | Medium |
| Command injection | Medium | High | High |
| XXE | Medium | High | Medium |
| SSRF | Medium | High | High |
| Request smuggling | Low-Medium | High | High |
| Security headers | Low | High | Low-Medium |
| TLS configuration | Low | High | Low |
| Known vulnerable components | Low-Medium | High | Medium |
| LLM app prompt injection | High | Low | High |
| Architecture trust boundaries | High | Low | High |
| Scanner triage | High | Medium | High |

---

# 4. Recommended Workflow

## Phase 1: Traditional Scanner First

Run DAST/scanner tooling for deterministic coverage:

```text
SQLi
XSS
path traversal
command injection
XXE
SSRF callback checks
request smuggling
SSTI
open redirect
CORS
headers/cookies
TLS
known exposed services
known CVE fingerprints
```

Goal:

```text
Get broad measurable coverage quickly.
```

---

## Phase 2: AI-Assisted Context Review

Feed AI:

```text
OpenAPI / Swagger
Burp sitemap
HTTP request/response samples
scanner findings
role matrix
test accounts
user stories
architecture diagrams
frontend routes
JavaScript bundles
```

Ask AI to produce:

```text
authorization matrix
object ownership model
tenant-boundary parameters
workflow abuse cases
state-machine bypass tests
scanner finding prioritization
missing evidence checklist
```

Goal:

```text
Find what scanners are structurally bad at finding.
```

---

## Phase 3: Human Validation

Humans must validate:

```text
exploitability
business impact
scope safety
reproduction quality
severity
chaining potential
client-facing explanation
```

Goal:

```text
Convert hypotheses into defensible findings.
```

---

# 5. Practical Rule of Thumb

## Delegate to AI when the vulnerability depends on:

```text
meaning
intent
workflow
ownership
role expectations
tenant boundaries
state transitions
business rules
cross-endpoint chaining
documentation mismatch
architecture assumptions
```

## Delegate to scanners when the vulnerability depends on:

```text
payload execution
response differences
browser behavior
protocol behavior
headers
TLS negotiation
known paths
known versions
CVE fingerprints
repeatable dynamic checks
```

## Keep humans responsible for:

```text
proof
impact
scope
ethics
severity
creative chaining
final reporting
```

---

# 6. Final Summary

AI is best used as a **semantic pentest assistant**. It helps identify tests that require understanding how the application is supposed to work.

Traditional DAST scanners are best used as **dynamic measurement engines**. They find vulnerabilities that can be proven through payloads, signatures, response behavior, and protocol checks.

The highest-value security workflow is not choosing one over the other. It is:

```text
Use scanners to find measurable technical flaws.
Use AI to find context-dependent abuse cases and prioritize evidence.
Use humans to validate exploitability and business impact.
```

## Evidence Base / References

The AI-vs-scanner delegation model is supported by three evidence groups:

1. AI cyber-agent and vulnerability-detection studies
2. OWASP security testing guidance
3. DAST scanner documentation

---

### 1. AI Cyber-Agent and AI Vulnerability Detection Evidence

#### Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing / ARTEMIS

**Link:** https://arxiv.org/abs/2512.09882  
**PDF:** https://arxiv.org/pdf/2512.09882

**Use this to support:**

- AI can be effective in scoped, tool-driven penetration testing.
- AI is strong at systematic enumeration, parallel testing, and triage.
- AI still has false-positive issues and struggles with GUI-heavy tasks.
- AI should not be treated as a complete replacement for humans.

**Key relevance:**

The ARTEMIS study evaluated AI agents against 10 cybersecurity professionals in a live university network of around 8,000 hosts across 12 subnets. ARTEMIS placed second overall, found 9 valid vulnerabilities, achieved an 82% valid submission rate, and outperformed 9 of 10 human participants. However, the paper also reports that existing agent scaffolds underperformed most humans, and that AI agents had higher false-positive rates and struggled with GUI-based tasks.

**Supports this statement:**

> AI is useful as a semantic and orchestration layer for enumeration, triage, and context-aware hypothesis generation, but humans remain necessary for validation, exploitability, and final impact assessment.

---

#### Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models

**Link:** https://arxiv.org/abs/2408.08926  
**PDF:** https://arxiv.org/pdf/2408.08926  
**Project:** https://cybench.github.io

**Use this to support:**

- AI can solve some offensive security tasks when the environment is structured.
- AI performance drops on harder, longer-horizon cyber tasks.
- AI capability should be treated as uneven rather than universally strong.

**Key relevance:**

Cybench evaluates language-model agents on 40 professional-level CTF tasks from four competitions. The paper reports that top agents solved complete tasks that human teams solved in up to 11 minutes, while the hardest task took human teams 24 hours and 54 minutes and remained beyond existing agents.

**Supports this statement:**

> AI is valuable for guided exploitation, task decomposition, and tool-assisted workflows, but current agents still struggle with complex, long-horizon exploitation compared with skilled humans.

---

#### Comparison of Static Application Security Testing Tools and Large Language Models for Repo-Level Vulnerability Detection

**Link:** https://arxiv.org/abs/2407.16235  
**PDF:** https://arxiv.org/pdf/2407.16235

**Use this to support:**

- AI can have higher recall than traditional static tools in some vulnerability-detection settings.
- AI also tends to suffer from higher false positives.
- AI is better used for candidate discovery and triage than as a final vulnerability oracle.

**Key relevance:**

This paper compares 15 SAST tools with 12 open-source LLMs for repo-level vulnerability detection. It found that SAST tools had lower vulnerability detection rates but relatively low false positives, while LLMs could detect more vulnerabilities but suffered from high false positives.

**Supports this statement:**

> AI findings should be treated as hypotheses until proven. AI is useful for generating candidates and reducing triage burden, but final findings require evidence.

---

#### Sifting the Noise: A Comparative Study of LLM Agents in Vulnerability False Positive Filtering

**Link:** https://arxiv.org/abs/2601.22952  
**PDF:** https://arxiv.org/pdf/2601.22952

**Use this to support:**

- AI is useful for scanner/SAST finding triage.
- AI can reduce false positives, but aggressive filtering can also suppress true positives.
- AI-assisted triage should remain human-reviewed.

**Key relevance:**

This study evaluates LLM-based agent frameworks for vulnerability false-positive filtering. It reports that LLM agents can reduce large volumes of SAST noise, but the benefit varies by model, CWE, and agent design. It also warns that aggressive filtering can suppress true vulnerabilities.

**Supports this statement:**

> AI is best used to cluster, prioritize, and explain scanner output, not to automatically decide exploitability or severity.

---

### 2. OWASP Guidance Supporting AI-Advantaged Vulnerability Classes

#### OWASP WSTG: Testing for the Circumvention of Work Flows

**Link:** https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows  
**GitHub source:** https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows.md

**Use this to support:**

- Business logic and workflow abuse are application-specific.
- Workflow vulnerabilities require misuse cases based on intended process.
- Generic scanners are structurally weak here because the issue is not necessarily a malformed request or obvious payload.

**Key relevance:**

OWASP describes workflow-circumvention vulnerabilities as cases where an attacker misuses an application or system to avoid the designed or intended workflow. The guide explains that testing requires developing business logic abuse/misuse cases that complete a process without following the correct steps in the correct order.

**Supports these AI-delegated classes:**

- Business logic flaws
- Workflow bypass
- State-machine abuse
- Function-use limit abuse
- Account recovery abuse
- Payment/refund/order lifecycle abuse

---

#### OWASP API Security Top 10 2023: API1 Broken Object Level Authorization

**Link:** https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/

**Use this to support:**

- BOLA/IDOR is about object-level permission, not merely endpoint access.
- Every endpoint that receives an object ID should check whether the logged-in user has permission to act on that object.
- Scanners struggle unless they understand users, objects, tenants, and ownership relationships.

**Key relevance:**

OWASP states that object-level authorization checks should validate that the logged-in user has permission to perform the requested action on the requested object. This directly supports the claim that BOLA/IDOR requires ownership-aware testing, not just generic parameter fuzzing.

**Supports these AI-delegated classes:**

- BOLA / IDOR
- Cross-tenant isolation failure
- Object ownership abuse
- GraphQL object authorization
- Multi-account authorization testing

---

#### Broken Object Level Authorization in the Wild: An Empirical Taxonomy from 100+ Bug Bounty Disclosures

**Link:** https://arxiv.org/abs/2605.25865  
**PDF:** https://arxiv.org/pdf/2605.25865

**Use this to support:**

- BOLA/IDOR appears frequently in real bug bounty disclosures.
- BOLA often involves action-level object abuse, not only direct read access.
- GraphQL Global IDs appear as a real-world exploitation pattern.

**Key relevance:**

This paper analyzes public HackerOne disclosures tagged IDOR or improper access control and classifies confirmed BOLA cases. It is useful for supporting the claim that object-level authorization testing needs context-aware reasoning over resources, actions, ownership, and roles.

---

#### OpenAPI Specification Extended Security Scheme: A Method to Reduce the Prevalence of Broken Object Level Authorization

**Link:** https://arxiv.org/abs/2212.06606  
**PDF:** https://arxiv.org/pdf/2212.06606

**Use this to support:**

- OpenAPI security definitions do not sufficiently express object-level authorization.
- BOLA cannot be fully captured by generic API authentication schemes.
- API specifications need extra object-level security semantics.

**Key relevance:**

The paper argues that OpenAPI security properties do not address object authorization and that object-level security is largely left to developers. This supports using AI to reason over OpenAPI specs, object IDs, roles, and ownership boundaries.

---

#### OWASP API Security Top 10 2023: API3 Broken Object Property Level Authorization

**Link:** https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/

**Use this to support:**

- Some authorization bugs are at the property/field level, not the endpoint or object level.
- APIs may allow users to manipulate properties they should not control.
- This supports AI-assisted review of schema, request bodies, and field-level trust assumptions.

**Key relevance:**

OWASP�s guidance covers APIs that expose or allow modification of object properties that the user should not be allowed to read or change.

**Supports these AI-delegated classes:**

- Mass assignment / excessive data exposure
- Field-level authorization
- Client-controlled price, role, status, or tenant fields
- API documentation vs implementation mismatch

---

#### OWASP Top 10 for LLM Applications 2025

**Link:** https://owasp.org/www-project-top-10-for-large-language-model-applications/  
**PDF:** https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf

**Use this to support:**

- LLM application risks are not well covered by traditional DAST.
- Prompt injection, sensitive information disclosure, excessive agency, and tool abuse require language/context-aware testing.
- AI/LLM app testing requires evaluation of model behavior, tool behavior, and indirect instruction handling.

**Key relevance:**

OWASP�s LLM Top 10 describes prompt injection, sensitive information disclosure, system prompt leakage, tool abuse, and excessive agency as major risks in LLM applications.

**Supports these AI-delegated classes:**

- Prompt injection
- Indirect prompt injection
- RAG data leakage
- Tool abuse
- Excessive agency
- System prompt leakage
- LLM-driven unauthorized actions

---

#### OWASP LLM06: Excessive Agency

**Link:** https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html

**Use this to support:**

- LLM-agent vulnerabilities often involve the model taking unsafe actions through tools.
- The issue is not only prompt text; it is the combination of model behavior, tool permissions, and authorization design.
- Traditional scanners cannot fully evaluate whether an agent should or should not perform an action.

**Key relevance:**

OWASP describes excessive agency as a risk where an LLM-based system is granted the ability to call tools, functions, extensions, or external systems, potentially leading to unsafe actions.

---

### 3. Evidence Supporting Traditional DAST-Advantaged Vulnerability Classes

#### OWASP ZAP Alert Details

**Link:** https://www.zaproxy.org/docs/alerts/  
**Passive scan rules:** https://www.zaproxy.org/docs/desktop/addons/passive-scan-rules/  
**Active scan rules:** https://www.zaproxy.org/docs/desktop/addons/active-scan-rules/

**Use this to support:**

- DAST tools are explicitly built around active and passive scan rules.
- Traditional scanners are strong for known, measurable HTTP issues.
- Scanner findings map well to deterministic checks such as headers, injection classes, misconfigurations, and known patterns.

**Key relevance:**

ZAP documents HTTP passive and active scan rules that find specific vulnerabilities. This supports scanner-first delegation for issues that can be detected through direct HTTP behavior, payloads, or passive response inspection.

**Supports scanner-delegated classes:**

- Security headers
- Cookie flags
- XSS
- SQL injection
- Path traversal
- Command injection
- CORS
- Information disclosure
- Known HTTP misconfigurations

---

#### Burp Suite Documentation: Testing for SQL Injection Vulnerabilities

**Link:** https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/sql-injection/testing

**Use this to support:**

- SQL injection is scanner-friendly because it can be actively tested using payloads.
- Burp Scanner is explicitly designed to audit requests for SQL injection issues.
- SQLi belongs in the scanner-first category.

**Key relevance:**

PortSwigger�s Burp documentation describes using Burp Scanner active scanning to test requests for SQL injection vulnerabilities and review flagged SQL injection issues.

**Supports scanner-delegated classes:**

- SQL injection
- Error-based SQLi
- Boolean-based SQLi
- Time-based SQLi
- Parameter injection testing

---

#### PortSwigger Web Security Academy: HTTP Request Smuggling

**Link:** https://portswigger.net/web-security/request-smuggling

**Use this to support:**

- Request smuggling is protocol-behavior driven.
- It depends on front-end and back-end parsing differences.
- Reliable detection requires precise request construction and response observation, which is better suited to scanner/tooling workflows than pure AI reasoning.

**Key relevance:**

PortSwigger describes HTTP request smuggling as a technique that interferes with how a website processes sequences of HTTP requests. It is associated with protocol parsing differences and can bypass security controls or compromise users.

**Supports scanner-delegated classes:**

- HTTP request smuggling
- CL.TE / TE.CL behavior
- HTTP/2 downgrade or translation issues
- Front-end/back-end parser inconsistencies

---

#### PortSwigger Web Security Academy: SQL Injection

**Link:** https://portswigger.net/web-security/sql-injection

**Use this to support:**

- SQL injection is a mature, payload-driven vulnerability class.
- Detection relies heavily on dynamic testing and observable response behavior.
- Scanner automation is effective for broad coverage.

---

#### PortSwigger Web Security Academy: Cross-Site Scripting

**Link:** https://portswigger.net/web-security/cross-site-scripting

**Use this to support:**

- XSS is strongly tied to payload execution, browser context, and response rendering.
- DAST/browser-based tools are well-suited to reflected, stored, and DOM XSS testing.

---

#### PortSwigger Web Security Academy: Server-Side Request Forgery

**Link:** https://portswigger.net/web-security/ssrf

**Use this to support:**

- SSRF is best confirmed dynamically through response behavior or out-of-band callbacks.
- AI can identify likely SSRF parameters, but scanner/OAST tooling is needed for proof.

---

#### PortSwigger Web Security Academy: XML External Entity Injection

**Link:** https://portswigger.net/web-security/xxe

**Use this to support:**

- XXE is payload-driven and can often be confirmed through file-read behavior, SSRF, error messages, or out-of-band interactions.

---

#### PortSwigger Web Security Academy: Path Traversal

**Link:** https://portswigger.net/web-security/file-path-traversal

**Use this to support:**

- Path traversal is scanner-friendly because payload encodings and file signatures can be tested systematically.

---

#### PortSwigger Web Security Academy: OS Command Injection

**Link:** https://portswigger.net/web-security/os-command-injection

**Use this to support:**

- Command injection is best confirmed dynamically through output, time delays, or out-of-band callbacks.

---

#### PortSwigger Web Security Academy: Server-Side Template Injection

**Link:** https://portswigger.net/web-security/server-side-template-injection

**Use this to support:**

- SSTI has strong dynamic detection signals such as expression evaluation and template-engine-specific behavior.

---

#### PortSwigger Web Security Academy: CORS

**Link:** https://portswigger.net/web-security/cors

**Use this to support:**

- CORS misconfiguration is testable by sending controlled `Origin` headers and observing response headers.

---

### 4. Practical Citation Mapping

| Claim | Use These Sources |
|---|---|
| AI can outperform humans in narrow, scoped, tool-driven pentest settings, but has limitations | ARTEMIS: https://arxiv.org/abs/2512.09882 |
| AI solves some structured cyber tasks but struggles with harder long-horizon exploitation | Cybench: https://arxiv.org/abs/2408.08926 |
| AI can have higher recall but higher false positives than deterministic tools | SAST vs LLM comparison: https://arxiv.org/abs/2407.16235 |
| AI can help reduce scanner/SAST triage noise but needs review | Sifting the Noise: https://arxiv.org/abs/2601.22952 |
| Business logic and workflow bypass are application-specific | OWASP WSTG workflow testing: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/06-Testing_for_the_Circumvention_of_Work_Flows |
| BOLA/IDOR requires object ownership and authorization context | OWASP API1: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/ |
| BOLA appears in real bug bounty disclosures and includes action-level object abuse | BOLA in the Wild: https://arxiv.org/abs/2605.25865 |
| Field/property-level authorization needs schema and business-context reasoning | OWASP API3: https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/ |
| LLM app vulnerabilities require prompt/tool/model-behavior testing | OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/ |
| DAST scanners are built for active/passive HTTP checks | OWASP ZAP alerts: https://www.zaproxy.org/docs/alerts/ |
| SQLi is scanner-first because it is actively testable through payloads and responses | Burp SQLi docs: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/sql-injection/testing |
| Request smuggling is scanner/tooling-first because it depends on HTTP parsing and protocol behavior | PortSwigger request smuggling: https://portswigger.net/web-security/request-smuggling |

---

### 5. Safe Final Wording

> The evidence does not support replacing scanners or human pentesters with AI. It supports a hybrid delegation model. AI is strongest for context-dependent vulnerability discovery, test-case generation, scanner-output triage, and reasoning over roles, workflows, ownership, and architecture. Traditional DAST scanners remain stronger for deterministic, payload-driven, protocol-observable, and signature-based vulnerability classes. Humans remain necessary for exploitability validation, business impact assessment, safe proof, and final severity judgment.

## Counter-Evidence to the Delegation Model: Where the Boundary Can Reverse

The AI-vs-scanner split is useful, but it is not absolute. Some evidence suggests AI can outperform scanners on traditionally scanner-owned vulnerability classes, and modern scanners can increasingly detect some context-heavy authorization issues that were historically considered manual or AI-assisted.

The safest position is:

> The delegation model describes the default advantage, not a permanent capability boundary.

---

### 1. AI Can Sometimes Beat Traditional Scanners on SQL Injection

The original delegation model places SQL injection in the scanner-first category because SQLi is payload-driven and dynamically measurable. However, some research argues that LLM-powered scanners can outperform traditional black-box SQLi tools.

#### Evidence

**SqliGPT: Evaluating and Utilizing Large Language Models for Automated SQL Injection Black-Box Detection**

This paper argues that traditional black-box SQLi scanners rely heavily on predefined payload rules and can lack diversity in payload scheduling. The authors propose SqliGPT, an LLM-powered black-box SQLi scanner designed to use contextual reasoning and adaptive payload generation. :contentReference[oaicite:0]{index=0}

#### Why this challenges the scanner-first claim

It suggests that for SQLi, AI may help with:

- payload selection
- payload mutation
- bypass generation
- deciding what to test next
- adapting to response context

#### How to interpret it

This does **not** mean �AI replaces SQLi scanners.� It means the best SQLi scanner may increasingly be a **scanner with AI-assisted payload strategy**.

Safe wording:

> SQL injection remains scanner-first for proof, but AI can improve payload generation, scheduling, and bypass discovery. The winning architecture may be AI-assisted DAST rather than pure scanner or pure LLM.

---

### 2. AI May Be Stronger Than Scanners at WAF Bypass Payload Generation

The scanner-first model assumes scanner payload libraries are strong for SQLi, XSS, SSTI, and command injection. However, LLMs can generate novel or adapted payloads that are not in static payload lists.

#### Evidence

**Adversarial SQL Injection Generation with LLM-Based Architectures**

This 2026 paper evaluates LLM-based SQLi payload generation against 10 WAFs and a MySQL validator. It reports that the proposed RADAGAS-GPT4o system achieved the best overall bypass rate in their experiments, with particularly high bypass rates against some AI/ML-based WAFs. However, it struggled against rule-based WAFs such as ModSecurity and Coraza in some configurations. :contentReference[oaicite:1]{index=1}

#### Why this challenges the scanner-first claim

It suggests AI can outperform static payload lists when the goal is:

- generating adversarial variants
- mutating payloads
- bypassing filters
- exploring non-obvious encodings

#### How to interpret it

This supports a narrower claim:

> For classic injection classes, scanners are still better at broad execution and proof, but AI may outperform static scanners in payload creativity and bypass generation.

It does **not** prove AI is better at confirming exploitable SQLi end-to-end.

---

### 3. AI Can Help With XSS Payload Generation, but Runtime Validation Still Matters

XSS was placed in the scanner-first category because browser execution and runtime context matter. Some research explores using LLMs to generate obfuscated XSS payloads, which could challenge traditional payload libraries.

#### Evidence

**Evaluating LLM-Generated Obfuscated XSS Payloads for Machine Learning-Based Detection**

This paper tests LLM-generated obfuscated XSS payloads and emphasizes runtime browser evaluation. The results show some promise, but also significant limitations: untuned models had low behavior-preserving match rates, and fine-tuning improved results only modestly. The paper concludes that runtime behavior checks are essential. :contentReference[oaicite:2]{index=2}

#### Why this partially challenges the scanner-first claim

AI may help generate payload variants, but the evidence also reinforces the original scanner-first position because runtime behavior validation remains necessary.

Safe wording:

> AI can assist XSS payload generation, but XSS remains scanner/browser-tooling-first for proof because payload validity depends on runtime execution.

---

### 4. Modern DAST Scanners Can Detect Some BOLA, IDOR, and BFLA Issues

The original model places BOLA/IDOR, BFLA, RBAC, and tenant isolation in the AI-assisted/manual category. That is still generally true, but modern API security scanners increasingly support multi-session authorization testing.

#### Evidence

**Invicti API Access Control Testing**

Invicti documents API access control testing for IDOR, BOLA, and BFLA using multi-session scanning. This directly challenges the simplistic claim that scanners cannot test authorization issues. :contentReference[oaicite:3]{index=3}

#### Why this challenges the AI-first claim

A scanner can detect some authorization flaws when it is given:

- multiple authenticated sessions
- different user roles
- comparable objects
- API definitions
- stateful scan configuration

#### How to interpret it

This does **not** mean scanners understand business authorization by default. It means authorization testing becomes scanner-friendly when the tester supplies the missing context.

Safe wording:

> BOLA and BFLA are not impossible for scanners. They are difficult for generic unauthenticated or single-session DAST. Modern multi-session API scanners can detect some access-control flaws when provided with roles, accounts, and comparable resources.

---

### 5. Dedicated IDOR/BOLA Automation Exists

There are purpose-built tools that automate parts of IDOR testing by manipulating object identifiers and comparing responses.

#### Evidence

The IDORD project describes itself as an automated IDOR vulnerability scanner that tests object identifiers in API requests to detect unauthorized access risks. :contentReference[oaicite:4]{index=4}

#### Why this challenges the AI-first claim

It shows that some IDOR testing can be automated without AI, especially when:

- object IDs are obvious
- responses are comparable
- authorization failure is easy to detect
- the tool has multiple accounts or known restricted objects

#### How to interpret it

This does not eliminate AI/human value. It narrows the claim:

> Simple IDOR is automatable. Complex ownership, tenant, workflow, and role-based authorization issues still require context-aware reasoning and human validation.

---

### 6. Some Vendors Claim Business Logic Detection Is Becoming a DAST Feature

Some modern DAST/API security vendors claim business logic, BOLA, and IDOR detection as differentiators.

#### Evidence

Escape�s 2026 DAST tooling guide states that business logic vulnerability detection, including BOLA and IDOR, separates modern DAST from legacy scanners. This is vendor/industry material, so it should be treated as weaker evidence than peer-reviewed papers or OWASP guidance, but it shows the market direction. :contentReference[oaicite:5]{index=5}

#### Why this challenges the AI-first claim

It suggests scanner tooling is moving upward from classic payload testing into:

- API schema analysis
- authenticated multi-user testing
- authorization modeling
- object access comparison
- business-logic heuristics

#### How to interpret it

Safe wording:

> Business logic testing is not permanently outside scanner scope. However, scanner effectiveness depends heavily on whether the tool receives enough application context, role data, object mappings, and workflow state.

---

### 7. OWASP Still Warns That Business Logic Usually Requires Manual Assessment

The reverse evidence above should not be overstated. OWASP�s developer guidance still says business logic errors, race condition checks, and certain zero-days usually require manual assessments. :contentReference[oaicite:6]{index=6}

This supports the original model�s core claim:

> Generic DAST remains weak for business logic unless heavily configured, extended, or paired with human/AI context.

---

## Revised Position

The stronger version of the AI-vs-scanner model is:

| Vulnerability Class | Default Advantage | Reverse Case |
|---|---|---|
| SQL injection | Traditional DAST | AI can improve payload generation, scheduling, and bypasses |
| XSS | Traditional DAST/browser tooling | AI can help generate or mutate payloads, but runtime proof is still needed |
| SSRF | Traditional DAST/OAST | AI can identify high-value SSRF candidates and impact paths |
| Request smuggling | Specialized scanner/tooling | AI can explain variants but rarely replaces protocol testing |
| BOLA/IDOR | AI-assisted/manual | Multi-session API scanners can detect simpler cases |
| BFLA/RBAC | AI-assisted/manual | Scanners can test configured role matrices |
| Business logic | AI-assisted/manual | Purpose-built tools may automate narrow workflow checks |
| LLM prompt injection | AI-assisted/manual | Some automated red-team tools can generate and score prompt attacks |
| Scanner triage | AI-assisted | Traditional tools remain better at raw detection and reproducibility |

---

## Final Balanced Claim

Use this wording instead of an absolute AI-vs-scanner split:

> AI is generally better suited to vulnerability classes that require semantic reasoning over roles, workflows, object ownership, tenant boundaries, documentation, and architecture. Traditional DAST is generally better suited to vulnerability classes that are payload-driven, response-observable, protocol-measurable, or signature-based. However, the boundary is not fixed. AI can improve scanner-owned tasks such as SQLi and XSS through adaptive payload generation, while modern multi-session API scanners can detect some authorization issues such as BOLA, IDOR, and BFLA when provided with sufficient context. Therefore, the correct model is not AI versus scanner, but context-aware AI-assisted scanning plus human validation.