# AI vs SAST/SCA/Secret Scanning Delegation Model for Secure Code Review

## Executive Position

AI-assisted code review should be treated as a **contextual reasoning layer**, not as a replacement for deterministic security tooling. The practical split is:

* **Delegate to AI-assisted code review** when the vulnerability depends on business intent, framework conventions, authorization assumptions, multi-file reasoning, reviewer explanation, or secure-fix design.
* **Delegate to traditional SAST/SCA/secret scanners** when the issue is enumerable, rule-backed, policy-backed, dependency-backed, or requires repeatable CI enforcement.
* **Delegate to humans** when the answer depends on threat modeling, asset sensitivity, exploitability, architecture, abuse cases, or deciding whether a risky pattern is acceptable.

The evidence is mixed but consistent on one point: the best-performing workflows are hybrid. Recent LLM studies show strong recall and contextual value, but also poor localization, false positives, weak statement-level reasoning, and unsafe generated fixes. Traditional scanners remain valuable because they are repeatable, auditable, and fast, but they miss context-heavy weaknesses and produce irrelevant warnings.

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

CodeQL�s data-flow analysis is specifically designed to track how values propagate through a program and whether untrusted or sensitive data reaches dangerous usage sites.

However, SAST is imperfect. An empirical study of C/C++ secure code review found that a single SAST tool produced warnings in vulnerable functions for **52%** of vulnerability-contributing commits, but at least **76%** of warnings in vulnerable functions were irrelevant to the actual vulnerability, and **22%** of vulnerability-contributing commits remained undetected due to rule limitations.

### Evidence supporting SCA and secret scanners

SCA is the right delegation target for known vulnerable dependencies, license risk, package metadata, SBOM inventory, and transitive dependency exposure. Datadog describes SCA as detecting open-source libraries across repositories and running services, providing visibility into library vulnerabilities and license management.

Secret scanners are also better than generic AI for known token patterns because they can use provider-specific patterns, push protection, and validity checks. GitHub secret scanning supports custom regular expressions, partner patterns, and validity checks that can verify whether a detected credential is still active.

SCA also has limits. A comparative study of nine SCA tools found large variance in reported vulnerable dependencies and known vulnerabilities, concluding that practitioners should not rely on a single SCA tool.

---

## Delegation Rule of Thumb

| Question                                                           | Best first delegate                       |
| ------------------------------------------------------------------ | ----------------------------------------- |
| �Is this known dependency vulnerable or license-problematic?�      | SCA                                       |
| �Did someone commit a recognizable credential?�                    | Secret scanner                            |
| �Does tainted input reach a dangerous sink?�                       | SAST, then AI/human triage                |
| �Is this endpoint missing authorization for this business object?� | AI-assisted review, then human validation |
| �Is the security design acceptable?�                               | Human                                     |
| �Is this fix safe and complete?�                                   | AI can draft; human/SAST/test must verify |
| �Can we enforce this rule across every PR?�                        | SAST/SCA/secret scanner                   |
| �Can we explain the finding and suggest remediation?�              | AI-assisted review                        |

---

# Top 15 Vulnerability Types Best Delegated to AI-Assisted Code Review

> �Delegated to AI� means AI is used for first-pass review, hypothesis generation, explanation, and remediation suggestions. It does **not** mean AI is the final authority.

