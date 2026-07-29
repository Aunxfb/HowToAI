---
title: "AI vs DAST Comparison: Evidence Base and References"
description: "Complete evidence base supporting the AI vs traditional DAST scanner delegation model, including AI cyber-agent studies, OWASP guidance, DAST scanner documentation, and citation mapping."
status: active
tags: [security, penetration-testing, dast, ai-testing, vulnerability-assessment, web-security, references, evidence]
last_verified: 2026-07-29
layer: cold
applies_to: "web application security testing, penetration testing workflow"
---

# AI vs DAST Comparison: Evidence Base and References

## Overview

This file contains the complete evidence base supporting the AI vs traditional DAST scanner delegation model. It includes four evidence groups: AI cyber-agent and vulnerability-detection studies, OWASP security testing guidance, DAST scanner documentation, and a practical citation mapping. Use this file when you need to verify the factual basis for any delegation claim in the main framework, cite specific sources, or evaluate the strength of the evidence behind each recommendation.

## Background

The delegation model in the main framework assigns vulnerability types to AI, DAST, or human validation based on the nature of detection required. Each assignment is supported by peer-reviewed research, OWASP guidance, or established tooling documentation. This file collects all supporting evidence in one place so that claims can be traced to their original sources.

Evidence sources are classified into three tiers of strength:

- **Tier 1 — Peer-reviewed studies**: Academic papers from arxiv and conferences. These carry the most weight for supporting delegation claims.
- **Tier 2 — OWASP guidance**: Community-vetted standards and testing guides. Authoritative for vulnerability taxonomy and testing methodology.
- **Tier 3 — Vendor/industry documentation**: Tool documentation and academy guides. Useful for understanding scanner capabilities but may reflect vendor positioning rather than objective assessment.

The evidence is organized into four groups:

- **Group 1**: AI cyber-agent studies evaluating LLM performance in penetration testing and vulnerability detection
- **Group 2**: OWASP guidance that explicitly or implicitly supports AI-advantaged vulnerability classes
- **Group 3**: DAST scanner documentation that supports scanner-advantaged vulnerability classes
- **Group 4**: A practical citation mapping table linking each claim to its source

## How to Use This Evidence

Each evidence entry follows a consistent structure:

- **Source heading** with title and links
- **Use this to support** — the specific claims this source backs
- **Key relevance** — what the source actually says
- **Supports this statement** (or "Supports these classes") — the direct mapping to the delegation model

When evaluating a delegation claim in the main framework, look up the relevant source here to verify its strength and any limitations the source itself may report.

---

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

OWASP's guidance covers APIs that expose or allow modification of object properties that the user should not be allowed to read or change.

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

OWASP's LLM Top 10 describes prompt injection, sensitive information disclosure, system prompt leakage, tool abuse, and excessive agency as major risks in LLM applications.

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

PortSwigger's Burp documentation describes using Burp Scanner active scanning to test requests for SQL injection vulnerabilities and review flagged SQL injection issues.

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

---

## Related Documents

- [AI vs DAST Comparison: Main Document](ai-vs-dast-comparison.md) — decision framework, delegation matrix, workflow, and counter-evidence
- [AI vs DAST Comparison: Deep Dives](ai-vs-dast-comparison-deep-dives.md) — per-vulnerability type descriptions for all 30 AI and DAST-delegated categories
- [AI vs SAST/SCA Delegation Model](ai-vs-sast-comparison.md) — counterpart for static analysis tool delegation
- [Reference File Standards](reference-standards.md) — structural standards for all reference files in this repository

## References

All sources are listed with full URLs in the evidence groups above. Key external repositories:

- ARTEMIS: https://arxiv.org/abs/2512.09882
- Cybench: https://arxiv.org/abs/2408.08926
- SAST vs LLM: https://arxiv.org/abs/2407.16235
- Sifting the Noise: https://arxiv.org/abs/2601.22952
- OWASP WSTG Workflow Testing: https://owasp.org/www-project-web-security-testing-guide/
- OWASP API Security Top 10: https://owasp.org/API-Security/
- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP ZAP: https://www.zaproxy.org/docs/alerts/
- PortSwigger Burp Suite: https://portswigger.net/burp/documentation
- PortSwigger Web Security Academy: https://portswigger.net/web-security
