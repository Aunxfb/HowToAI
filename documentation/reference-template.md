---
title: <Title: Concise, Descriptive>
description: <One or two sentences. What this covers and who it is for. Max 280 chars.>
status: <active | draft | deprecated | archived>
tags: [<keyword1>, <keyword2>, <keyword3>]
last_verified: <YYYY-MM-DD>
layer: <hot | warm | cold>  # classify by loading intent; sizes are guidance, not limits
applies_to: <optional: platform, component, or concept>
---

# <Title — must match frontmatter title>

> <Optional one-line summary or key takeaway. Not a replacement for description.>

## Overview

2-4 sentences. What this document covers, who it is for, and why it exists. Do not include tutorial content or step-by-step instructions here.

**Audience:** <Who should read this — human contributors, AI agents, both?>

## Background

Optional section. Prerequisites, terminology definitions, or context the reader needs before approaching the main content. Omit if the document is self-contained.

- **Key terms:** Define acronyms and jargon on first use.
- **Prerequisites:** Any prior knowledge, tools, or setup assumed.
- **Context:** Why this topic matters in the broader system.

---

## Content Section

Replace with stable heading names from the standard set. Use subsections as needed but keep the structure predictable.

### Subsection A

Bullet points for enumerations. Use active voice. Be specific.

- Concrete rule or observation
- Another fact with specific detail
- Link to deeper reference if this item needs expansion

### Subsection B

Numbered lists only for sequential steps:

1. First do this
2. Then do that
3. Verify with this command

### Patterns

Recommended approaches. Include labeled examples.

**[Copy-Safe]** Ready-to-use pattern with imports, error handling, and test coverage.

```python
def example_function(param: str) -> bool:
    """Docstring explaining behavior."""
    return bool(param)
```

**[Conceptual]** Illustrative only — adapt to your context.

```python
# This shows the idea, not production code
process(data)
```

### Anti-Patterns

Approaches to avoid and why.

- **Don't do X because:** reason
- **Don't do Y because:** reason

### Validation

Commands or checks that prove the content works.

```bash
# Command to verify
some-command --flag
# Expected: specific output or exit code
```

---

## Related Documents

Links to other files in this repository. Use relative paths and descriptive text.

- [Reference Standards](../documentation/reference-standards.md) — the conventions this template follows
- [<Other File>](../<path>/<file>.md) — <1-line description of what it covers>

## References

External sources, citations, or official documentation links. Use full URLs.

- <Author or Organization>, "<Title>", <URL>, <access date if dynamic>
- <Specification or standard link>

---

*Last verified: <YYYY-MM-DD> — update this date when content is reviewed or changed.*
