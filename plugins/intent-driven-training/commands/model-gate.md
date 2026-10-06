---
name: model-gate
description: Preflight the current feature or plan and recommend the minimum sufficient model before implementation.
allowed-tools: [Read, Glob, Grep, Bash]
---
Run the ModelGate skill against the current feature/intent/plan before implementation. Use only existing repository and plan context. Do not call external APIs or browse for model advice. Return one recommendation, a short reason, and explicit escalation conditions.