| Rank | Vulnerability type                                   | Why AI is useful                                                                                                                                  | Caveat                                                                     |
| ---: | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
|    1 | Broken object-level authorization / IDOR             | AI can read routes, controllers, models, and ownership checks together and ask whether `user_id`, tenant, org, or resource ownership is enforced. | Human must validate business rules and exploitability.                     |
|    2 | Missing function-level authorization                 | AI can compare similar endpoints and identify inconsistent middleware, decorators, annotations, guards, or policy checks.                         | SAST may catch known patterns, but AI is better at convention drift.       |
|    3 | Tenant isolation failures                            | AI can reason over naming, data model relationships, query filters, and implied tenant boundaries.                                                | High-risk; requires human review.                                          |
|    4 | Business logic flaws                                 | AI can map intended workflow against code paths, state transitions, and bypass opportunities.                                                     | Humans still win on product intent and abuse cases.                        |
|    5 | Insecure direct state transitions                    | AI can spot transitions like `pending -> approved`, `trial -> paid`, or `user -> admin` without sufficient checks.                                | Requires domain context.                                                   |
|    6 | Inconsistent security controls across similar code   | AI is good at pattern comparison: one handler sanitizes, authorizes, rate-limits, or validates while another does not.                            | Best paired with grep/SAST evidence.                                       |
|    7 | Framework misuse                                     | AI can recognize dangerous or non-idiomatic use of framework APIs, middleware order, route configuration, or security annotations.                | Needs framework-specific prompting and current docs.                       |
|    8 | Insecure error handling and information disclosure   | AI can judge whether error messages expose internal state, tokens, stack traces, SQL errors, or account enumeration clues.                        | SAST can catch some hardcoded patterns.                                    |
|    9 | Unsafe deserialization usage in context              | AI can inspect whether deserialization is reachable from untrusted input and whether allowlists or safe formats are used.                         | SAST should still scan known dangerous APIs.                               |
|   10 | SSRF risk in application-specific URL fetchers       | AI can identify when user-controlled URLs reach HTTP clients, metadata endpoints, webhook fetchers, or import features.                           | SAST taint tracking may be more exhaustive for source-to-sink flow.        |
|   11 | Path traversal in feature context                    | AI can reason about file import/export features, archive extraction, report downloads, and path normalization mistakes.                           | SAST can catch canonical dangerous sinks.                                  |
|   12 | Insecure access-control defaults                     | AI can review whether default roles, default visibility, or fallback behavior fail open.                                                          | Human needs to confirm intended policy.                                    |
|   13 | Security regression in pull requests                 | AI can compare changed code against existing conventions and identify removed checks, changed guards, or weakened validation.                     | Should be backed by tests and SAST gates.                                  |
|   14 | Incomplete remediation                               | AI can compare a patch against the original vulnerability and ask whether all variants and call sites were fixed.                                 | LLM repair studies show generated fixes can be weak; verify independently. |
|   15 | Developer-facing explanation and secure fix drafting | AI can turn low-level findings into actionable review comments, threat explanations, and patch suggestions.                                       | AI-generated patches must be reviewed and tested.                          |

---

# Top 15 Vulnerability Types Best Delegated to Traditional SAST

| Rank | Vulnerability type                                       | Why SAST is the better first delegate                                                                                                      | AI role                                               |
| ---: | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- |
|    1 | SQL injection source-to-sink flow                        | SAST engines can systematically trace tainted input into query sinks. CodeQL explicitly supports data-flow analysis for insecure data use. | Explain and triage.                                   |
|    2 | Command injection                                        | Rule and taint engines are strong for dangerous process execution APIs.                                                                    | Review exploitability and safe replacement.           |
|    3 | XSS in templating or response sinks                      | SAST can enumerate sinks and sanitization APIs across templates and handlers.                                                              | Check contextual encoding correctness.                |
|    4 | Path traversal to filesystem APIs                        | SAST can track untrusted input into file APIs.                                                                                             | Review business context and path allowlist design.    |
|    5 | Unsafe deserialization API usage                         | SAST can reliably flag known dangerous deserialization functions/classes.                                                                  | Determine reachability and safe migration.            |
|    6 | Hardcoded insecure crypto primitives                     | SAST can flag MD5, SHA-1, ECB mode, weak random, and deprecated algorithms.                                                                | Explain risk and replacement.                         |
|    7 | Weak TLS/certificate validation                          | SAST can detect disabled verification, permissive trust managers, and insecure protocol flags.                                             | Check intended environment and compensating controls. |
|    8 | Insecure randomness                                      | SAST can flag predictable PRNGs used in security-sensitive contexts.                                                                       | Determine whether use is security-sensitive.          |
|    9 | XXE parser misconfiguration                              | SAST can detect unsafe XML parser settings.                                                                                                | Confirm parser reachability.                          |
|   10 | LDAP/XPath/template injection                            | SAST can find known sink APIs and taint paths.                                                                                             | Explain exploitability.                               |
|   11 | Open redirect                                            | SAST can trace user-controlled redirect targets.                                                                                           | Decide whether domain allowlist is correct.           |
|   12 | Header injection / response splitting                    | SAST can detect untrusted input in headers.                                                                                                | Review framework protections.                         |
|   13 | Insecure temporary file usage                            | SAST can flag unsafe temp-file patterns and race-prone APIs.                                                                               | Confirm platform impact.                              |
|   14 | Resource leak / missing close in security-sensitive code | Static analysis can find unclosed streams, locks, or resources.                                                                            | Prioritize by impact.                                 |
|   15 | Variant analysis of known vulnerability patterns         | Query-based SAST such as CodeQL is well suited to finding all occurrences of a known bug pattern across a codebase.                        | Help write or refine custom queries.                  |

