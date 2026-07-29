# Product Curation Design

## Purpose

`awesome-tools` is a small, strict, personal product collection built on the maintainer's direct experience, sustained observation, or trusted first-hand user experience. It is not intended to be a comprehensive directory, a bookmark collection, or a vendor advertising channel.

Inclusion does not automatically mean endorsement. Every formal entry states the depth and source of its verification.

## Scope

The collection may include any product type, including:

- software and desktop or mobile applications;
- SaaS and online services;
- hardware;
- professional or consumer services;
- open-source projects;
- tools and workflows that combine multiple products.

Products qualify because they support a concrete use case and satisfy the evidence requirements below, not because they belong to a preferred industry or technology category.

## Repository Structure

```text
README.md
catalog/
products/
  software/
  saas/
  hardware/
  services/
  open-source/
archive/
.github/
  ISSUE_TEMPLATE/
    suggest-product.yml
  PULL_REQUEST_TEMPLATE.md
templates/
  product-entry.md
```

- `catalog/` retains deep tool and workflow records such as the existing WeChat export entry.
- `products/` contains formally accepted product entries.
- `archive/` preserves entries that are no longer current or recommended, together with the reason.
- Candidates remain in GitHub Issues and do not appear under `products/`.

## Status Model

Formal product entries have one of three statuses:

| Status | Meaning |
| --- | --- |
| `researched` | The maintainer formed an independent judgment using sustained observation, trusted first-hand user experience, and primary product sources, but has not personally completed a core workflow. |
| `tested` | The maintainer personally completed at least one core product workflow and recorded the environment, result, and limitations. |
| `recommended` | The maintainer is willing to recommend the product for a defined audience and use case, with explicit situations where it should not be recommended. |

`candidate` is an Issue state, not a formal catalog status. A normal progression is:

```text
Candidate Issue -> researched -> tested -> recommended
```

Status may also be reduced when evidence, product quality, or current relevance changes. Products that no longer qualify move to `archive/`.

`needs-review` is a temporary maintenance label, not a fourth formal status. While the label is active, README presentation must not treat the entry as a current recommendation.

## Admission Criteria

A product may enter `products/` only when all of the following are true:

1. It supports a concrete and explainable use case.
2. The judgment is based on direct use, sustained observation, or specific first-hand experience from a trusted user.
3. Primary sources have been checked for the product's capabilities, pricing, availability, and platform support.
4. The entry explains why the product deserves attention relative to ordinary alternatives.
5. Important limitations, risks, and unsuitable use cases are stated.
6. Confirmed facts, third-party experience, and maintainer judgment are distinguishable.
7. The verification status and last review date are present.
8. Vendor relationships, sponsorships, affiliate incentives, and other conflicts are disclosed.
9. No credentials, private records, internal URLs, private account identifiers, cookies, sessions, logs, or machine-specific private paths are included.

A product remains a Candidate Issue when it is supported only by marketing, popularity, a casual recommendation, or incomplete evidence.

## Product Entry Schema

Each product uses one Markdown file with the following sections:

```markdown
# Product Name

Status:
Last reviewed:
Product type:
Official website:

## What It Is
## Why It Earned A Place
## Best For
## Experience Basis
## What Has Been Verified
## What Has Not Been Verified
## Strengths
## Limitations And Risks
## Pricing And Access
## Privacy And Data Handling
## Alternatives
## Source Links
## Disclosure
```

`Experience Basis` is mandatory and identifies whether the judgment comes from direct use, sustained observation, or trusted first-hand user experience. `What Has Not Been Verified` is mandatory for `researched` entries.

## Candidate And Contribution Workflow

```text
Discover or receive a product
-> create one Candidate Issue
-> check duplicates, scope, experience basis, and conflicts
-> collect primary sources and trusted experience
-> reject, continue observing, or prepare a formal entry
-> submit one product per pull request
-> run automated format and safety checks
-> maintainer review
-> merge or request changes
```

Candidate Issues collect:

- product name, official URL, and product type;
- the problem it solves;
- the submitter's identity and relationship to the product;
- the reason it deserves investigation;
- the source and depth of existing experience;
- whether the maintainer or submitter has used it;
- known limitations, risks, and alternatives.

The maintainer may create candidates and entries directly. Users and vendors may submit Candidate Issues, but vendor self-nominations must disclose their relationship. External submitters cannot assign `tested` or `recommended`; those statuses require the maintainer's direct experience and judgment. External pull requests contain one product each.

Initially, public contribution is Issue-first. Direct external product pull requests should be enabled only after approximately ten accepted entries demonstrate that the schema and review standard are stable.

## Automated Checks

Automation checks structure and public safety, not whether a product is good. Checks should cover:

- required metadata and sections;
- allowed status values;
- duplicate official URLs;
- broken links;
- presence and validity of `Last reviewed`;
- accidental secrets, account identifiers, raw records, logs, or private paths;
- `What Has Not Been Verified` for `researched` entries;
- a concrete completed workflow for `tested` and `recommended` entries;
- a defined audience, use case, and non-recommendation boundary for `recommended` entries.

The checks must report file and rule names without printing detected secret values.

## Review And Maintenance

Default review intervals are:

| Product type or risk | Review interval |
| --- | --- |
| Stable software or hardware | 12 months |
| SaaS, AI products, or rapidly changing services | 6 months |
| Products handling sensitive data, permissions, or private workflows | 3-6 months |

A major redesign, acquisition, material pricing change, service shutdown, or security incident triggers an immediate review.

Review outcomes are:

- retain the status and update `Last reviewed`;
- apply the temporary `needs-review` label when evidence is incomplete;
- reduce the status when the prior judgment is no longer supported;
- move the entry to `archive/` when the product is unavailable, unmaintained, materially degraded, unsafe for the documented use, or no longer worthy of inclusion.

Archived entries retain the archive date, former status, reason, possible replacements, and an explicit warning that historical conclusions may be stale.

## Edge Cases

- A temporarily unavailable website produces a `needs-review` label, not immediate deletion.
- Unconfirmed pricing blocks status upgrades and is labeled as unconfirmed.
- Conflicts between vendor claims and trusted experience remain visible and attributed.
- Vendor requests may correct factual errors but do not override independent judgments.
- Unverified security reports are attributed and labeled as unconfirmed.
- Contributions containing private data are cleaned or closed without repeating the sensitive material in public discussion.

## Acceptance Criteria

The product curation system is ready for implementation when:

- the repository distinguishes candidates from formal entries;
- the three formal statuses have enforceable evidence requirements;
- a reusable product template and Candidate Issue template exist;
- one product maps to one reviewable pull request;
- automated checks cover schema, links, duplication, freshness, and public safety;
- README presentation prioritizes `recommended`, then `tested`, while clearly labeling `researched`;
- review and archive rules preserve history without implying that stale judgments remain current.
