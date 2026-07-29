# LLM Budget-Friendly Design

> A good AI framework continuously moves deterministic work away from the LLM until the only thing left is making decisions under uncertainty.

---

# 1. Purpose

This document describes how to design efficient, reliable, and scalable AI systems that work well with:

- local LLMs
- small models (1B - 13B parameters)
- limited context windows
- limited reasoning capacity
- expensive inference
- long-running autonomous workflows

The objective is not to make the LLM do more.

The objective is:

> Make the LLM responsible only for tasks that genuinely require intelligence.

Everything else should be handled by deterministic systems.

---

# 2. Core Mental Model

An LLM is not a complete application.

An LLM is a reasoning component.

It should not be treated as:

- a database
- a workflow engine
- a parser
- a serializer
- a file manager
- a validator
- a calculator
- a compiler
- a memory system

Those are software responsibilities.

The LLM is best used for:

- interpretation
- planning
- judgement
- ambiguity resolution
- risk analysis
- creative generation
- tradeoff evaluation

A reliable AI system looks like:

```

```
             User

              |

              v

        Workflow Engine

              |

    +---------+---------+

    |                   |

    v                   v
```

Deterministic          LLM

Runtime                Reasoning

Scripts                Decisions

Validators             Analysis

Serializers

```
    |

    v
```

Artifact Storage

```

The LLM is not the system.

The LLM is one component inside the system.

---

# 2.5 Design Balance — Determinism Is a Tool, Not a Goal

The purpose of determinism is to reduce unnecessary cognitive load, not to eliminate intelligence or create rigid workflows.

## Bad implementation

```
Everything is a state machine.
Everything is a script.
LLM only fills forms.
```

This produces a glorified automation engine.

## Good implementation

```
Deterministic system:
- controls execution
- stores state
- validates results

LLM:
- handles ambiguity
- makes decisions
- explores options
```

The goal is not less AI.

The goal is better allocation of AI.

---

# 3. First Principle: Deterministic Work Belongs in Software

## Rule

> If software can perform a task reliably, do not spend AI tokens performing it.

Examples:

## Software responsibilities

- JSON generation
- YAML generation
- XML generation
- parsing
- sorting
- searching
- filtering
- validation
- calculations
- file operations
- API requests
- authentication
- retries
- formatting
- compression
- conversion
- testing

## LLM responsibilities

- deciding what matters
- interpreting unclear information
- evaluating options
- reasoning about risks
- designing solutions
- resolving ambiguity

---

## Example

Bad:

```

Read these 500 files and summarize the project structure.

```

Better:

```

Script:

scan_repository()

Output:

repository_map.json

LLM:

Analyze repository_map.json

```

The LLM receives information.

It does not perform mechanical extraction.

---

# 4. Reasoning Is the Scarce Resource

Tokens are not the only constraint.

The most limited resource is reasoning capacity.

A small model can fail when forced to handle:

- instructions
- formatting
- memory
- planning
- syntax
- constraints
- decision making

at the same time.

Example:

```

Generate valid JSON.
Remember 20 rules.
Analyze security risks.
Create a deployment plan.
Explain your reasoning.

```

The model is not necessarily bad.

The workload is badly designed.

---

## Design goal

Remove everything that does not require intelligence.

The LLM should spend its capacity on:

- uncertainty
- judgement
- decisions

---

# 5. The LLM Should Generate Meaning, Not Syntax

One of the biggest sources of wasted tokens and failures is asking LLMs to manually produce structured formats.

Examples:

- JSON
- YAML
- XML
- CSV
- SQL
- HTML
- Markdown tables

These are serialization problems.

Software already solves serialization.

---

## Bad

```

Generate:

{
"name":"Alice",
"age":30,
"active":true
}

```

The model must handle:

- brackets
- quotes
- commas
- escaping
- schema compliance

None of this requires intelligence.

---

## Better

LLM output:

```

SET name Alice
SET age 30
SET active true

```

Software converts:

```

semantic data

```
  |

  v
```

JSON/YAML/database/API

```

The LLM provides meaning.

Software provides correctness.