---

# Top 15 Vulnerability Types Best Delegated to SCA

| Rank | Vulnerability type / risk                | Why SCA wins                                                                            | Human/AI role                            |
| ---: | ---------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------- |
|    1 | Known vulnerable direct dependencies     | SCA maps package/version metadata to advisories and CVEs.                               | Decide upgrade priority.                 |
|    2 | Known vulnerable transitive dependencies | SCA/SBOM tooling is built to walk dependency graphs.                                    | Validate reachability and business risk. |
|    3 | License policy violations                | SCA is designed for license inventory and policy enforcement.                           | Legal/human review.                      |
|    4 | Deprecated or end-of-life packages       | SCA can inventory stale components at scale.                                            | Decide migration path.                   |
|    5 | Dependency confusion risk indicators     | SCA can identify package sources, scopes, and registry metadata.                        | Human validates build process.           |
|    6 | Typosquatting / suspicious packages      | SCA and package-intelligence tools can compare names, age, maintainers, and reputation. | Human confirms intent.                   |
|    7 | Vulnerable container base images         | SCA/container scanners map OS packages and layers to advisories.                        | Human decides rebuild/patch timing.      |
|    8 | SBOM completeness gaps                   | SCA/SBOM tools generate and compare component inventories.                              | Human reviews coverage.                  |
|    9 | Vulnerability exploit maturity           | SCA tools can enrich advisories with severity and exploit data.                         | Human prioritizes actual exposure.       |
|   10 | Package provenance gaps                  | SCA can flag missing signatures, unknown sources, or untrusted registries.              | Human defines policy.                    |
|   11 | Transitive risk concentration            | Graph-based SCA can identify vulnerable components reached through many paths.          | Human decides systemic remediation.      |
|   12 | Runtime dependency drift                 | SCA can compare repository dependencies with deployed service dependencies.             | Human resolves drift.                    |
|   13 | Vulnerable shaded/cloned components      | SCA can help, but standard tools may miss hidden dependencies and shaded clones.        | Human/security research required.        |
|   14 | VEX / exploitability status tracking     | SCA/SBOM workflows can store �affected/not affected� decisions.                         | Human must justify VEX.                  |
|   15 | Open-source policy enforcement in CI     | SCA is repeatable and auditable for build gates.                                        | AI explains developer remediation.       |

---

# Top 15 Vulnerability Types Best Delegated to Secret Scanners

