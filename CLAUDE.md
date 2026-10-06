# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Claude Code **plugin marketplace** containing one plugin, `intent-driven-training` (Intent-Driven Engineering training and workflow). It is almost entirely Markdown prompt content plus one small Python script. There is no build step, package manifest, linter, or test suite.

The repository is not an application. Standards written for a TypeScript/Node API (Zod validation, `src/routes`, `src/services`, and so on) have nothing to apply to here.

## Layout: two levels, two manifests

- `.claude-plugin/marketplace.json` (repo root) is the marketplace manifest. It lists plugins and points at each one with `source`.
- `plugins/intent-driven-training/` is the plugin root. Its own `.claude-plugin/plugin.json` holds the plugin name, version, and keywords.

Inside the plugin root:

- `commands/*.md` — slash commands. Each is frontmatter (`name`, `description`, optional `allowed-tools`) plus a one-paragraph prompt.
- `skills/<skill-name>/SKILL.md` — skills, with frontmatter `name`, `description` (the trigger condition), and `version`.

`${CLAUDE_PLUGIN_ROOT}` resolves to `plugins/intent-driven-training/`, not the repo root. Paths in skills must be written relative to it.

## How the pieces relate

The commands are stages of one loop, defined in `skills/feature-workflow/SKILL.md`:

**Intent -> smallest safe delta -> validation -> evidence -> refine only when evidence says so**

Intended order: `/setup-feature` → `/review-intent` → `/model-gate` → `/run-feature` → `/prove-feature`, with `/context-map` and `/simplify` usable at any point. All are files under `commands/` except `/model-gate`, which is the skill invoked directly. The commands are deliberately thin; the reasoning lives in the three skills (`feature-workflow`, `context-discipline`, `model-gate`).

### ModelGate

ModelGate is the only component with executable logic, and it is split on purpose:

1. The active model reads the plan and scores four factors from 0 to 3: complexity, context, consequence, capability. The rubric is in `skills/model-gate/SKILL.md`.
2. `skills/model-gate/scripts/model-gate.py` turns those scores into a tier deterministically. It makes no API calls and uses only the standard library.
3. `skills/model-gate/references/model-tiers.md` maps tiers to real model names. It ships with "Configure locally" placeholders, and the core rubric stays vendor-neutral.

Scoring rules in the script, in precedence order:

- `--deterministic` → `NO_LLM`, regardless of scores
- `capability == 3`, or `consequence == 3` with `complexity >= 2` → `REASONING`
- otherwise by sum (0–12): `<= 3` → `FAST`, `<= 7` → `STANDARD`, else `REASONING`

The rubric appears in three places: the 0–3 factor definitions in `SKILL.md`, the thresholds in `model-gate.py`, and the tier descriptions in `model-tiers.md` and the plugin `README.md`. Change them together.

## Commands

Run the scorer directly:

```bash
python3 plugins/intent-driven-training/skills/model-gate/scripts/model-gate.py \
  --complexity 1 --context 1 --consequence 3 --capability 1
```

It prints JSON with `tier`, `scores`, and `reason`. Add `--deterministic` to force `NO_LLM`.

Load the plugin into a session without installing it:

```bash
claude --plugin-dir ./plugins/intent-driven-training
```

Validate the manifests:

```bash
claude plugin validate .
```

Install through the marketplace, from inside Claude Code:

```
/plugin marketplace add <path-to-this-repo>
/plugin install intent-driven-training@intent-driven-training
```

## Things to keep consistent

- **Version**: `plugin.json` `version` (currently `1.1.0`) and the version note in the root `README.md`.
- **Command and skill lists**: adding or removing a file under `commands/` or `skills/` means updating the lists in `plugins/intent-driven-training/README.md`.
- **Descriptions**: the plugin description is written separately in `marketplace.json` and `plugin.json`.
- **Interpreter name**: invoke the scorer as `python3`. Plain `python` does not exist on machines that only ship `python3` (stock macOS, for example).
- **No `commands/model-gate.md`**: `/model-gate` comes from the skill. A command file with the same name shadows the skill, and the scorer never runs.
- **Name overlap**: the plugin's `/simplify` shares a name with a Claude Code built-in. Refer to it namespaced (`/intent-driven-training:simplify`) when it matters which one runs.

## Editing style

The plugin's content follows its own principle of minimum sufficient constraint: commands are one short paragraph, skills are a short numbered list or rubric, and prompts state what must be true instead of prescribing how to build it. Keep additions that lean.
