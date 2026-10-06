# Intent-Driven Training Plugin

A small training/process plugin for Intent-Driven Engineering.

Core loop:

**Intent -> smallest safe delta -> validation -> evidence -> refine only when evidence says so**

## Included commands

- `/setup-feature` - create the smallest useful feature workspace
- `/review-intent` - check an intent for outcome, inputs, outputs, success criteria, and unnecessary constraints
- `/run-feature` - implement the smallest safe delta
- `/prove-feature` - gather running evidence against success criteria
- `/simplify` - remove unnecessary implementation detail and constraints
- `/context-map` - identify the minimum context needed for the work
- `/model-gate` - run a preflight before implementation and recommend the minimum sufficient model tier

## Included skills

- **Context Discipline** - load only what the task needs
- **Feature Workflow** - keep work centered on intent, evidence, and progressive refinement
- **ModelGate** - choose the minimum sufficient intelligence before implementation

## ModelGate principle

Do not spend more intelligence than the work requires.

The routing order is:

1. Deterministic tooling / no LLM
2. Fast / low-cost model
3. Standard engineering model
4. Reasoning / frontier model

ModelGate does not call another model API. It uses the model already active in the IDE to classify four factors, then a tiny local deterministic script calculates the recommendation.