| Rank | Secret type / issue                | Why secret scanners win                                                   | AI role                               |
| ---: | ---------------------------------- | ------------------------------------------------------------------------- | ------------------------------------- |
|    1 | Cloud access keys                  | Provider-specific patterns and validity checks outperform generic review. | Explain rotation steps.               |
|    2 | GitHub/GitLab tokens               | Secret scanners know token formats and can block pushes.                  | Help write incident notes.            |
|    3 | API keys                           | Pattern libraries and custom regex scale across repos.                    | Identify likely code owner.           |
|    4 | OAuth client secrets               | Structured token detection is repeatable.                                 | Explain blast radius.                 |
|    5 | Database passwords                 | Secret scanners catch committed credentials and config leaks.             | Help triage environment exposure.     |
|    6 | Private keys                       | Regex/entropy scanners are strong for PEM blocks and key formats.         | Explain revocation.                   |
|    7 | SSH keys                           | Format-based detection is reliable.                                       | Recommend rotation.                   |
|    8 | JWT signing secrets                | Custom patterns can catch app-specific secret names.                      | Review signing/rotation design.       |
|    9 | Webhook signing secrets            | Secret scanners can match known provider formats.                         | AI maps affected integrations.        |
|   10 | Slack/Teams/Discord tokens         | Provider-specific signatures are scanner-friendly.                        | Draft remediation comments.           |
|   11 | Payment provider keys              | Partner patterns and validity checks help prioritize active keys.         | Human coordinates provider rotation.  |
|   12 | Hardcoded encryption keys          | Scanner detects entropy and naming patterns.                              | Human determines data exposure.       |
|   13 | `.env` and config leaks            | Secret scanners catch known formats across files.                         | AI suggests secure config migration.  |
|   14 | Proprietary internal token formats | Custom regex support is better than ad hoc AI review.                     | AI can help generate custom regex.    |
|   15 | Push-time credential blocking      | Secret scanning push protection prevents introduction before merge.       | AI explains why the push was blocked. |

---

# Top 15 Areas Where Humans Still Win

| Rank | Area                                 | Why humans win                                                                                      |
| ---: | ------------------------------------ | --------------------------------------------------------------------------------------------------- |
|    1 | Threat modeling                      | Humans understand assets, adversaries, trust boundaries, and business impact.                       |
|    2 | Business logic abuse                 | AI can hypothesize, but humans know intended product behavior.                                      |
|    3 | Authorization policy correctness     | Humans decide who should access what, under which conditions.                                       |
|    4 | Multi-tenant risk acceptance         | Tenant isolation failures require business and legal judgment.                                      |
|    5 | Cryptographic design                 | Tools can flag bad APIs, but humans must validate protocol design, key lifecycle, and threat model. |
|    6 | Exploitability validation            | Humans determine whether a finding is actually reachable and impactful.                             |
|    7 | Chained vulnerabilities              | Humans are better at combining low/medium issues into realistic attack paths.                       |
|    8 | Architecture review                  | AI and SAST review code; humans review system boundaries, deployment, and assumptions.              |
|    9 | Security exceptions                  | Humans decide whether risk is acceptable, temporary, or policy-breaking.                            |
|   10 | Production compensating controls     | Humans understand WAFs, IAM, network boundaries, feature flags, and monitoring.                     |
|   11 | Incident response after secret leaks | Scanners detect; humans coordinate rotation, revocation, forensics, and disclosure.                 |
|   12 | Dependency exploitability            | SCA reports known CVEs, but humans decide whether vulnerable code is reachable.                     |
|   13 | Secure design tradeoffs              | Humans balance usability, compatibility, cost, and residual risk.                                   |
|   14 | Reviewing AI-generated fixes         | Evidence shows LLM fixes can be incomplete or unsafe.                                               |
|   15 | Final sign-off for high-risk code    | Humans remain accountable for payment, auth, identity, crypto, data deletion, and admin workflows.  |

---

## Contradictory Evidence and How to Interpret It

### Claim: �LLMs outperform SAST.�

This is sometimes true in narrow benchmarks. The C# benchmark found higher mean F1 scores for GPT-4.1, Mistral Large, and DeepSeek V3 than SonarQube, CodeQL, and Snyk Code on the tested projects. But the same study warned that LLM outputs were noisier and less precise in line/column localization, limiting standalone use in safety-critical audits.

**Interpretation:** Use AI for recall and contextual triage, not as the final gate.

### Claim: �SAST is too noisy to trust.�

Also partly true. The C/C++ secure code review study found that SAST warnings can help prioritize vulnerable functions, but many warnings in vulnerable functions were irrelevant and some vulnerabilities were missed entirely.

