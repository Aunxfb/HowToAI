---
title: AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence
description: Supporting and contradictory evidence, all 13 references with citations, and claim mapping for the AI vs SAST/SCA/secret scanning delegation model.
status: active
tags: [ai, sast, sca, evidence, references, security, code-review]
last_verified: 2026-07-29
layer: warm
applies_to: secure code review delegation decisions
---

# AI vs SAST/SCA/Secret Scanning Delegation Model -- Evidence

## Overview

This document contains the evidence base for the [AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review](ai-vs-sast-comparison.md). It includes supporting and contradictory evidence from academic benchmarks, empirical studies, and official documentation, as well as all 13 references, the citation mapping table, and suggested citation language. Intended for reviewers who want to verify the delegation claims against the original sources.

---

## Evidence Summary

### Evidence supporting AI-assisted code review

LLMs perform well when vulnerability detection benefits from broader code context, explanation, and semantic interpretation. A 2025 benchmark comparing LLMs with SonarQube, CodeQL, and Snyk Code on C# projects found higher mean F1 scores for LLMs than the static tools, mainly due to higher recall, while also warning that LLMs had noisier output and inaccurate line/column localization.

A multi-language empirical study found that GPT-4o achieved the strongest vulnerability detection and CWE classification scores among tested models, and a user study with 22 developers found that an LLM-assisted VS Code tool helped developers detect vulnerabilities more accurately and faster.

### Evidence contradicting over-delegation to AI

Repository-level and statement-level findings are much weaker. SecVulEval, a real-world C/C++ benchmark covering 25,440 function samples and 5,867 CVEs, found that even the best tested model achieved only **23.83% F1** for detecting vulnerable statements with correct reasoning.

Another ACL 2025 benchmark emphasizes that real-world vulnerabilities often require interprocedural analysis across multi-hop function calls, which is harder than function-level benchmark detection.

LLM-generated repairs are also risky. A Copilot-focused buffer overflow repair study reported a **76% detection rate** but only **15% repair rate**, showing that detecting a bug and producing a safe fix are not equivalent.

### Evidence supporting traditional SAST

SAST remains valuable for systematic, CI-enforceable checks. OWASP describes SAST tools as source-code or compiled-code analyzers that can be integrated into IDEs and development workflows to detect flaws early.

CodeQL's data-flow analysis is specifically designed to track how values propagate through a program and whether untrusted or sensitive data reaches dangerous usage sites.

However, SAST is imperfect. An empirical study of C/C++ secure code review found that a single SAST tool produced warnings in vulnerable functions for **52%** of vulnerability-contributing commits, but at least **76%** of warnings in vulnerable functions were irrelevant to the actual vulnerability, and **22%** of vulnerability-contributing commits remained undetected due to rule limitations.

### Evidence supporting SCA and secret scanners

SCA is the right delegation target for known vulnerable dependencies, license risk, package metadata, SBOM inventory, and transitive dependency exposure. Datadog describes SCA as detecting open-source libraries across repositories and running services, providing visibility into library vulnerabilities and license management.

Secret scanners are also better than generic AI for known token patterns because they can use provider-specific patterns, push protection, and validity checks. GitHub secret scanning supports custom regular expressions, partner patterns, and validity checks that can verify whether a detected credential is still active.

SCA also has limits. A comparative study of nine SCA tools found large variance in reported vulnerable dependencies and known vulnerabilities, concluding that practitioners should not rely on a single SCA tool.

---

## Contradictory Evidence and How to Interpret It

### Claim: "LLMs outperform SAST."

This is sometimes true in narrow benchmarks. The C# benchmark found higher mean F1 scores for GPT-4.1, Mistral Large, and DeepSeek V3 than SonarQube, CodeQL, and Snyk Code on the tested projects. But the same study warned that LLM outputs were noisier and less precise in line/column localization, limiting standalone use in safety-critical audits.

**Interpretation:** Use AI for recall and contextual triage, not as the final gate.

### Claim: "SAST is too noisy to trust."

Also partly true. The C/C++ secure code review study found that SAST warnings can help prioritize vulnerable functions, but many warnings in vulnerable functions were irrelevant and some vulnerabilities were missed entirely.

**Interpretation:** Use SAST as a deterministic signal, not as a complete vulnerability oracle.

### Claim: "AI can find what scanners miss."

True for some context-heavy weaknesses, but not reliably at statement-level precision. SecVulEval found low F1 for vulnerable-statement detection with correct reasoning, showing that LLMs still struggle with fine-grained real-world C/C++ vulnerability localization.

**Interpretation:** AI is strongest as a reviewer assistant and hypothesis generator, weakest as a precise, auditable detector.

### Claim: "SCA gives objective dependency truth."

Only partially. SCA tools vary substantially in what they report, and hidden/shaded/cloned dependencies can create blind spots.

**Interpretation:** Use SCA as the primary dependency control, but validate high-risk dependency exposure with multiple sources, SBOMs, runtime inventory, and human review.

