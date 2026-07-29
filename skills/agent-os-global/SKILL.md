---
name: agent-os-global
description: Use to apply a local Agent OS governance protocol to non-trivial agent work, including risk classification, durable record routing, and red-action boundaries.
---

# Agent OS Global

Use this skill when an agent task may affect future context, records, rules, permissions, or work continuity. It is a portable public version; replace the placeholder paths with your own local operating-system paths.

## Canonical Inputs

Define these in your environment:

- `AGENT_OS_ROOT`: folder containing agent governance docs.
- `LIFE_OS_ROOT`: folder containing durable personal or team records.
- `GLOBAL_WORK_LEDGER`: lightweight ledger for non-project work.

Recommended governance files:

- `README.md`
- `source-of-truth-map.md`
- `permission-matrix.md`
- `agent-behavior-contract.md`
- `recording-policy.md`

## Workflow

1. Classify matter type, risk level, target deliverable, and likely record destination.
2. Read only the governance files needed for the current task.
3. Execute the smallest useful action.
4. If the task changes durable context, write the result to the correct record path.
5. If no specific path exists, add a light ledger entry.
6. If a repeated correction or failure appears, update or propose a policy, lesson, skill, or adapter change.
7. Stop before red actions.

## Red Actions

Ask before deletion, external send or publish, spending money, credential or permission changes, tool or background-agent activation, legal or medical commitments, broad cross-disk write expansion, or other irreversible actions.

## Closeout Standard

Every non-trivial task should end with one of:

- a durable record path;
- a global ledger entry;
- a brief reason no record was appropriate.