**Interpretation:** Use SAST as a deterministic signal, not as a complete vulnerability oracle.

### Claim: �AI can find what scanners miss.�

True for some context-heavy weaknesses, but not reliably at statement-level precision. SecVulEval found low F1 for vulnerable-statement detection with correct reasoning, showing that LLMs still struggle with fine-grained real-world C/C++ vulnerability localization.

**Interpretation:** AI is strongest as a reviewer assistant and hypothesis generator, weakest as a precise, auditable detector.

### Claim: �SCA gives objective dependency truth.�

Only partially. SCA tools vary substantially in what they report, and hidden/shaded/cloned dependencies can create blind spots.

**Interpretation:** Use SCA as the primary dependency control, but validate high-risk dependency exposure with multiple sources, SBOMs, runtime inventory, and human review.

---

## Practical Delegation Model

### 1. Run deterministic scanners first

Every pull request should run:

* SAST for source-to-sink and dangerous API patterns.
* SCA for dependencies, licenses, SBOM, and package risk.
* Secret scanning for credentials and push protection.
* IaC/container scanning where relevant.

This creates the baseline: repeatable, auditable, enforceable, and suitable for CI/CD gates.

### 2. Use AI-assisted review on changed code

AI should review:

* Changed endpoints.
* Authorization-sensitive code.
* Authentication/session code.
* Payment, identity, admin, tenant, and data-access paths.
* Scanner findings that need triage.
* Fixes for known vulnerabilities.
* Similar-code inconsistencies.

The prompt should include the diff, relevant surrounding files, route/middleware configuration, data models, and expected security policy.

### 3. Require human review for high-risk classes

Human security review is mandatory for:

* AuthN/AuthZ changes.
* Multi-tenant access.
* Cryptography.
* Payment and financial logic.
* Data deletion/export.
* Admin workflows.
* Dependency exceptions.
* Secrets exposure.
* Any AI-generated security fix.

### 4. Convert repeated AI findings into deterministic rules

If AI repeatedly finds the same pattern, convert it into:

* A SAST rule.
* A CodeQL query.
* A Semgrep rule.
* A custom secret pattern.
* A CI policy.
* A test case.

This prevents AI from being used as a non-deterministic substitute for a rule that should be enforced.

---

## Recommended Review Workflow

```text
1. Developer opens PR
2. CI runs SAST + SCA + secret scanning
3. AI reviews the diff and scanner output
4. AI labels findings:
   - likely true positive
   - needs human review
   - likely false positive
   - missing test
   - unsafe fix
5. Human reviewer validates high-risk findings
6. Security owner approves exceptions
7. Repeated patterns become rules/tests
8. Metrics are collected by vulnerability type and detection source
```

---

## Decision Matrix

| Vulnerability class    | AI-assisted review |   SAST |  SCA | Secret scanner |  Human |
| ---------------------- | -----------------: | -----: | ---: | -------------: | -----: |
| IDOR / BOLA            |               High | Medium |  Low |            Low |   High |
| Missing authorization  |               High | Medium |  Low |            Low |   High |
| Business logic flaw    |               High |    Low |  Low |            Low |   High |
| Tenant isolation       |               High | Medium |  Low |            Low |   High |
| SQL injection          |             Medium |   High |  Low |            Low | Medium |
| XSS                    |             Medium |   High |  Low |            Low | Medium |
| Command injection      |             Medium |   High |  Low |            Low | Medium |
| Path traversal         |             Medium |   High |  Low |            Low | Medium |
| SSRF                   |               High |   High |  Low |            Low |   High |
| Unsafe deserialization |             Medium |   High |  Low |            Low | Medium |
| Weak crypto API        |             Medium |   High |  Low |            Low |   High |
| Crypto design flaw     |             Medium | Medium |  Low |            Low |   High |
| Vulnerable dependency  |                Low |    Low | High |            Low | Medium |
| License risk           |                Low |    Low | High |            Low |   High |
| Hardcoded secret       |                Low | Medium |  Low |           High | Medium |
| Secret leak incident   |                Low |    Low |  Low |           High |   High |
| Insecure generated fix |               High | Medium |  Low |            Low |   High |

