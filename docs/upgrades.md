# Upgrade notes

Consumed by `/spectacular:upgrade` (and readable by humans): for each plugin
version, the workspace-side migration items it introduces. Newest first. A
version with no section requires no workspace changes.

Hand-maintained; every release that changes workspace-facing behavior adds a
section here.

## 0.5.0

- `CLAUDE.md`: update the `product/designs/` Layout row to the wording in
  `templates/workspace-claude.md` (adds the distilled `tokens.json` /
  `design-language.md`).
- Workspaces with imported design code: **distill it** — run
  `/spectacular:design` for the relevant PRD (its import step now distills),
  or ask a workspace session to distill the imported code in
  `product/designs/system/` into `tokens.json` and `design-language.md` per
  the plugin's templates. UI repo contracts gain the tokens pointer and a
  theme-bootstrap first task at plan time.

## 0.4.0

- `CLAUDE.md`: update the `product/designs/` Layout row to the wording in
  `templates/workspace-claude.md` (design specs + imported design code).
- No artifact migrations. Ready design code (e.g. a Claude Design project)
  is imported by `/spectacular:design` step 3 — git-canonical under
  `product/designs/system/` or a spec's own folder, with `provenance.md`.

## 0.3.0

- `CLAUDE.md`: add the `product/designs/` row to Layout, the `design-NNN`
  reference example, and the designed-UI clause to **Story ready** — copy all
  three from `templates/workspace-claude.md`.
- No artifact migrations. Design specs are new: a UI-bearing approved PRD gets
  one via `/spectacular:design` before its next `/spectacular:plan` run (the
  owner may explicitly plan without one).

## 0.2.0

- `CLAUDE.md`: add the **Commit protocol** section — copy from
  `templates/workspace-claude.md`.
- `conventions.md` (only if the naming step was taken): realign to the frozen
  taxonomy in `templates/naming-families.md` — every activated letter must
  carry its frozen family meaning; pools move to their letter's rightful
  family; record the migration in a History section. Codenames already in use
  are never renamed silently — surface any conflict to the owner.
- Brief: the template now carries a "Product shape (capability sketch)"
  section (2–4 lines per capability). Amend an approved brief only via
  `changes/` and only where the old thinness hides a real gap.
- Draw missing git lines: any artifacts left uncommitted by v0.1 skills are
  committed as logical units (map, each PRD, each ADR + overview) under the
  commit protocol.

## 0.1.0

Baseline — no migrations.
