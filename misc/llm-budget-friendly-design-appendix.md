# LLM Budget-Friendly Design Appendix

This appendix converts the principles from `llm_budget_friendly_design.md` into practical engineering procedures.

It defines:

- how to design AI frameworks
- how to decide what becomes a script, skill, or agent
- how to design phases and state machines
- how to define agent contracts
- how to define skill interfaces
- how to structure an AI runtime

The goal is:

> Given any AI task, systematically determine where intelligence belongs and where software should take over.

---

# Part 2 — AI Framework Design Procedure

---

# 1. Design the State Machine First

The most common mistake in AI framework design is starting with:

> "What should my agent prompt say?"

Do not start there.

Start with:

> "What states exist, and how does information move between them?"

---

A workflow should first be represented as:

```

State A

```
|
| transition

v
```

State B

```
|
| transition

v
```

State C

```

Each state defines:

- what information exists
- what actions are allowed
- what outputs are required
- what determines completion

---

Example:

Software development workflow:

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

architecture_pending

```
    |

    v
```

architecture_complete

```
    |

    v
```

implementation_pending

```
    |

    v
```

testing_complete

```

The workflow engine manages movement.

The LLM only helps complete individual states.

---

# 2. Task Decomposition Procedure

Given a task:

Example:

> Build an AI security review assistant.

Do not immediately create:

```

security_agent

```

First decompose.

Ask:

```

What information must be collected?

What transformations are deterministic?

What decisions require judgement?

What outputs are needed?

```

---

Example decomposition:

```

Repository scanning

```
|
v
```

Script

```
|
v
```

Dependency extraction

```
|
v
```

Script

```
|
v
```

Risk interpretation

```
|
v
```

LLM

```
|
v
```

Report generation

```
|
v
```

Script

```

---

# 3. Classify Every Operation

Every operation belongs to one of three categories.

---

# Category A — Deterministic

No AI required.

Characteristics:

- same input produces same output
- rules are known
- correctness can be tested

Examples:

```

parse JSON

calculate hash

sort files

validate schema

convert formats

generate reports

run tests

```

Implementation:

```

script
library
database
API

```

---

# Category B — Capability

Requires external systems.

Examples:

```

search internet

read database

execute command

access repository

send email

```

Implementation:

```

skill
tool
service

```

---

# Category C — Reasoning

Requires intelligence.

Examples:

```

Which design is better?

Is this a security risk?

What caused this failure?

What should we prioritize?

```

Implementation:

```

LLM agent

```

---

# 4. The LLM Eligibility Test

Before using an LLM, ask:

```

Does this task require:

* interpretation?
* uncertainty handling?
* judgement?
* tradeoff analysis?
* creativity?

```

If no:

Use software.

---

Examples:

## Should use LLM

```

Evaluate whether this architecture is maintainable.

```

## Should not use LLM

```

Convert YAML to JSON.

```

---

# 5. Create the State Model

Before creating agents, define:

```

What must survive between sessions?

```

Typical state:

```

workflow_state

phase_state

decision_history

artifacts

logs

checkpoints

```

---

Recommended layout:

```

workspace/

```
state/

    workflow.json

    current_phase.json


inputs/

artifacts/

outputs/

logs/
```

```

---

# 6. Define Phase Contracts

A phase is a bounded unit of work.

Every phase defines:

```

Input

Process

Output

Validation

Next State

```

Example:

```

Phase:

Threat Analysis

Input:

architecture.md

Process:

Analyze security risks

Output:

threats.md

Validation:

threats.md exists

Next:

review_pending

```

---

# 7. Design Skills

A skill exists when:

- a capability is reusable
- external access is required
- deterministic execution is preferred

---

Ask:

```

Can this be a script?

Can this be reused?

Does this need AI?

```

---

Example:

Bad:

```

general_file_skill

```

Too broad.

Better:

```

read_file()

search_files()

write_file()

```

---

# 8. Design Agents

Create an agent only when reasoning is required.

An agent needs:

```

Purpose

Inputs

Allowed skills

Decision responsibility

Outputs

Completion condition

```

---

An agent should not:

- manage workflow state
- format files
- validate schemas
- perform mechanical operations

---

# 9. Design Prompts Last

A prompt is an adapter.

It should not contain the entire system.

A good prompt contains:

```

Current state

Goal

Available artifacts

Available skills

Output requirement

```

---

Example:

```

Current phase:

threat_review

Read:

architecture.md

Create:

threats.md

Use:

security_analysis skill

```

---

# 10. Evaluate the Architecture

Before deployment:

Ask:

```

Can the model be smaller?

Can more work become code?

Can context be reduced?

Can state be clearer?

Can skills become higher level?

Can failures recover automatically?

```

---

# 11. Do Not Overengineer Checkpoint

Before creating an agent, skill, or phase, ask:

```

Is this abstraction solving a repeated problem?

Does this reduce complexity?

Would the system be simpler without it?

```

---

# Part 3 — Templates

---

# 1. Phase Template

```yaml
phase:

  name:

  purpose:


  entry_state:


  exit_state:


  inputs:

    -


  outputs:

    -


  required_skills:

    -


  agent:


  validation:

    -


  failure_state:


  retry_policy:
```

---

Example:

```yaml
phase:

  name: security_review

  purpose:
    Identify security risks.


  entry_state:
    architecture_complete


  exit_state:
    security_review_complete


  inputs:

    - architecture.md

    - dependencies.json


  outputs:

    - threats.md

    - risk.json


  required_skills:

    - dependency_scan


  agent:
    threat_reviewer


  validation:

    - risk.json exists

    - schema valid


  failure_state:

    security_review_failed
```

---

# 2. Agent Template

```yaml
agent:

  name:


  purpose:


  reasoning_required:

    true


  inputs:

    -


  outputs:

    -


  skills:

    -


  decisions:

    -


  constraints:

    -


  context:


    required_files:

      -


    forbidden_files:

      -


  success_condition:


  failure_condition:
```

---

Example:

```yaml
agent:

  name:
    architecture_reviewer


  purpose:
    Evaluate system design.


  reasoning_required:
    true


  inputs:

    - architecture.md


  outputs:

    - review.md


  decisions:

    - identify tradeoffs

    - recommend improvements


  success_condition:

    review.md created
```

---

# 3. Skill Template

```yaml
skill:

  name:


  purpose:


  deterministic:


  inputs:


  outputs:


  side_effects:


  errors:


  cost:


  examples:
```

---

Example:

```yaml
skill:

  name:
    search_repository


  purpose:
    Find files matching a pattern.


  deterministic:
    true


  inputs:

    path:
      string


    pattern:
      string


  outputs:

    files:
      list[string]


  side_effects:
    none


  errors:

    invalid_path

    permission_denied
```

---

# 4. Workflow State Template

```yaml
workflow:

  id:


  current_phase:


  status:


  completed_phases:


  artifacts:


  errors:


  next_action:
```

---

Example:

```yaml
workflow:

  id:
    project_alpha


  current_phase:
    implementation


  status:
    running


  completed_phases:

    - requirements

    - architecture


  artifacts:

    - design.md

    - api_spec.md


  next_action:

    run_tests
```

---

# 5. Decision Template

```yaml
decision:

  question:

  options:

  constraints:

  chosen:

  reasoning:

  confidence:

  reversible:
```

---

# 6. Skill Quality Checklist

```
Does it reduce reasoning burden?

Does it have deterministic behavior?

Does it expose useful metadata?

Can it fail safely?

Can it be tested without an LLM?
```

---

# Part 4 — Reference Architecture

---

# 1. System Overview

A budget-friendly AI framework:

```
                         User

                          |

                          v

                  Workflow Controller

                          |

                          v

                 State Machine Engine

                          |

          +---------------+---------------+

          |                               |

          v                               v

 Deterministic Runtime                LLM

 Scripts                              Reasoning

 Validators                           Decisions

 Serializers                          Analysis

          |                               |

          +---------------+---------------+

                          |

                          v

                 Artifact Storage
```

---

# 2. Recommended Project Structure

```
ai_framework/


    agents/

        planner.yaml

        reviewer.yaml


    phases/

        requirements.yaml

        design.yaml

        implementation.yaml


    skills/

        filesystem.yaml

        search.yaml

        compiler.yaml


    scripts/

        serializer.py

        validator.py


    state/

        workflow.json


    workspace/

        inputs/

        outputs/

        artifacts/


    prompts/

        system.md


    logs/
```

---

# 3. Runtime Loop

The runtime should look like:

```
while workflow.running:


    load_state()


    determine_current_phase()


    validate_inputs()


    execute_deterministic_steps()


    invoke_LLM_if_required()


    validate_outputs()


    save_artifacts()


    update_state()


    transition_phase()
```

---

The LLM is one operation inside the workflow.

Not the workflow itself.

---

# 4. Context Loading Strategy

Never:

```
Load entire history.
```

Never:

```
Load entire repository.
```

Prefer:

```
workflow state

+

current phase

+

required artifacts

+

skill results
```

---

Context should be assembled.

Not accumulated.

---

# 5. Multi-Agent Communication

Agents communicate through artifacts.

Example:

```
research_agent

        |

        v

research.md


        |

        v


analysis_agent


        |

        v


analysis.md
```

Not:

```
Agent A explains everything to Agent B through conversation.
```

---

# 6. Failure Handling

Every phase must define:

```
failure state

retry policy

rollback method

human escalation point
```

---

Example:

```
implementation_failed

        |

        +---- retry

        |

        +---- request_review

        |

        +---- rollback
```

---

# 7. Model Replacement

The framework should survive model changes.

Example:

```
Local 7B model

        |

same framework

        |

Cloud 70B model
```

The architecture should not depend on a specific model.

A better model improves decisions.

It does not repair bad design.

---

# 8. Final Architecture Rule

When designing an AI framework:

1. Define states.
2. Define transitions.
3. Move deterministic work into software.
4. Create artifacts.
5. Create skills.
6. Create agents.
7. Write prompts last.
8. Measure failures.
9. Reduce complexity.

The best AI systems are not giant autonomous agents.

They are deterministic systems that use AI exactly where deterministic software cannot replace judgement.

---

# 9. Human Approval Boundary

Not everything should be autonomous.

Architecture:

```
                 Workflow Engine

                       |

                Decision Point

                       |

          +-------------+-------------+

          |                           |

          v                           v

       Auto Execute             Human Review
```

Define for each phase whether a human decision gate is required before proceeding.