---

## Operating Principles

1. **AI is best for context, not certainty.** Use it to reason about intent, compare patterns, explain findings, and propose fixes.
2. **SAST is best for repeatable source-code rules.** Use it for taint tracking, dangerous APIs, and variant analysis.
3. **SCA is best for dependency truth, but not perfect truth.** Use it for known vulnerable packages, licenses, SBOMs, and transitive exposure, but validate high-risk cases.
4. **Secret scanners are best for credentials.** Use provider patterns, push protection, custom regex, and validity checks.
5. **Humans own risk decisions.** Humans decide exploitability, business impact, exceptions, and architectural correctness.
6. **Convert lessons into rules.** AI findings should harden the pipeline over time, not remain one-off observations.
7. **Never trust AI-generated security patches without independent validation.** Evidence shows LLMs can detect issues better than they repair them.

---

## Whitepaper Conclusion

The defensible model is not �AI versus SAST.� It is **AI plus SAST/SCA/secret scanning plus human judgment**, with clear delegation boundaries.

AI-assisted code review is most valuable where scanners lack product context: authorization, tenant isolation, business logic, insecure workflows, framework misuse, inconsistent controls, and remediation review. Traditional scanners remain superior where detection is structured, enumerable, and policy-driven: tainted source-to-sink flows, dangerous APIs, dependency CVEs, licenses, SBOM inventory, and hardcoded secrets. Humans remain essential wherever risk depends on intent, architecture, exploitability, compensating controls, and accountability.

The strongest practical recommendation is:

> Use scanners as mandatory gates, AI as a contextual reviewer, and humans as the final authority for high-risk security decisions.

## References and Verification Links

> Use this section as the whitepaper reference appendix. Each reference includes the claim it supports so reviewers can verify the delegation model directly.

### 1. LLMs vs Static Code Analysis Tools: Systematic Benchmark

**Reference:** *Large Language Models Versus Static Code Analysis Tools: A Systematic Benchmark for Vulnerability Detection*
**Link:** https://arxiv.org/abs/2508.04448
**Supports:**

* Direct comparison between LLMs and traditional SAST tools.
* Compared GPT-4.1, Mistral Large, and DeepSeek V3 against SonarQube, CodeQL, and Snyk Code.
* Supports the claim that LLMs can achieve strong vulnerability-detection performance in some benchmark settings.
* Also supports the caution that LLMs may produce noisier output and weaker precise localization than deterministic tooling.

**Use in whitepaper:**
Use this as the main evidence for the statement: �AI-assisted code review can outperform traditional SAST in some benchmark settings, especially on recall, but should not be treated as a standalone authoritative scanner.�

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
Use this to justify the rule: �AI can draft fixes, but humans and tests must verify them.�

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

**Reference:** OWASP � *Source Code Analysis Tools*
**Link:** https://owasp.org/www-community/Source_Code_Analysis_Tools
**Supports:**

* Defines SAST/source-code analysis tools.
* Supports SAST as a method for analyzing source code or compiled code to find security flaws.
* Supports the inclusion of SAST in IDE and CI/CD workflows.

**Use in whitepaper:**
Use this as the authoritative baseline definition of SAST and why it belongs in secure development pipelines.

---

### 6. CodeQL Data Flow Analysis Documentation

**Reference:** GitHub CodeQL � *About Data Flow Analysis*
**Link:** https://codeql.github.com/docs/writing-codeql-queries/about-data-flow-analysis/
**Supports:**

* CodeQL security queries use data-flow analysis.
* Data-flow analysis can identify insecure data use, dangerous arguments passed to functions, and sensitive-data leaks.
* Supports delegating source-to-sink vulnerability classes to SAST/CodeQL.

**Use in whitepaper:**
Use this to justify assigning SQL injection, command injection, XSS, path traversal, SSRF source-to-sink paths, and sensitive-data leaks to traditional SAST first.

---

### 7. GitHub Secret Scanning: Concept Documentation

