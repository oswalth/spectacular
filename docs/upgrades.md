# Upgrade notes

Consumed by `/spectacular:upgrade` (and readable by humans): for each plugin
version, the workspace-side migration items it introduces. Newest first. A
version with no section requires no workspace changes.

Hand-maintained; every release that changes workspace-facing behavior adds a
section here — written at release time (step 4 of `docs/release.md`), and
every section must have a matching entry in `CHANGELOG.md`.

## 0.12.0

- `CLAUDE.md`: add the **Language** section (name the language your
  artifacts already use — English unless the team chose otherwise), the
  **Fresh before derived** bullet under "How this workspace works", the
  **Housekeeping in a code repo** bullet under "Work outside a PRD
  breakdown", the reworded code-repo footer sentence in **Commit
  protocol** (a task commit carries `Task: task-NNN`, a housekeeping commit
  carries none), and the last bullet of Ways of working §5 (read code
  repos fresh) — copy each from `templates/workspace-claude.md`.
- `.spectacular/registry.md`: add the `remote` column between `path` and
  `role` (`| name | path | remote | role | one-liner |`); fill each row from
  the local clone's `git remote get-url origin` — the upgrade proposes the
  values. `role` is now the area key used by `/spectacular:next <role>` and
  `/spectacular:onboard`: keep it a short stable label shared by the repos
  of one area (api, web, mobile, infra, …).
- Code repos, one change set per repo landed per its `merge_flow` (a PR on
  `pr` repos, one mainline commit on `local-rebase` repos): add `CLAUDE.md`
  from `templates/code-claude.md` (fill repo name, one-liner, role, product
  name, workspace directory — it imports the contract and the workspace
  `CLAUDE.md`; Claude Code asks once per machine to allow the external
  import); give `README.md` the shape of `templates/code-readme.md`, at
  least a **Prerequisites** section — the upgrade proposes its content from
  manifests and the contract's Stack, you confirm. No contract migration.
- No artifact migrations. Scoped `next`, `onboard` and the read-fresh rule
  need nothing from existing artifacts.

## 0.11.0

- `CLAUDE.md`: add **§5 Just-in-time reconnaissance** at the end of
  "Ways of working (Karpathy guidelines)" — copy from
  `templates/workspace-claude.md`. A workspace that already carries a
  locally written §5 realigns its text to the template.
- Code-repo contracts: add the `## Toolchain notes` section (the heading
  and the template's comment; content is written by implement at each
  task's landing gate — an existing repo may seed it from repo-level facts
  sitting in done tasks' Learnings). The drift scan reports the missing
  section; the fix lands per repo as its own `chore(contract): …` commit.
- No task or story migrations: existing Learnings stay where they are.

## 0.10.0

- `CLAUDE.md`: add the **Work outside a PRD breakdown** section (after
  the references paragraph), the `delivery/bugs/` row and the updated
  `delivery/tasks/` row in **Layout**, `bug-005` in the references line,
  the **Bug ready** / **Bug done** definitions under Definitions of Ready
  and Done, "(a standalone task has none)" in **Task ready**, and the
  bug/standalone items in the commit-protocol grain list — copy each from
  `templates/workspace-claude.md`.
- No artifact migrations: existing tasks all carry `story:` and stay
  valid; `delivery/bugs/` is created lazily by the first
  `/spectacular:bug`. Standalone tasks and bug reports appear only when
  you create them.

## 0.9.0

- `CLAUDE.md`: add the **Gate protocol** section and the **Self-sufficient
  by design** bullet under "How this workspace works" — copy both from
  `templates/workspace-claude.md`.
- ADR status vocabulary is now `stub → draft → approved`; existing ADRs
  (`draft`/`approved`) need no change. Optionally run a bare
  `/spectacular:decide` once to persist the decision map as ADR stubs —
  `/spectacular:next` surfaces pending decisions only when stubs exist.
- No other artifact migrations.

## 0.8.0

- `CLAUDE.md`: update the **Commit protocol** section — the
  `/spectacular:implement` exception paragraph is replaced by the
  landing-gate wording; copy from `templates/workspace-claude.md`.
- No artifact migrations. Code-repo contracts gain nothing new; from this
  version the upgrade drift scan itself checks each registered repo's
  `.spectacular/contract.md` against the current template (fixes gated per
  repo). Code repos still carry no plugin version pin.

## 0.7.0

- Code-repo contracts: restructure `## Conventions` to the dimension list in
  `templates/contract.md` (common core + stack-specific dimensions). For an
  existing repo, fill it by asking a workspace session to run the
  repo-bootstrap interview from plan's Missing-repo step against that repo (frame from
  the ADRs that shaped it and other registered contracts, recommended option
  per open dimension), or fill it by hand. New repos get the interview from
  plan at creation.
- No workspace-artifact migrations. Convention gaps found later are amended
  in the contract directly (gated) per implement step 8; only
  ADR-contradicting changes need a superseding ADR.

## 0.6.0

- `CLAUDE.md`: extend the **Commit protocol** section with the Conventional
  Commits grammar, the workspace type/scope mapping, and the
  no-versions/no-tags rule — copy from `templates/workspace-claude.md`.
  Update the **Task done** DoD line to the CC-subject + `Task: task-NNN`
  footer wording.
- Code-repo contracts: add the `versioning:` and `release_flow:` front-matter
  fields (defaults `semver` / `manual`) — copy from `templates/contract.md`.
  New repos get them from plan; existing contracts add them by hand.
- History is not rewritten: existing `task-NNN: …` commits stay as they are;
  the CC grammar applies from this upgrade forward. Workspaces create no tags.
- Commit messages never carry AI-attribution trailers (`Co-Authored-By:
  Claude …`, `Generated with …`) — applies to workspace and code-repo
  commits from this upgrade forward.

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
