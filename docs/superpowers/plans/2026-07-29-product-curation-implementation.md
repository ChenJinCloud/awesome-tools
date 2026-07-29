# Product Curation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a small, strict product-curation system that separates candidates from formal entries, enforces evidence-based statuses, and protects the public repository from malformed, stale, duplicate, or sensitive submissions.

**Architecture:** Markdown remains the human-readable source of truth. One product lives in one typed directory and uses a fixed metadata/section schema; small Python standard-library validators enforce structure, freshness, duplicate URLs, and link availability. GitHub Issue and pull-request templates provide the human intake gates, while one CI workflow combines the new catalog checks with the existing public-safety scanner.

**Tech Stack:** Markdown, GitHub Issue Forms, GitHub Actions, Python 3.11+ standard library, existing `scripts/check_public_safety.py`.

## Global Constraints

- The repository is a small, strict personal collection, not a comprehensive directory or advertising channel.
- Product types are `software`, `saas`, `hardware`, `services`, and `open-source`.
- Formal statuses are exactly `researched`, `tested`, and `recommended`; `candidate` exists only in Issues.
- `tested` and `recommended` require the maintainer's direct experience.
- `researched` requires sustained observation or specific first-hand experience from a trusted user plus primary sources.
- One product entry is one Markdown file and one product submission is one pull request.
- No credentials, raw private records, account identifiers, cookies, sessions, logs, or machine-specific private paths may enter the repository.
- Use only Python's standard library; do not add package-manager dependencies for catalog validation.
- Link checks must use bounded timeouts and retries and must never submit credentials or authenticated requests.
- Automation validates structure and public safety, never whether a product is genuinely good.

---

## File Map

| Path | Responsibility |
| --- | --- |
| `templates/product-entry.md` | Canonical copyable product-entry template and field instructions. |
| `products/README.md` | Explains formal statuses, typed directories, and admission boundary. |
| `products/software/.gitkeep` | Tracks the software directory before its first entry. |
| `products/saas/.gitkeep` | Tracks the SaaS directory before its first entry. |
| `products/hardware/.gitkeep` | Tracks the hardware directory before its first entry. |
| `products/services/.gitkeep` | Tracks the services directory before its first entry. |
| `products/open-source/.gitkeep` | Tracks the open-source directory before its first entry. |
| `archive/README.md` | Defines archive metadata and prevents archived entries from implying a current recommendation. |
| `scripts/check_product_catalog.py` | Parses and validates entry metadata, headings, status evidence, type placement, duplicate URLs, risk-based review intervals, and freshness. |
| `scripts/test_product_catalog.py` | Network-free regression tests for catalog validation. |
| `scripts/check_product_links.py` | Checks public product/source URLs using bounded anonymous HTTP requests. |
| `scripts/test_product_links.py` | Local fake-server tests for link success, retry, and failure behavior. |
| `.github/ISSUE_TEMPLATE/suggest-product.yml` | Candidate-only product suggestion form with relationship disclosure. |
| `.github/PULL_REQUEST_TEMPLATE/product.md` | Product-specific one-entry PR checklist and maintainer-only status declaration without affecting code PRs. |
| `.github/workflows/product-catalog-checks.yml` | Runs structural tests, catalog validation, public-safety checks, and link checks. |
| `README.md` | Explains the curation model and links to candidates, formal products, archive, and contribution paths. |

---

### Task 1: Establish the product entry contract and repository directories

**Files:**
- Create: `templates/product-entry.md`
- Create: `products/README.md`
- Create: `products/software/.gitkeep`
- Create: `products/saas/.gitkeep`
- Create: `products/hardware/.gitkeep`
- Create: `products/services/.gitkeep`
- Create: `products/open-source/.gitkeep`
- Create: `archive/README.md`

**Interfaces:**
- Consumes: The approved status definitions and admission criteria in `docs/superpowers/specs/2026-07-29-product-curation-design.md`.
- Produces: Exact metadata labels and heading names consumed by `scripts/check_product_catalog.py`: `Status`, `Last reviewed`, `Product type`, `Official website`, and the 13 required `##` headings below.