---

# 6. Use a Serialization Layer

Never rely on prompting the model:

- "always output valid JSON"
- "remember the schema"
- "escape strings correctly"

Move this into software.

Example:

```

semantic_state.txt

```
    |

    v
```

serializer

```
    |

    v
```

json
yaml
toml
xml
csv

```

The model should not care about the final format.

---

# 7. The Framework Owns State, Not the LLM

The LLM should never be responsible for remembering:

- workflow position
- completed steps
- previous sessions
- retries
- failures
- checkpoints

Those are framework concerns.

---

The framework owns:

```

current phase

completed phases

artifact locations

permissions

retry count

failure state

```

The LLM owns:

```

analysis

hypotheses

recommendations

tradeoffs

decisions

```

---

## Bad

```

AI:
"I think we finished design and should start implementation."

```

---

## Good

```

Framework:

Current phase:
implementation

AI:

Determine implementation strategy.

```

---

# 8. Complex Workflows Have Deterministic State Boundaries

Multi-phase AI systems should have deterministic state boundaries, while allowing intelligent decisions inside those boundaries.

Example:

```

requirements_pending

```
    |

    v
```

requirements_complete

```
    |

    v
```

design_pending

```
    |

    v
```

design_complete

```
    |

    v
```

implementation_pending

```

Each transition has:

- required inputs
- validation rules
- outputs
- failure states

---

The LLM operates inside a state.

It does not manage the state machine.

## Framework role

The framework controls:

```
Can this transition happen?
```

## LLM role

The LLM decides:

```
Which valid transition is best?
```

Example:

Bad:

```
STATE_A
  |
  | always
  v
STATE_B
```

Everything is hardcoded.

Better:

```
STATE_A

LLM decides:
- continue
- request more information
- retry
- escalate

Framework validates transition.
```

---

# 9. Externalize Memory

Conversation is temporary.

Files are persistent.

Do not rely on:

- previous chat messages
- hidden memory
- model recall

Store important information externally.

Example:

```

workspace/

```
state/

    workflow.json

    phase.json


artifacts/

    analysis.md

    decisions.md

    results.md


logs/
```

```

---

Benefits:

- resumable
- debuggable
- versionable
- inspectable
- transferable between models

---

# 10. File-Based State Passing

Agents should communicate through artifacts.

Not conversations.

---

Bad:

```

Agent A tells Agent B:

"Here is what happened earlier..."

```

---

Good:

```

Agent A

writes:

research.md

Agent B

reads:

research.md

```

---

Benefits:

- no hidden context
- easy recovery
- model replacement
- auditing
- parallel execution

---

# 11. Split by Context Boundaries, Not Task Names

The important unit is not the agent.

The important unit is the context boundary.

## Bad splitting

```

database_agent

api_agent

frontend_agent

backend_agent
```

when all need the same architecture context.

## Good splitting

```

requirements_phase

implementation_phase

security_review_phase
```

because each has different:

- information
- goals
- evaluation criteria

## The right question

Not:

> "Can this be another agent?"

But:

> "Does this have a different context boundary?"

---

# 12. Skills Are APIs, Not Documentation

A skill is a capability interface.

It should expose:

- purpose
- inputs
- outputs
- constraints

Nothing more.

---

Bad:

```

This skill carefully analyzes files by recursively traversing...

```

---

Good:

```

search_files(path, pattern)

Returns:

matching file paths

Side effects:

none

```

---

The model needs to know:

"When should I use this?"

Not:

"How does this work internally?"

## Finding the right abstraction level

Skills should be high-level enough to reduce planning, but low-level enough to preserve control.

Too low:

```
read_file()
write_file()
execute_shell()
```

The model must orchestrate everything.

Too high:

```
solve_problem()
```

The system becomes opaque.

The sweet spot:

```
analyze_repository()
generate_report()
run_security_scan()
prepare_release()
```

---

# 13. Skills Should Hide Complexity

Small models perform better when complexity is hidden.

---

Bad:

```

read_file()

parse_file()

validate_file()

transform_file()

save_file()

```

---

Better:

