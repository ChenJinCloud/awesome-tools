# Awesome Tools

[English](README.md) | [简体中文](README.zh-CN.md)

This repository is my public catalog of high-quality tools, workflows, and reusable agent skills.

The goal is not to collect every interesting link. Each entry should explain why the tool or solution is useful, where it fits, what boundary or risk matters, and whether I have actually used or verified it.

## Principles

- Prefer field-tested workflows over generic recommendations.
- Separate public reusable material from private implementations and personal records.
- Keep private data, credentials, account identifiers, raw exports, logs, and local machine paths out of this repository.
- Add enough context for a future agent or operator to understand the use case safely.
- Mark fragile, compliance-sensitive, or version-sensitive material explicitly.

## Structure

```text
.github/
  workflows/
catalog/
  macos-wechat-export-capability.md
  personal-system-skills.md
docs/
  repository-consolidation/
  superpowers/
    plans/
    specs/
skills/
  agent-os-global/
  agent-os-operation/
  calm-mint-pencil-cover/
  codex-closeout-archive/
  creator-pricing/
  daily-log/
  open-methodology-md/
  universal-methodology/
```

## Current Entries

| Entry | Type | Status |
| --- | --- | --- |
| [Personal System Skills](catalog/personal-system-skills.md) | Agent skill bundle | Public-safe sanitized skill set added |
| [Private WeChat Archive Capability and Post-Export Uses](catalog/macos-wechat-export-capability.md) | Private local capability | Capability and actual post-export uses only; implementation remains private |

## Skills

The `skills/` directory is the canonical public source for these skill packages. A skill should not be maintained in a second standalone repository unless it has an independent release lifecycle that cannot be supported here.

- [agent-os-global](skills/agent-os-global/SKILL.md): apply local Agent OS governance to non-trivial agent work.
- [agent-os-operation](skills/agent-os-operation/SKILL.md): operate or audit an Agent OS governance project.
- [calm-mint-pencil-cover](skills/calm-mint-pencil-cover/SKILL.md): generate a stable calm mint colored-pencil article cover style.
- [codex-closeout-archive](skills/codex-closeout-archive/SKILL.md): preserve an agent conversation as a concise process asset.
- [creator-pricing](skills/creator-pricing/SKILL.md): evaluate creator sponsorship pricing and negotiation options.
- [daily-log](skills/daily-log/SKILL.md): create or update daily logs and basic maintenance records.
- [open-methodology-md](skills/open-methodology-md/SKILL.md): open the latest methodology Markdown document in a local reader.
- [universal-methodology](skills/universal-methodology/SKILL.md): clarify ambiguous, high-stakes, or reusable matters before execution.

## Entry Template

Use this shape when adding a new tool, workflow, or capability note:

```markdown
# Name

## What It Is
## Why It Is Useful
## Best Use Cases
## Source / Project Links
## Boundaries And Risks
## My Usage Status
## Recheck Before Use
```

## Public Boundary

This repository contains public, reusable material only. Private implementations, personal source data, credentials, machine-specific paths, raw exports, and private validation evidence belong in their respective private systems.