- [ ] **Step 1: Create the canonical entry template**

Create `templates/product-entry.md` with literal placeholders that are safe because this is a copyable template, not a formal product entry:

```markdown
# Product Name

Status: researched
Last reviewed: 2026-07-29
Product type: software
Official website: https://example.com
Review interval months: 12

## What It Is

State what the product does in concrete language.

## Why It Earned A Place

Explain why it deserves a place in this small collection rather than merely being notable.

## Best For

Name the audience and use cases that benefit most.

## Experience Basis

State whether the judgment is based on direct use, sustained observation, or specific first-hand experience from a trusted user.

## What Has Been Verified

Separate confirmed product facts and completed workflows from judgment.

## What Has Not Been Verified

List untested capabilities and uncertain claims. For `tested` or `recommended`, write `None material for the documented use case.` only when accurate.

## Strengths

List strengths supported by the experience basis and sources.

## Limitations And Risks

Include unsuitable use cases and material security, privacy, reliability, or lock-in concerns.

## Pricing And Access

State the plan or purchase basis checked and the date. Mark unconfirmed pricing explicitly.

## Privacy And Data Handling

Describe only publicly supportable data-handling facts and any unresolved questions.

## Alternatives

Name meaningful substitutes and why this product still merits inclusion.

## Source Links

- [Official website](https://example.com)
- [Official documentation](https://example.com/docs)

## Disclosure

State vendor, sponsorship, affiliate, or other conflicts. Write `None.` when there are none.
```

- [ ] **Step 2: Document formal product placement**

Create `products/README.md` explaining:

```markdown
# Products

Formal entries appear here only after passing the admission criteria in the product-curation design. Unreviewed discoveries remain Candidate Issues.

## Statuses

- `researched`: independent judgment from sustained observation or trusted first-hand experience plus primary sources; not personally tested.
- `tested`: the maintainer personally completed at least one core workflow.
- `recommended`: the maintainer can name who should use it, why, and when not to use it.

Inclusion is not endorsement. Open `README.md` at the repository root for the contribution route.

## Recommended

No entries yet.

## Tested

No entries yet.

## Researched

No entries yet.
```

- [ ] **Step 3: Create typed directories and archive rules**

Create the five empty `.gitkeep` files. Create `archive/README.md` requiring archived entries to record `Archived`, `Former status`, `Archive reason`, `Possible replacements`, and a stale-conclusion warning.

- [ ] **Step 4: Run public-safety checks**

Run:

```bash
python scripts/check_public_safety.py --root .
python scripts/test_public_safety.py
```

Expected: both commands exit `0` and print their pass messages.

- [ ] **Step 5: Commit the contract**

```bash
git add templates/product-entry.md products archive
git commit -m "docs: define product entry contract"
```

---

### Task 2: Build the catalog validator with test-driven development

**Files:**
- Create: `scripts/check_product_catalog.py`
- Create: `scripts/test_product_catalog.py`

**Interfaces:**
- Consumes: Markdown files under `products/<product-type>/*.md` and the field/heading contract from Task 1.
- Produces: `validate_catalog(root: Path, today: date) -> list[Finding]`; CLI exit `0` when there are no errors, exit `2` otherwise; diagnostics contain only file, rule ID, and safe explanation.

- [ ] **Step 1: Write failing fixture tests for valid and malformed entries**

Create `scripts/test_product_catalog.py` using `tempfile.TemporaryDirectory`. Import `validate_catalog` from `check_product_catalog` and define this fixture builder:

```python
def entry(
    *,
    name: str = "Example Product",
    status: str = "researched",
    reviewed: str = "2026-07-29",
    product_type: str = "software",
    website: str = "https://example.com",
    experience: str = "Sustained observation plus a trusted user's first-hand workflow.",
    verified: str = "Official capabilities and pricing were checked.",
    unverified: str = "The maintainer has not completed the core workflow.",
    limitations: str = "A material limitation.",
    review_months: str = "12",
) -> str:
    sections = {
        "What It Is": "A concrete product description.",
        "Why It Earned A Place": "It solves the documented problem unusually well.",
        "Best For": "Teams with the documented use case.",
        "Experience Basis": experience,
        "What Has Been Verified": verified,
        "What Has Not Been Verified": unverified,
        "Strengths": "A supported strength.",
        "Limitations And Risks": limitations,
        "Pricing And Access": "Official pricing checked on 2026-07-29.",
        "Privacy And Data Handling": "Public privacy terms were reviewed.",
        "Alternatives": "A meaningful alternative.",
        "Source Links": "- [Official website](https://example.com)",
        "Disclosure": "None.",
    }
    body = "\n\n".join(f"## {heading}\n\n{text}" for heading, text in sections.items())
    return (
        f"# {name}\n\nStatus: {status}\nLast reviewed: {reviewed}\n"
        f"Product type: {product_type}\nOfficial website: {website}\n"
        f"Review interval months: {review_months}\n\n{body}\n"
    )
```

Add these helpers so every assertion creates an isolated real file:

```python
def write_entry(root: Path, text: str, directory: str = "software", name: str = "example.md") -> None:
    target = root / "products" / directory / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def rule_ids_for(*, directory: str = "software", **overrides: str) -> set[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_entry(root, entry(**overrides), directory=directory)
        return {finding.rule for finding in validate_catalog(root, date(2026, 7, 29))}


def rules_for_two_entries_with_same_url() -> set[str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_entry(root, entry(name="One"), name="one.md")
        write_entry(root, entry(name="Two"), name="two.md")
        return {finding.rule for finding in validate_catalog(root, date(2026, 7, 29))}
```

Add tests asserting:

```python
assert validate_catalog(root, date(2026, 7, 29)) == []
assert "invalid-status" in rule_ids_for(status="candidate")
assert "type-directory-mismatch" in rule_ids_for(product_type="saas", directory="software")
assert "researched-unverified-required" in rule_ids_for(status="researched", unverified="")
assert "tested-direct-experience-required" in rule_ids_for(status="tested", experience="Trusted user report only.")
assert "recommended-boundary-required" in rule_ids_for(status="recommended", limitations="")
assert "duplicate-official-url" in rules_for_two_entries_with_same_url()
assert "review-stale" in rule_ids_for(reviewed="2026-01-28", review_months="6")
assert "review-interval" in rule_ids_for(review_months="5")
```

- [ ] **Step 2: Run the tests and verify the import failure**

Run:

```bash
python scripts/test_product_catalog.py
```

Expected: non-zero exit with `ModuleNotFoundError: No module named 'check_product_catalog'`.

- [ ] **Step 3: Implement the parser and finding types**

Create `scripts/check_product_catalog.py` with:

```python
@dataclass(frozen=True)
class Finding:
    file: str
    rule: str
    message: str


@dataclass(frozen=True)
class Entry:
    path: Path
    title: str
    status: str
    last_reviewed: date
    product_type: str
    official_website: str
    review_interval_months: int
    sections: dict[str, str]


def parse_entry(path: Path) -> tuple[Entry | None, list[Finding]]:
    """Parse one Markdown entry without following links or reading other files."""


def validate_entry(entry: Entry, root: Path, today: date) -> list[Finding]:
    """Validate schema, placement, status evidence, and review freshness."""


def validate_catalog(root: Path, today: date) -> list[Finding]:
    """Validate all product entries and report duplicate canonical URLs."""
```

Use exact constants:

```python
ALLOWED_STATUSES = {"researched", "tested", "recommended"}
ALLOWED_TYPES = {"software", "saas", "hardware", "services", "open-source"}
REVIEW_MONTHS = {
    "software": 12,
    "saas": 6,
    "hardware": 12,
    "services": 6,
    "open-source": 12,
}
ALLOWED_REVIEW_MONTHS = {3, 6, 12}
REQUIRED_SECTIONS = (
    "What It Is",
    "Why It Earned A Place",
    "Best For",
    "Experience Basis",
    "What Has Been Verified",
    "What Has Not Been Verified",
    "Strengths",
    "Limitations And Risks",
    "Pricing And Access",
    "Privacy And Data Handling",
    "Alternatives",
    "Source Links",
    "Disclosure",
)
```

Canonicalize official URLs by lowercasing scheme/host, removing a trailing slash, and rejecting query strings/fragments for the official website field. Require `Review interval months` to be `3`, `6`, or `12`; it may shorten but never lengthen the default interval for the product type. Use `3` or `6` for sensitive data, permission, or private-workflow products. For direct-experience enforcement, require the exact marker `Direct use:` in `Experience Basis` for `tested` and `recommended`. For a recommendation boundary, require the exact marker `Do not use when:` under `Limitations And Risks` for `recommended`.

- [ ] **Step 4: Implement safe CLI behavior**

Add CLI options:

```text
--root PATH       repository root, default parent of scripts/
--today YYYY-MM-DD  deterministic date override for tests and maintenance
--json            emit findings as JSON without entry contents
```

Print only safe diagnostics:

```text
Product catalog validation failed.
- products/saas/example.md [review-stale] Review is older than the 6-month interval.
```

Do not print section contents or URLs.

- [ ] **Step 5: Run validator tests and the empty real catalog**

Run:

```bash
python scripts/test_product_catalog.py
python scripts/check_product_catalog.py --root .
```

Expected: tests print `Product catalog validator tests passed.` and the real catalog prints `Product catalog validation passed.` with exit `0`.

- [ ] **Step 6: Commit the validator**

```bash
git add scripts/check_product_catalog.py scripts/test_product_catalog.py
git commit -m "feat: validate product catalog entries"
```

---

### Task 3: Add bounded anonymous link validation

**Files:**
- Create: `scripts/check_product_links.py`
- Create: `scripts/test_product_links.py`

**Interfaces:**
- Consumes: Public `http` and `https` URLs extracted from `Official website` and `Source Links` in formal product Markdown files.
- Produces: `check_urls(urls: Iterable[str], timeout: float, retries: int) -> list[LinkFinding]`; CLI exit `0` on success, `2` for confirmed failures; no response bodies are stored or printed.

- [ ] **Step 1: Write failing fake-server tests**

Create `scripts/test_product_links.py` with a local `ThreadingHTTPServer` handler exposing:

```text
/ok       -> HEAD 200
/head405  -> HEAD 405, GET 200
/missing  -> HEAD 404
/flaky    -> first HEAD 503, second HEAD 200
```

Assert:

```python
assert check_urls([base + "/ok"], timeout=1, retries=1) == []
assert check_urls([base + "/head405"], timeout=1, retries=1) == []
assert check_urls([base + "/flaky"], timeout=1, retries=2) == []
assert check_urls([base + "/missing"], timeout=1, retries=1)[0].rule == "link-http-error"
assert check_urls(["file:///private/path"], timeout=1, retries=1)[0].rule == "link-scheme"
```

- [ ] **Step 2: Run the tests and verify the import failure**

Run:

```bash
python scripts/test_product_links.py
```

Expected: non-zero exit with `ModuleNotFoundError: No module named 'check_product_links'`.

- [ ] **Step 3: Implement URL extraction and checking**

Create `scripts/check_product_links.py` using `urllib.request` and `urllib.parse`. Define:

```python
@dataclass(frozen=True)
class LinkFinding:
    url_host: str
    rule: str
    message: str


def extract_urls(root: Path) -> list[str]:
    """Return unique public URLs from formal product entries only."""


def check_urls(
    urls: Iterable[str], timeout: float = 5.0, retries: int = 2
) -> list[LinkFinding]:
    """Check URLs anonymously with HEAD and a GET fallback for 405/501."""
```

Requirements:

- allow only `http` and `https`;
- never read credentials from environment or configuration;
- reject URLs with username/password components;
- set a static `User-Agent: awesome-tools-link-check/1.0`;
- use `HEAD`, falling back to `GET` only for status `405` or `501`;
- retry status `429`, `500`, `502`, `503`, and `504` with delays of `0.5` then `1.0` seconds;
- treat redirects as normal `urllib` behavior;
- print only hostname, rule, and status category, not query strings or response bodies.

- [ ] **Step 4: Add deterministic CLI controls**

Support:

```text
--root PATH
--timeout SECONDS
--retries COUNT
```

When no formal entries exist, print `No product links to check.` and exit `0`.

- [ ] **Step 5: Run local tests**

Run:

```bash
python scripts/test_product_links.py
python scripts/check_product_links.py --root . --timeout 5 --retries 2
```

Expected: fake-server tests pass; the empty catalog reports no links and exits `0`.

- [ ] **Step 6: Commit the link checker**

```bash
git add scripts/check_product_links.py scripts/test_product_links.py
git commit -m "feat: check product catalog links"
```

---

### Task 4: Add candidate intake and pull-request governance

**Files:**
- Create: `.github/ISSUE_TEMPLATE/suggest-product.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE/product.md`

**Interfaces:**
- Consumes: Candidate fields and authority boundaries from the approved design.
- Produces: Candidate Issues labeled `candidate`; a `needs-review` maintenance label; product PRs that require one-entry scope and maintainer-owned status decisions.

- [ ] **Step 1: Create the Candidate Issue Form**

Create `.github/ISSUE_TEMPLATE/suggest-product.yml` with:

```yaml
name: Suggest a product
description: Propose one product for research; suggestion does not imply inclusion or endorsement.
title: "Candidate: "
labels: ["candidate"]
body:
  - type: markdown
    attributes:
      value: Candidates remain in Issues until the maintainer independently accepts them.
  - type: input
    id: name
    attributes: {label: Product name}
    validations: {required: true}
  - type: input
    id: website
    attributes: {label: Official website, placeholder: "https://example.com"}
    validations: {required: true}
  - type: dropdown
    id: type
    attributes:
      label: Product type
      options: [software, saas, hardware, services, open-source]
    validations: {required: true}
  - type: textarea
    id: problem
    attributes: {label: Problem and concrete use case}
    validations: {required: true}
  - type: dropdown
    id: experience
    attributes:
      label: Experience basis
      options: [I used it directly, Trusted user used it directly, Sustained observation, Marketing or discovery only]
    validations: {required: true}
  - type: textarea
    id: evidence
    attributes: {label: Specific experience and primary sources}
    validations: {required: true}
  - type: textarea
    id: risks
    attributes: {label: Known limitations, risks, and alternatives}
    validations: {required: true}
  - type: dropdown
    id: relationship
    attributes:
      label: Relationship to the product
      options: [None, User or customer, Employee or creator, Sponsor or affiliate, Other material relationship]
    validations: {required: true}
  - type: textarea
    id: disclosure
    attributes: {label: Relationship details, description: "Write None when there is no relationship."}
    validations: {required: true}
  - type: checkboxes
    id: safety
    attributes:
      label: Public-safety confirmation
      options:
        - label: I did not include credentials, private records, account identifiers, logs, or private paths.
          required: true
```

- [ ] **Step 2: Disable unstructured Issues and define the PR checklist**

Create `.github/ISSUE_TEMPLATE/config.yml` with `blank_issues_enabled: false`. Create `.github/PULL_REQUEST_TEMPLATE/product.md` requiring:

- exactly one product entry;
- an existing Candidate Issue link;
- submitter relationship disclosure;
- maintainer confirmation of formal status;
- primary-source links;
- completed public-safety and catalog checks;
- confirmation that `tested`/`recommended` contains `Direct use:`;
- confirmation that `recommended` contains `Do not use when:`.

- [ ] **Step 3: Validate YAML and required copy locally**