**Reference:** GitHub Docs � *Secret Scanning*
**Link:** https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
**Supports:**

* Secret scanning detects credentials committed to repositories.
* Supports provider patterns and automated scanning workflows.
* Supports assigning hardcoded credentials, API keys, cloud keys, and tokens to secret scanners rather than AI.

**Use in whitepaper:**
Use this to support the claim that secret detection should be scanner-first because token patterns and provider integrations are deterministic and scalable.

---

### 8. GitHub Secret Scanning Validity Checks

**Reference:** GitHub Docs � *Validity Checks*
**Link:** https://docs.github.com/en/code-security/concepts/secret-security/validity-checks
**Supports:**

* Validity checks verify whether a detected secret is still active and exploitable.
* Supports prioritizing active secrets over inactive or already-rotated credentials.
* Strengthens the case that secret scanners outperform AI for credential detection and triage.

**Use in whitepaper:**
Use this to justify: �Secret scanners win because they can identify, classify, and sometimes validate real active credentials.�

---

### 9. Datadog Software Composition Analysis Documentation

**Reference:** Datadog Docs � *Software Composition Analysis*
**Link:** https://docs.datadoghq.com/security/code_security/software_composition_analysis/
**Supports:**

* SCA detects open-source libraries in repositories and running services.
* SCA provides visibility into library vulnerabilities and license management.
* Supports assigning known vulnerable dependencies and license issues to SCA.

**Use in whitepaper:**
Use this as an operational definition of SCA and why dependency and license risks should be delegated to SCA first.

---

### 10. OWASP Dependency-Check

**Reference:** OWASP � *Dependency-Check*
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
Use this to qualify the SCA delegation model: �SCA is best for declared dependencies, but hidden/shaded/cloned dependencies may require additional analysis.�

---

### 13. Hidden Dependencies and SBOM-Based SCA

**Reference:** *Hidden Dependencies and Component Variants in SBOM-Based Software Composition Analysis*
**Link:** https://arxiv.org/abs/2604.21278
**Supports:**

* SBOM-based analysis depends on accurate component identity and dependency representation.
* Hidden code-level dependencies and component variants can cause inconsistent vulnerability reporting.
* Supports treating SBOM/SCA results as important but not infallible.

**Use in whitepaper:**
Use this to support the statement: �SBOMs and SCA are necessary for dependency governance, but they do not eliminate the need for human validation in complex supply-chain cases.�

---

## Mapping References to Delegation Claims

| Delegation claim                                                                   | Best supporting references |
| ---------------------------------------------------------------------------------- | -------------------------- |
| AI is useful for contextual vulnerability review but should not replace scanners   | References 1, 2, 3         |
| AI can outperform SAST in some benchmark settings                                  | Reference 1                |
| AI struggles with precise vulnerable-statement localization                        | Reference 2                |
| AI-generated fixes require human validation                                        | Reference 3                |
| SAST is useful but noisy and incomplete                                            | Reference 4                |
| SAST is appropriate for source-code and compiled-code flaw detection               | Reference 5                |
| SAST/CodeQL is especially appropriate for source-to-sink data-flow vulnerabilities | Reference 6                |
| Secret scanning should be scanner-first, not AI-first                              | References 7, 8            |
| SCA should handle known vulnerable dependencies and license risks                  | References 9, 10           |
| SCA output can vary across tools                                                   | Reference 11               |
| SCA can miss hidden, shaded, or cloned dependencies                                | References 12, 13          |

---

## Suggested Whitepaper Citation Language

Use this wording in the whitepaper body:

> The evidence does not support a clean replacement model where AI substitutes for SAST, SCA, or secret scanning. Instead, current research supports a hybrid model. LLMs can provide strong contextual review and may outperform some static tools in certain benchmark settings, but they also struggle with precise vulnerable-statement localization and reliable repair. Traditional SAST remains useful for repeatable source-to-sink and dangerous-API checks, while SCA and secret scanners remain the correct first-line controls for dependency and credential risks. Human review remains necessary for exploitability, business logic, architecture, and risk acceptance.
