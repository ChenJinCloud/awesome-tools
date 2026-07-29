---
name: daily-log
description: Use to create or update daily logs, maintenance notes, plans-vs-actuals, basic state tracking, and next-day minimum actions.
---

# Daily Log

Use this skill when the user wants to record the day, update a log, compare plan versus actual, or track basic maintenance state.

## Configure Paths

Set these for your own system:

```text
DAILY_LOG_ROOT=<your daily log folder>
MAINTENANCE_ROOT=<your maintenance or basic state folder>
```

Recommended daily filename:

```text
YYYY/YYYY-MM/YYYY-MM-DD.md
```

## Daily Template

```markdown
# YYYY-MM-DD Daily Log

## Overview

## Original Plan

## Actual Timeline

## Completed

## Unfinished / Rolled Forward

## Deviations And Reasons

## Basic State
- Sleep:
- Food:
- Movement:
- Hygiene:
- Outside:
- Mood:

## Key Communications / Decisions

## Risk Signals

## Minimum Actions For Tomorrow

## Sources
```

## Workflow

1. Resolve the date from the user or current local date.
2. Create the daily file if missing; otherwise read the existing file.
3. Append time-ordered updates to `Actual Timeline`.
4. Move finished items to `Completed`.
5. Record health or maintenance signals in `Basic State`.
6. At closeout, summarize deviations and choose tomorrow's minimum actions.

## Guardrails

- Do not over-polish raw daily logs.
- Keep private details local.
- Preserve source notes when the user is using the log as evidence.