Run this standard-library smoke test:

```bash
python - <<'PY'
from pathlib import Path

issue = Path('.github/ISSUE_TEMPLATE/suggest-product.yml').read_text()
required = ['labels: ["candidate"]', 'id: relationship', 'id: disclosure', 'id: safety']
missing = [item for item in required if item not in issue]
raise SystemExit(f"missing: {missing}" if missing else 0)
PY
```

Expected: exit `0` with no output. GitHub performs the authoritative Issue Form schema validation when the branch is pushed.

- [ ] **Step 4: Create the required repository labels**

Run these idempotent commands against `ChenJinCloud/awesome-tools`:

```bash
gh label create candidate --repo ChenJinCloud/awesome-tools --color D4C5F9 --description "Product proposed for investigation; not formally included" --force
gh label create needs-review --repo ChenJinCloud/awesome-tools --color FBCA04 --description "Current evidence or review date needs maintainer attention" --force
```

Verify:

```bash
gh label list --repo ChenJinCloud/awesome-tools --json name --jq '.[].name' | rg '^(candidate|needs-review)$'
```

Expected: both label names are printed.

- [ ] **Step 5: Commit governance templates**

```bash
git add .github/ISSUE_TEMPLATE .github/PULL_REQUEST_TEMPLATE/product.md
git commit -m "docs: add product contribution workflow"
```

---

### Task 5: Wire catalog and privacy checks into GitHub Actions

**Files:**
- Create: `.github/workflows/product-catalog-checks.yml`

**Interfaces:**
- Consumes: Test and CLI scripts from Tasks 2 and 3 plus existing `scripts/check_public_safety.py` and `scripts/test_public_safety.py`.
- Produces: One required-check candidate named `product-catalog` for pushes and pull requests affecting products, templates, validators, workflows, or public-safety rules.

- [ ] **Step 1: Create the workflow**

Create `.github/workflows/product-catalog-checks.yml`:

```yaml
name: Product catalog checks

on:
  pull_request:
    paths:
      - "products/**"
      - "archive/**"
      - "templates/**"
      - ".github/ISSUE_TEMPLATE/**"
      - ".github/PULL_REQUEST_TEMPLATE/**"
      - ".github/workflows/product-catalog-checks.yml"
      - "scripts/check_product_*.py"
      - "scripts/test_product_*.py"
      - "scripts/check_public_safety.py"
      - "scripts/test_public_safety.py"
  push:
    branches: [main]
    paths:
      - "products/**"
      - "archive/**"
      - "templates/**"
      - ".github/**"
      - "scripts/**"

permissions:
  contents: read

jobs:
  product-catalog:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Test public-safety scanner
        run: python scripts/test_public_safety.py
      - name: Scan public repository
        run: python scripts/check_public_safety.py --root .
      - name: Test product catalog validator
        run: python scripts/test_product_catalog.py
      - name: Validate product catalog
        run: python scripts/check_product_catalog.py --root .
      - name: Test product link checker
        run: python scripts/test_product_links.py
      - name: Check product links
        run: python scripts/check_product_links.py --root . --timeout 5 --retries 2
```

Do not add write permissions, secrets, scheduled jobs, or automatic commits in this first implementation.

- [ ] **Step 2: Verify all commands locally in workflow order**

Run:

```bash
python scripts/test_public_safety.py
python scripts/check_public_safety.py --root .
python scripts/test_product_catalog.py
python scripts/check_product_catalog.py --root .
python scripts/test_product_links.py
python scripts/check_product_links.py --root . --timeout 5 --retries 2
```

Expected: all six commands exit `0`.

- [ ] **Step 3: Commit CI**

```bash
git add .github/workflows/product-catalog-checks.yml
git commit -m "ci: validate product catalog"
```

---

### Task 6: Integrate the curation system into the public README

**Files:**
- Modify: `README.md`
- Modify: `docs/public-review-checklist.md`