---

## References

> Each reference includes the claim it supports so reviewers can verify the delegation model directly.

### 1. LLMs vs Static Code Analysis Tools: Systematic Benchmark

**Reference:** *Large Language Models Versus Static Code Analysis Tools: A Systematic Benchmark for Vulnerability Detection*
**Link:** https://arxiv.org/abs/2508.04448
**Supports:**

* Direct comparison between LLMs and traditional SAST tools.
* Compared GPT-4.1, Mistral Large, and DeepSeek V3 against SonarQube, CodeQL, and Snyk Code.
* Supports the claim that LLMs can achieve strong vulnerability-detection performance in some benchmark settings.
* Also supports the caution that LLMs may produce noisier output and weaker precise localization than deterministic tooling.

**Use in whitepaper:**
Use this as the main evidence for the statement: "AI-assisted code review can outperform traditional SAST in some benchmark settings, especially on recall, but should not be treated as a standalone authoritative scanner."

---

### 2. SecVulEval: Real-World C/C++ Vulnerability Detection Benchmark

**Reference:** *SecVulEval: Benchmarking LLMs for Real-World C/C++ Vulnerability Detection*
**Link:** https://arxiv.org/abs/2505.19828
**Supports:**

* LLMs still struggle with fine-grained, statement-level vulnerability localization.
* The best-performing tested model achieved only **23.83% F1** for detecting vulnerable statements with correct reasoning.
* Contradicts overconfident claims that AI can reliably replace human or SAST review for precise vulnerability identification.

**Use in whitepaper:**
Use this as the main evidence against fully delegating vulnerability detection to AI. It supports the position that AI should be used for hypothesis generation, explanation, and contextual review, not final authoritative detection.

---

### 3. Copilot Vulnerability Repair Study

**Reference:** *Code Vulnerability Repair with Large Language Model using Context-Aware Prompt Tuning*
**Link:** https://arxiv.org/abs/2409.18395
**Supports:**

* Detection and repair are different capabilities.
* In the buffer-overflow-focused study, Copilot achieved a **76% vulnerability detection rate** but only a **15% repair rate** without additional context-aware prompt tuning.
* Supports the claim that AI-generated security fixes require human review and independent validation.

**Use in whitepaper:**
Use this to justify the rule: "AI can draft fixes, but humans and tests must verify them."

---

### 4. Empirical Study of SAST for Secure Code Review

**Reference:** *An Empirical Study of Static Analysis Tools for Secure Code Review*
**Link:** https://arxiv.org/abs/2407.12241
**Supports:**

* SAST is useful but incomplete.
* A single SAST tool produced warnings in vulnerable functions for **52%** of vulnerability-contributing commits.
* At least **76%** of warnings in vulnerable functions were irrelevant to the actual vulnerability.
* **22%** of vulnerability-contributing commits remained undetected due to SAST rule limitations.

**Use in whitepaper:**
Use this as balanced evidence: SAST helps prioritize review but cannot replace human security review or contextual AI-assisted triage.

---

### 5. OWASP Source Code Analysis Tools

**Reference:** OWASP -- *Source Code Analysis Tools*
**Link:** https://owasp.org/www-community/Source_Code_Analysis_Tools
**Supports:**

* Defines SAST/source-code analysis tools.
* Supports SAST as a method for analyzing source code or compiled code to find security flaws.
* Supports the inclusion of SAST in IDE and CI/CD workflows.

**Use in whitepaper:**
Use this as the authoritative baseline definition of SAST and why it belongs in secure development pipelines.

---

### 6. CodeQL Data Flow Analysis Documentation

**Reference:** GitHub CodeQL -- *About Data Flow Analysis*
**Link:** https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/
**Supports:**

* CodeQL security queries use data-flow analysis.
* Data-flow analysis can identify insecure data use, dangerous arguments passed to functions, and sensitive-data leaks.
* Supports delegating source-to-sink vulnerability classes to SAST/CodeQL.

**Use in whitepaper:**
Use this to justify assigning SQL injection, command injection, XSS, path traversal, SSRF source-to-sink paths, and sensitive-data leaks to traditional SAST first.

---

### 7. GitHub Secret Scanning: Concept Documentation

**Reference:** GitHub Docs -- *Secret Scanning*
**Link:** https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
**Supports:**

* Secret scanning detects credentials committed to repositories.
* Supports provider patterns and automated scanning workflows.
* Supports assigning hardcoded credentials, API keys, cloud keys, and tokens to secret scanners rather than AI.

**Use in whitepaper:**
Use this to support the claim that secret detection should be scanner-first because token patterns and provider integrations are deterministic and scalable.

---

### 8. GitHub Secret Scanning Validity Checks

**Reference:** GitHub Docs -- *Validity Checks*
**Link:** https://docs.github.com/en/code-security/concepts/secret-security/validity-checks
**Supports:**

