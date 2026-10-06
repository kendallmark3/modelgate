# ModelGate and the Intent-Driven Training plugin

A Claude Code plugin that keeps AI-assisted feature work small, evidence-based, and no more expensive than it needs to be.

It gives you two things:

- **ModelGate**: a preflight check that tells you the cheapest model tier that can do the job, before you spend tokens on it. Sometimes the answer is "no model at all".
- **A lean feature loop**: six short commands that take a feature from intent to proof without inventing scope along the way.

## Why use it

**Most work does not need the strongest model.** Renaming a config key and redesigning an auth flow are different jobs, but teams tend to run both on whatever model is selected. ModelGate makes the choice explicit and takes about a minute.

**The recommendation is repeatable.** The model only scores four factors from 0 to 3. A small local script turns those scores into a tier, so the same scores always give the same answer, and you can read exactly why in 30 lines of Python.

**Nothing leaves your machine.** ModelGate calls no extra APIs, does no web research, and benchmarks nothing. It uses the model already running in your session plus the Python standard library.

**It is vendor-neutral.** The rubric talks about tiers, not products. You map tiers to the models your team is allowed to use, in one file.

**The workflow resists scope creep.** Every command pushes the same way: state what must be true, build the smallest change that makes it true, then prove it with running evidence instead of prose.

## Install

You need [Claude Code](https://claude.com/claude-code) and `python3` on your PATH.

Inside Claude Code:

```
/plugin marketplace add kendallmark3/modelgate
/plugin install intent-driven-training@intent-driven-training
```

To try it without installing, clone the repo and start Claude Code with:

```bash
claude --plugin-dir ./plugins/intent-driven-training
```

## Using ModelGate

Write down what you want to build, as a plan or an intent file, then run:

```
/intent-driven-training:model-gate INTENT.md
```

Claude reads only enough context to score the work, runs the scorer, and replies in a fixed format. This is real output for an intent that renames one config key across three files:

```text
MODEL GATE
Recommended tier: NO_LLM
Confidence: High

Why:
- Mechanical refactoring: straightforward key rename with deterministic find-and-replace
- Bounded scope: one config file and two known call sites
- Existing test coverage validates the refactoring

Escalate only if:
- The call sites are unexpectedly complex or numerous
- Behavior changes require new test logic
```

### The four tiers

| Tier | Use it for |
|---|---|
| `NO_LLM` | Work a script, formatter, or find-and-replace does reliably |
| `FAST` | Simple, bounded work |
| `STANDARD` | Normal engineering reasoning |
| `REASONING` | Novel, ambiguous, cross-system, or high-consequence work |

### The four factors

Each is scored 0 to 3. The full definitions are in [SKILL.md](plugins/intent-driven-training/skills/model-gate/SKILL.md).

| Factor | 0 | 3 |
|---|---|---|
| Complexity | Mechanical | Novel architecture or difficult reasoning |
| Context | No repository understanding needed | Broad, cross-system, or highly ambiguous |
| Consequence | Trivial and easily reversible | Security, compliance, money movement, destructive change |
| Capability | Deterministic transformation | Advanced reasoning or specialized capability |

### How the tier is decided

The rules apply in this order:

1. The work is flagged deterministic: `NO_LLM`.
2. Capability is 3, or consequence is 3 with complexity 2 or more: `REASONING`.
3. Otherwise, add the four scores (0 to 12): 3 or less is `FAST`, 4 to 7 is `STANDARD`, 8 or more is `REASONING`.

You can run the scorer yourself:

```bash
python3 plugins/intent-driven-training/skills/model-gate/scripts/model-gate.py \
  --complexity 1 --context 2 --consequence 1 --capability 2
```

It prints JSON with the tier, the scores, and the reason.

### Map tiers to your models

Out of the box ModelGate recommends a tier only. To get a model name, fill in the "Organization mapping" column in [model-tiers.md](plugins/intent-driven-training/skills/model-gate/references/model-tiers.md) with the models your team has approved. Revisit it when prices or availability change.

## The feature loop

**Intent -> smallest safe delta -> validation -> evidence -> refine only when evidence says so**

| Step | Command | What it does |
|---|---|---|
| 1 | `/intent-driven-training:setup-feature` | Creates only the files needed to start |
| 2 | `/intent-driven-training:review-intent` | Checks the intent for outcome, inputs, outputs, success criteria, and real constraints; strips prescriptions that are not requirements |
| 3 | `/intent-driven-training:model-gate` | Recommends the minimum sufficient model tier |
| 4 | `/intent-driven-training:run-feature` | Implements the smallest safe change |
| 5 | `/intent-driven-training:prove-feature` | Checks the running result against the success criteria and reports pass, fail, and unknown |

Two more are useful at any point:

- `/intent-driven-training:context-map` lists the minimum set of files, tests, and patterns the feature touches.
- `/intent-driven-training:simplify` removes detail, constraints, and abstractions the outcome does not require.

Two skills, **Feature Workflow** and **Context Discipline**, load on their own when Claude is moving a feature through the loop or deciding what to read.

Switch to the recommended tier with `/model` before step 4. Move up a tier only when the evidence from step 5 shows the current one is not enough.

## What it does not do

- It does not switch models for you. It recommends; you select.
- It does not measure or report token spend.
- The factor scores are the model's judgment of your plan. A vague plan gets a vague score, so run `review-intent` first.

## Repository layout

```
.claude-plugin/marketplace.json     marketplace manifest
plugins/intent-driven-training/     the plugin (v1.1.0)
  commands/                         six workflow commands
  skills/                           feature-workflow, context-discipline, model-gate
```

Author: Mark Kendall