**Interfaces:**
- Consumes: All templates, validators, contribution routes, and commands produced by Tasks 1-5.
- Produces: The public navigation and operator instructions for discovering, suggesting, reviewing, adding, and archiving products.

- [ ] **Step 1: Add the product-curation positioning to README**

Immediately after the opening description, add:

```markdown
## Product Curation

This is a small, strict personal collection, not a comprehensive directory. Formal product entries are grounded in direct use, sustained observation, or specific first-hand experience from a trusted user. Inclusion is not endorsement.

| Status | Meaning |
| --- | --- |
| `researched` | Independently researched from primary sources and trusted experience; not personally tested. |
| `tested` | I personally completed at least one core workflow. |
| `recommended` | I can state who should use it, why, and when not to use it. |

- [Browse formal products](products/README.md)
- [Suggest one Candidate product](https://github.com/ChenJinCloud/awesome-tools/issues/new?template=suggest-product.yml)
- [Read the product-entry template](templates/product-entry.md)
- [Review archived entries](archive/README.md)
```

Extend the Structure block with `products/`, `archive/`, `templates/product-entry.md`, the two product checker scripts, and `.github/` contribution files. Do not add a product to `Current Entries` until a real entry passes review.

- [ ] **Step 2: Extend the manual public-review checklist**

Add a Product Entries section to `docs/public-review-checklist.md` requiring reviewers to check:

- experience basis is specific and attributable;
- verified and unverified claims are separated;
- recommendation audience and non-use boundary are explicit;
- pricing and privacy statements cite current primary sources;
- disclosure is complete;
- no private evidence was copied into the public entry.

- [ ] **Step 3: Run the complete local verification suite**

Run:

```bash
python scripts/test_public_safety.py
python scripts/check_public_safety.py --root .
python scripts/test_product_catalog.py
python scripts/check_product_catalog.py --root .
python scripts/test_product_links.py
python scripts/check_product_links.py --root . --timeout 5 --retries 2
git diff --check
```

Expected: every Python command exits `0`; `git diff --check` produces no output.

- [ ] **Step 4: Verify implementation against the approved design**

Check each acceptance criterion in `docs/superpowers/specs/2026-07-29-product-curation-design.md` and record the evidence in the eventual pull-request description:

```text
Candidates separated from products: Issue Form + products/README.md
Three statuses enforced: check_product_catalog.py
Reusable templates: product-entry.md + suggest-product.yml
One product per PR: PULL_REQUEST_TEMPLATE.md
Schema/link/duplicate/freshness/safety checks: scripts + workflow
README presentation order: README status table and no unreviewed entries
Archive history: archive/README.md
```

- [ ] **Step 5: Commit public documentation**

```bash
git add README.md docs/public-review-checklist.md
git commit -m "docs: publish product curation guide"
```

---

### Task 7: Final branch verification and publication

**Files:**
- Verify only; no new files expected.

**Interfaces:**
- Consumes: Completed Tasks 1-6.
- Produces: A reviewable branch or pull request containing the complete product-curation system.

- [ ] **Step 1: Confirm intended scope and clean worktree**

Run:

```bash
git status -sb
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
```

Expected: only the files named in this plan appear; the working tree has no unstaged changes.

- [ ] **Step 2: Run fresh final verification**

Run:

```bash
python scripts/test_public_safety.py
python scripts/check_public_safety.py --root .
python scripts/test_product_catalog.py
python scripts/check_product_catalog.py --root .
python scripts/test_product_links.py
python scripts/check_product_links.py --root . --timeout 5 --retries 2
git diff --check origin/main...HEAD
```

Expected: all commands exit `0` and all test scripts print their pass messages.

- [ ] **Step 3: Publish for review**

If executing on a feature branch, push it and open a draft PR. The PR body must state what changed, why, the evidence/status boundary, privacy protections, validation commands, and that no real product endorsement was added by the infrastructure change.

```bash
git push -u origin "$(git branch --show-current)"
```

Do not force-push, auto-merge, or mark the PR ready without explicit maintainer direction.