```

process_document()

```

---

Bad:

```

download()

extract()

verify()

move()

configure()

```

---

Better:

```

install_package()

```

---

Good skills remove decisions from the model.

## Observability requirement

Skills hide complexity from the LLM, but never hide execution details from the system.

A skill should expose:

```
result
metadata
artifacts
logs
errors
```

Bad:

```
compile_project()

Success.
```

Good:

```
compile_project()

status: success
warnings: 3
artifact: build/output.bin
duration: 32s
```

---

# 14. AI-Friendly Interfaces

Interfaces should be designed for machines.

Not only humans.

---

Bad:

```

final_version_latest_REAL.md

```

---

Good:

```

result.md

```

---

Bad:

```

The operation completed successfully.

```

---

Good:

```

STATUS=SUCCESS
FILE=/output/result.txt

```

---

Predictability is more valuable than readability.

---

# 15. Keep Prompts Minimal

Every instruction consumes attention.

Avoid:

- personality text
- unnecessary explanations
- repeated rules
- motivational language
- excessive examples

---

Prefer:

```

Read task.md.

Create plan.md.

Do not modify source files.

Return DONE.

```

---

Every sentence should change behavior.

---

# 16. Put Rules in Software

Prompt rules are suggestions.

Software rules are guarantees.

---

Bad:

```

Never overwrite files.

```

---

Better:

```

safe_write()

```

---

Bad:

```

Always validate JSON.

```

---

Better:

```

schema_validator()

```

---

The best instruction is a system that prevents mistakes.

---

# 17. Design for Weak Models First

Assume:

- small context
- weak planning
- occasional hallucination
- poor syntax generation
- limited memory

If a design works on a 3B model, stronger models become upgrades.

Not requirements.

## Model capability scaling

The architecture should degrade gracefully downward and improve gracefully upward.

Same workflow:

```
3B model:
  simple classification

13B model:
  basic planning

70B model:
  complex reasoning
```

The architecture stays unchanged.

Only the reasoning quality changes.

---

# 18. Separate Workflow State and Reasoning State

Two different types of information exist.

---

## Framework State

Deterministic.

Examples:

```

phase
status
retry_count
artifacts
permissions

```

---

## AI Reasoning State

Probabilistic.

Examples:

```

hypotheses
ideas
tradeoffs
recommendations
analysis

```

---

Never mix them.

The framework controls execution.

The LLM provides intelligence.

---

# 19. Make Everything Recoverable

A good AI workflow survives:

- crashes
- context loss
- session interruption
- model changes

Important information must exist outside the conversation.

---

Required:

```

checkpoints

artifacts

logs

state files

```

---

# 20. Spend Tokens Only Where They Matter

High-value token usage:

- reasoning
- planning
- architecture
- evaluation
- risk analysis

Low-value token usage:

- formatting
- syntax
- copying
- validation
- conversion

Move low-value work into software.

---

# 21. Framework Complexity Budget

A common failure mode:

```
Need an AI assistant
?
Build:
  agent framework
  plugin architecture
  workflow engine
  memory layer
  skill registry
  monitoring system
```

before solving the actual problem.

## Rule

```
One working workflow first.
Extract abstractions second.
Build framework third.
```

The framework itself also needs a budget.

---

# 22. AI Actions Should Prefer Reversible Operations

LLMs are probabilistic.

Therefore workflows should minimize irreversible mistakes.

## Prefer

```
analyze
preview
approve
apply
verify
```

## Over

```
decide
execute
```

## Bad

```
delete_user()
```

## Better

```
disable_user()
review()
delete()
```

## Bad

```
rewrite_database()
```

## Better

```
generate_migration()
validate()
apply()
```

---

# 23. Final Design Principle

> A good architecture makes the model's work smaller but more important.

> Build deterministic systems that create a safe operating environment for probabilistic intelligence. Give the LLM maximum freedom where judgement is required, and minimum responsibility where correctness can be guaranteed.

```

Less execution.
More judgement.

Less memory.
More state.

Less syntax.
More meaning.

Less prompting.
More engineering.

```
