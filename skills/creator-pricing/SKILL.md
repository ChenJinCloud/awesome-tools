---
name: creator-pricing
description: Use to evaluate YouTube creator sponsorship pricing, negotiation posture, renewal decisions, and whether a quoted price fits the channel, market, and campaign goal.
---

# Creator Pricing

Use this skill when the user needs to judge whether a creator quote is reasonable, how to negotiate, or whether to renew a creator partnership.

## Inputs

Ask for or infer:

- channel URL or handle;
- quoted price and deliverable type;
- target market and audience geography;
- recent average views;
- subscriber count;
- sponsorship format: dedicated video, integration, short, newsletter, or bundle;
- campaign goal: conversion, launch awareness, trust-building, or experiment.

## Data Check

When possible, inspect recent public channel data:

- last 10 long-form videos, excluding unusually fresh videos if they have not had time to mature;
- average views;
- views-to-subscriber ratio;
- engagement rate;
- posting frequency;
- recent growth trend;
- audience geography, if available from the creator or platform screenshots.

## Evaluation Framework

Score 1 to 5:

| Dimension | What To Check |
| --- | --- |
| Category fit | Is the content close to the product's buyer or user? |
| Audience fit | Does the audience match the target geography and role? |
| Content quality | Can the creator explain complex products clearly? |
| Data quality | Views, engagement, growth, consistency, and comments. |
| Competitive context | Recent sponsorships, saturation, or direct competitor exposure. |

Then compare the quote to implied CPM:

```text
implied_cpm = quoted_price / expected_views * 1000
```

Use regional and category benchmarks only as a guide. Do not treat CPM as the whole decision.

## Recommendation Bands

- Strong yes: strong fit, healthy data, price within acceptable range, and clear campaign goal.
- Negotiate: good fit but price, deliverables, or risk allocation needs adjustment.
- Experiment: uncertain fit; use lower budget, performance component, or small scope.
- Decline: weak fit, inflated price, poor audience match, or direct competitor conflict.

## Negotiation Options

Offer structured options rather than only pushing price down:

- lower fixed fee plus performance bonus;
- smaller first integration before a larger renewal;
- bundle of multiple posts with review gates;
- make-good clause when minimum view threshold is missed;
- creator autonomy in exchange for better pricing or timeline flexibility.

## Output Format

```markdown
Verdict:
Reasonable price range:
Quote assessment:
Key risks:
Recommended negotiation posture:
Suggested message:
What would change the decision:
```

## Guardrails

- Verify current public data before making a high-cost recommendation.
- Do not invent private analytics.
- Separate top-funnel value from direct conversion.
- Keep negotiation language respectful and relationship-preserving.
