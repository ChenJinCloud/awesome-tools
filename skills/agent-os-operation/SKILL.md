---
name: agent-os-operation
description: Use when modifying or auditing a local Agent OS project that stores agent rules, source maps, permissions, run ledgers, skills, adapters, hooks, or evaluation policy.
---

# Agent OS Operation

Use this skill for work inside an Agent OS governance project. It is narrower than `agent-os-global`: it applies when the Agent OS project itself is the target.

## Required Local Files

Replace these with the names used in your project:

- project `README.md`
- `source-of-truth-map.md`
- `permission-matrix.md`
- `agent-behavior-contract.md`
- `CHANGELOG.md`
- `run-ledger.md`
- validation script, if one exists

## Flow

1. Read the project entry and source-of-truth map.
2. Read the permission policy before writing.
3. Classify the task as green, yellow, or red.
4. Make the smallest useful change.
5. Update the project changelog and run ledger for yellow work.
6. Run or emulate the project validation script.
7. Report changed files, validation result, and residual risk.

## Stop Conditions

Stop before deletion, tool installation, hook activation, MCP activation, external send, credential changes, permission changes, or broad write expansion unless the user explicitly approves that specific action.
