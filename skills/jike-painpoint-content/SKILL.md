---
name: jike-painpoint-content
description: Turn a solved operational, technical, product, growth, or workflow pain point into a concise, evidence-bounded, platform-neutral methodology draft.
---

# Painpoint Content Writer

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

Create the canonical methodology draft that can later be adapted for Jike, Feishu, or another approved surface. This skill writes content only; it does not log in, publish, create remote documents, or alter platform state.

## Source contract

Use facts already present in the conversation or supplied artifacts. Build from:

- the concrete pain point and context;
- the observable impact or friction;
- attempted approaches and why they failed or were insufficient;
- the final solution and the evidence that it worked;
- advantages, cost, maintenance, risk, and unresolved caveats.

Ask a short targeted question only when a missing fact changes the solution or reproducibility. Never invent metrics, dates, screenshots, quotes, costs, permissions, or outcomes.

## Canonical output

Return a Markdown draft with this order:

1. Result-first title: `如何让/用 <tool> 实现 <result>，并且不再 <common failure>：`
2. A short opening paragraph stating the practical problem and result.
3. One principle sentence and one memorable rule.
4. Two to four concrete usage examples, commands, or decision rules.
5. Five to seven numbered reproduction steps.
6. One short failed-path or detour paragraph.
7. Why the solution is more stable than the obvious alternative.
8. Cost, maintenance, security, and remaining caveats.
9. A closing transformation from the old manual/error-prone workflow to the new stable workflow.

Keep the voice first-person when it reflects the user's experience. Use short paragraphs and high information density. Do not use literal labels such as “痛点一句话” unless the user asks for them.

## Portability and redaction gate

Before a draft can be marked public-ready, separate the transferable mechanism from the author's local environment:

- Keep principles, decision rules, generic commands, placeholders, and verification signals.
- Replace personal proxy nodes, public IPs, proxy ports, hostnames, account names, organization identifiers, local absolute paths, machine-specific aliases, and private URLs with generic placeholders or omit them.
- Do not present the author's exact network route as the solution. Say “use your own approved proxy endpoint” or “set the proxy variables required by your environment.”
- Keep exact personal values only in a private local implementation note; never copy that note into a public post by default.
- A method is not public-ready if a reader would need the author's account, node, secret, or machine path to reproduce it.

## Reproducibility gate

Before returning the draft, verify that a reader can answer:

- What prerequisite state is needed?
- What exact steps or commands should be followed?
- What signal proves the fix worked?
- Which common failure modes should be avoided?
- What should be measured after adoption?
- What is the first useful action if the reader has only 30 minutes?

If a platform-specific step is needed, describe it abstractly and leave the actual platform mutation to `jike-painpoint-sync`.

## Public-safety rules

Strip secrets, OAuth codes, passwords, tokens, private email addresses, internal URLs, customer names, non-public account identifiers, personal network nodes, public IPs, and machine-specific ports. Localhost ports are allowed only as clearly marked placeholders in a private implementation note; public drafts should use `<proxy-port>` or an equivalent variable.

Separate fact, interpretation, and unknown. State a remaining warning as a caveat rather than implying that every diagnostic warning was fixed.

## Regression fixture

Prompt shape: “把一个已解决的 Claude Code 登录问题写成即刻经验贴，但不要发布。” Expected content includes the proxy-vs-auth distinction, the broken shell wrapper as a root cause, portable placeholder-based verification commands, and no authorization code, private account details, personal node, or machine-specific port.
