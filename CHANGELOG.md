# Changelog

All notable changes to the spectacular plugin. Semver; bumps are derived from
Conventional Commit types since the last release tag (D-37). Release procedure:
`docs/release.md`; workspace-facing migration steps live in `docs/upgrades.md`
(always a subset of the versions here). Entries before 0.6.0 are backfilled
from commit subjects and upgrade notes; 0.2.0, 0.3.0 and 0.4.1 shipped inside
session commits and have no tags of their own.

## 0.6.0 — 2026-08-03

- Unified change strategy (D-37): Conventional Commits 1.0.0 across plugin,
  workspace, and code repos; artifact provenance in git-trailer footers
  (`Task: task-NNN`, `Refs: prd-004`), never the subject.
- Tags mark releases only; a commit's version is derived via `git describe`.
  Workspaces carry no versions and no tags. Historical plugin releases
  retro-tagged (v0.1.0, v0.4.0, v0.5.0).
- Version bumps derived from CC types since the last tag (feat → minor,
  fix → patch, breaking → major; workspace-facing ⇒ ≥ minor).
- Code-repo contracts gain `versioning` and `release_flow` fields.
- Added this CHANGELOG and `docs/release.md` (atomic release commit checklist;
  invariant: upgrades.md ⊆ CHANGELOG).
- Commit messages never carry AI-attribution trailers (`Co-Authored-By:
  Claude …`, `Generated with …`) — banned in plugin, workspace, and code
  repos alike.
- Plugin history rewritten once, pre-release, to the CC grammar (local-only
  repo, no consumers); a never-again event once published.
- Reworded commit formats in implement, init, the workspace CLAUDE.md template
  (commit protocol + Task-done DoD), and the spec.

## 0.5.0 — 2026-08-03

- Repo-boundary hook (Ways of working #7): plugin-repo sessions never modify
  project/workspace repos — enforced by a PreToolUse hook.
- Design-code distillation (D-36): imported design code distilled into
  `tokens.json` + `design-language.md`; implement's capsule carries the pair
  for UI tasks; plan wires the tokens source into UI repo contracts.

## 0.4.1 — 2026-08-03

- /spectacular:upgrade: equal pin and installed version no longer dead-ends —
  the drift scan runs as a verification pass (D-32 amendment).

## 0.4.0 — 2026-08-03

- Design-code import (D-35): ready design code imported into the workspace,
  git-canonical, with `provenance.md`; gated refresh.
- /spectacular:upgrade + shipped per-version upgrade notes (D-32).

## 0.3.0 — 2026-08-03

- Design stage (D-34): design specs as truth artifacts under
  `product/designs/`, /spectacular:design records owner-authored UX; plan,
  stories, tasks and the consistency check consume them.

## 0.2.0 — 2026-08-03

- Workspace commit protocol (D-26): nothing committed unprompted; propose →
  owner reviews → commit on explicit approval.
- Frozen naming taxonomy (letter families); deeper decide; retro
  challenge-not-accept rule (D-31); brief capability sketch (D-30).

## 0.1.0 — 2026-08-03

- Tracer bullet: plugin + marketplace manifests, seven lifecycle skills,
  repo-reader agent, standards-based templates, generated docs, README.
