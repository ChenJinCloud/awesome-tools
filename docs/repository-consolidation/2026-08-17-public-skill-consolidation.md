# Public Skill Repository Consolidation

Date: 2026-08-17

## Decision

`awesome-tools/skills/` is the canonical public source for reusable personal Codex skills. The standalone repositories below are being consolidated here to remove duplicate sources while preserving the complete distributable package.

## Source Mapping

| Original repository | Reviewed commit | Canonical destination | Preserved material |
| --- | --- | --- | --- |
| `ChenJinCloud/codex-closeout-archive` | `9b5bb6077cef2120ec1e2fa30b01eb070a3e4864` | `skills/codex-closeout-archive/` | Skill instructions, agent metadata, helper script, tests, README, changelog, requirements and MIT license |
| `ChenJinCloud/universal-methodology-skill` | `868c74cb6e00b02b01109b378c5a4d14dc759abd` | `skills/universal-methodology/` | Skill instructions, agent metadata, full progression reference and MIT license |

## Version Resolution

The standalone repositories were more complete than the earlier copies in `awesome-tools`, while the locally installed packages had newer instructions. The consolidated package therefore preserves the standalone support files and uses the current installed Skill instructions. Universal Methodology is recorded as v1.2.

`codex-closeout-archive` retains its pytest suite. The root workflow `.github/workflows/skill-tests.yml` runs that suite from its new monorepo path.

## Safety And Deletion Gate

The original repositories may be deleted only after all of the following are true:

- the destination files are committed and pushed;
- the closeout test suite and public-safety checks pass;
- the remote `awesome-tools` branch matches the verified local commit;
- no credential, private record, absolute personal path or generated output is introduced.

Deletion status: pending verification.