* Validity checks verify whether a detected secret is still active and exploitable.
* Supports prioritizing active secrets over inactive or already-rotated credentials.
* Strengthens the case that secret scanners outperform AI for credential detection and triage.

**Use in whitepaper:**
Use this to justify: "Secret scanners win because they can identify, classify, and sometimes validate real active credentials."

---

### 9. Datadog Software Composition Analysis Documentation

**Reference:** Datadog Docs -- *Software Composition Analysis*
**Link:** https://docs.datadoghq.com/security/code_security/software_composition_analysis/
**Supports:**

* SCA detects open-source libraries in repositories and running services.
* SCA provides visibility into library vulnerabilities and license management.
* Supports assigning known vulnerable dependencies and license issues to SCA.

**Use in whitepaper:**
Use this as an operational definition of SCA and why dependency and license risks should be delegated to SCA first.

---

### 10. OWASP Dependency-Check

**Reference:** OWASP -- *Dependency-Check*
**Link:** https://owasp.org/www-project-dependency-check/
**Supports:**

* Dependency-Check is an SCA tool that identifies project dependencies and checks whether they contain known publicly disclosed vulnerabilities.
* Supports the use of SCA for known dependency vulnerabilities.

**Use in whitepaper:**
Use this as a vendor-neutral OWASP reference for dependency vulnerability scanning.

---

### 11. Comparative Study of SCA Tool Reporting

**Reference:** *A Comparative Study of Vulnerability Reporting by Software Composition Analysis Tools*
**Link:** https://arxiv.org/abs/2108.12078
**Supports:**

* SCA tools vary significantly in the vulnerable dependencies and vulnerabilities they report.
* The study found large differences across nine SCA tools.
* Supports the caution that organizations should not blindly rely on a single SCA tool for complete dependency-risk truth.

**Use in whitepaper:**
Use this in the contradictory-evidence section: SCA is the right category for dependency risk, but SCA results are not perfectly consistent across tools.

---

### 12. Security Blind Spots of SCA

**Reference:** *On the Security Blind Spots of Software Composition Analysis*
**Link:** https://arxiv.org/abs/2306.05534
**Supports:**

* SCA tools can miss hidden dependencies caused by cloning or shading.
* The study demonstrates that existing SCA tools often miss vulnerable cloned/shaded components.
* Supports the caveat that SCA should be paired with deeper review for shaded, vendored, or copied dependencies.

**Use in whitepaper:**
Use this to qualify the SCA delegation model: "SCA is best for declared dependencies, but hidden/shaded/cloned dependencies may require additional analysis."

---

### 13. Hidden Dependencies and SBOM-Based SCA

**Reference:** *Hidden Dependencies and Component Variants in SBOM-Based Software Composition Analysis*
**Link:** https://arxiv.org/abs/2604.21278
**Supports:**

* SBOM-based analysis depends on accurate component identity and dependency representation.
* Hidden code-level dependencies and component variants can cause inconsistent vulnerability reporting.
* Supports treating SBOM/SCA results as important but not infallible.

**Use in whitepaper:**
Use this to support the statement: "SBOMs and SCA are necessary for dependency governance, but they do not eliminate the need for human validation in complex supply-chain cases."

---

## Mapping References to Delegation Claims

| Delegation claim | Best supporting references |
| ---------------- | ------------------------- |
| AI is useful for contextual vulnerability review but should not replace scanners | References 1, 2, 3 |
| AI can outperform SAST in some benchmark settings | Reference 1 |
| AI struggles with precise vulnerable-statement localization | Reference 2 |
| AI-generated fixes require human validation | Reference 3 |
| SAST is useful but noisy and incomplete | Reference 4 |
| SAST is appropriate for source-code and compiled-code flaw detection | Reference 5 |
| SAST/CodeQL is especially appropriate for source-to-sink data-flow vulnerabilities | Reference 6 |
| Secret scanning should be scanner-first, not AI-first | References 7, 8 |
| SCA should handle known vulnerable dependencies and license risks | References 9, 10 |
| SCA output can vary across tools | Reference 11 |
| SCA can miss hidden, shaded, or cloned dependencies | References 12, 13 |

---

## Suggested Whitepaper Citation Language

> The evidence does not support a clean replacement model where AI substitutes for SAST, SCA, or secret scanning. Instead, current research supports a hybrid model. LLMs can provide strong contextual review and may outperform some static tools in certain benchmark settings, but they also struggle with precise vulnerable-statement localization and reliable repair. Traditional SAST remains useful for repeatable source-to-sink and dangerous-API checks, while SCA and secret scanners remain the correct first-line controls for dependency and credential risks. Human review remains necessary for exploitability, business logic, architecture, and risk acceptance.

## Related Documents

- [AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review](ai-vs-sast-comparison.md) -- main delegation reference with decision matrices, operating principles, and workflow
- [AI vs DAST Comparison](ai-vs-dast-comparison.md) -- counterpart for dynamic analysis tool delegation
- [Reference File Standards](reference-standards.md) -- structural conventions used by all reference files
