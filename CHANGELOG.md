# Changelog

All notable changes to the spectacular plugin. Semver; bumps are derived from
Conventional Commit types since the last release tag (D-37). Release procedure:
`docs/release.md`; workspace-facing migration steps live in `docs/upgrades.md`
(always a subset of the versions here). Entries before 0.6.0 are backfilled
from commit subjects and upgrade notes; 0.2.0, 0.3.0 and 0.4.1 shipped inside
session commits and have no tags of their own.

## 0.11.1 — 2026-08-19

- Published (D-48): the repo moves to a private GitHub repository shared
  read-only with the team; install is `/plugin marketplace add
  oswalth/spectacular` + `/plugin install spectacular@spectacular`. README
  loses the local-checkout section, gains "Evolving the plugin" (how
  handoff briefs reach this repo — in-chat or as GitHub issues) and now
  references `docs/release.md`; the squash note reads Conventional Commits
  subject + `Task:` footer.
- Plugin-repo `CLAUDE.md`: two-zone rule, Ways of working #1–#9 (moved from
  the design zone so they load on any machine), how a retro round runs
  here, checklists for adding a skill / agent / template, the manual checks
  that stand in for the deferred lint. `design/` is shared with the team as
  the decision log; `tmp.md` (the founding brief, condensed in STATE.md) is
  removed.
- retro: the plugin-repo paragraph names GitHub issues as a brief carrier.
- Manifests: `author`, `repository`, marketplace `description`;
  `docs/release.md` step 5 is the manual-checks step (denylist grep, docs
  regeneration, `claude plugin validate .`).
- No workspace-facing change — nothing to upgrade.

## 0.11.0 — 2026-08-18

- implement reads the capsule by section (D-47, retro-driven): the
  workspace CLAUDE.md joins the capsule; the PRD contributes only the ACs
  the story maps from and the FRs they cite; ADRs contribute Decision
  Outcome, Consequences and Confirmation — Considered Options and Pros and
  Cons are never read; readiness checks read front matter only. Whole ADRs
  and PRDs had been a third of every run's pre-code context.
- implement plans first, then loops (D-47): after the capsule and before
  any further read, lookup or command, a numbered plan (step + check,
  Verification restated as runnable commands) is printed and progress is
  narrated against it; reconnaissance is just-in-time and per step — code
  is read at the step that touches it, never the whole tree; one batched
  lookup per question; a failing gate is the discovery mechanism; rehearse
  outside the repo only when an in-repo failure is expensive to undo; CLIs
  run non-interactively under a timeout. Defined once as **Ways of working
  §5 Just-in-time reconnaissance** in the workspace CLAUDE.md template and
  referenced by implement step 5.
- Repo-level Learnings get a home (D-47): the contract template gains
  `## Toolchain notes` (version pins and blocks, CLI flags and traps, lint
  quirks, layout facts); the landing gate presents Learnings triaged —
  repo-level as a contract diff on the task branch, story-level for the
  task file at close-out; the task template's Learnings comment says so;
  upgrade's drift scan reports a contract missing the section (an empty
  heading is fine).
- docs/models.md gains a Retro evidence section: on a frontier model at
  very high effort, implement deliberated 24–32k tokens before a visible
  plan; the sonnet recommendation for implement stands.

## 0.10.0 — 2026-08-18

- Standalone tasks (D-45, retro-driven): maintenance work with no
  user-visible change — an IaC team-member add, a dependency bump, a
  rotation, a data fix — is a task **without `story:`**; `repo:` +
  Verification make it ready. Written only by plan's new standalone mode
  (`/spectacular:plan "<task>"`), behind one challenge (new or changed
  behavior belongs to a PRD, then a story) and ≤3 clarify questions;
  implement, next and the DoR treat the missing story as "none", no
  acceptance step. PRD → story → task stays the mandatory spine for
  capability delivery.
- Bug flow (D-46, retro-driven): `/spectacular:bug "<what happened>"` files
  a bug report as an artifact — `delivery/bugs/NNN-<slug>.md`, `bug-NNN`,
  `status: open | closed`, `routed_to: []` — mapping the report onto a
  **bug Definition of Ready** (summary, where, steps, actual/expected,
  environment, reproducibility, evidence, regression, related) and
  eliciting the gaps in at most two propose-then-ask rounds; filing is
  never blocked. `/spectacular:plan bug-NNN` triages behind a narrowing
  funnel (front matter + slugs → capped candidate story bodies →
  repo-reader on candidate repos only → overview + touching ADRs; widen only
  on ask), converges or offers 2–3 candidate causes, and routes under one
  gate: violated AC → late acceptance FAIL on that story (returned to
  in-progress, fix tasks, re-tested to a fresh PASS); real work without an
  AC → standalone task(s); not a defect → closed with a Resolution (spec gap
  opens a change proposal). A routed bug stays open until fixed: implement
  closes it when the last routed task lands, the re-acceptance PASS closes
  a story-routed one, next surfaces untriaged / routed / fixed-but-open
  bugs and ranks untriaged ones with lingering drafts. Bugs are never
  implemented directly; no assignee/severity fields (deferred).
- plan's re-plan mode is now **fix** mode: `plan story-NNN "<defect>"`
  handles a defect found after acceptance without a prior FAIL entry.
  Mode is chosen by argument content: `prd-NNN…`/bare → breakdown,
  `story-NNN` → fix, `bug-NNN` → triage, free text → standalone task.
- Workspace CLAUDE.md template gains a "Work outside a PRD breakdown"
  section, the `delivery/bugs/` layout row, bug DoR/DoD, and the bug/
  standalone commit grain; the task template documents the optional
  `story:`; docs regenerated (ten commands, `bug` after `implement`).

## 0.9.0 — 2026-08-12

- Gate protocol + discussion-first (D-41, retro-driven): defined once in the
  workspace CLAUDE.md template, referenced by every gated skill — a gate
  ends with an explicit question naming the decision; only an explicit
  approve-like answer approves; vague go-aheads ("ok", "keep working")
  re-ask; approvals name their scope, partial approval is normal. plan's
  breakdown gains a bounded clarify pass; implement stops and asks when the
  capsule genuinely underdetermines a task; a uniform
  challenge-with-justification line lands at every authoring decision point
  (init generalized, prd, design, plan). Workspaces are self-sufficient by
  design: process rules live in repo artifacts, never one person's session
  memory or machine-local config.
- next sees the whole pipeline (D-42, retro-driven): additionally derives
  **plannable** PRDs (approved, no stories) and **pending decisions** (ADR
  stubs); ready-next lists every available action type; the single
  recommendation ranks across the full ladder — approve/accept/apply →
  implement → plan → decide → develop the next stub — instead of collapsing
  to PRD development when no delivery artifacts exist.
- plan reads sibling truth and takes PRD sets (D-43, retro-driven):
  breakdown context now includes every other approved PRD's front
  matter/scope and all existing stories/tasks; cross-PRD `depends_on` is
  expected wherever ordering is real. One run may break down 2–3
  tightly-coupled PRDs together (combined acyclicity over proposed +
  on-disk items; gate grouped per PRD showing ready-vs-blocked). Execution
  order stays derived, never stored; a set run is not epic trigger 2; bare
  plan suggests a target or coupled set — never all plannable PRDs at once.
- decide map mode (D-44, retro-driven): a bare call scans the approved
  brief, PRD bodies, and plan blockers, and persists the decision backlog
  under a gate as ADR **stubs** — reference, one-line scope, Forced-by
  note, reversal-cost note, suggested order; nothing speculative, re-scans
  only append. ADR status vocabulary becomes stub → draft → approved
  (mirroring PRD stubs, D-20); working `adr-NNN` fills the stub in place.

## 0.8.0 — 2026-08-04

- Landing gate for implement (D-39, retro-driven): the D-26 commit-protocol
  exception is removed — implement no longer commits or pushes on its own.
  Verification green opens a gate: diff summary, verification evidence, and
  both proposed commits (code-repo squash + workspace close-out) are
  presented, and one explicit greenlight lands both. One task = exactly one
  squashed mainline commit stays the grain (D-21); `local-rebase` pushes
  nothing, mainline/workspace pushes stay on explicit ask.
- Upgrade drift scan covers code repos (D-40, retro-driven): the scan now
  walks `.spectacular/registry.md` and checks each repo's
  `.spectacular/contract.md` against the current template; fixes are gated
  per repo as their own `chore(contract): …` commits, structure only. Code
  repos deliberately carry no plugin version pin — the workspace pin covers
  the constellation (P-5).

## 0.7.0 — 2026-08-04

- Repo-bootstrap conventions (D-38, retro-driven): a new code repo's
  engineering conventions are now elicited explicitly at creation, not left
  to chance.
  - Contract template: `## Conventions` is a structured dimension list —
    common core (architecture style, testing, tooling, build & packaging,
    quality gates) plus stack-specific dimensions derived per repo from its
    decided architecture (open list, never limited to the template).
  - plan step 5: repo-bootstrap interview — framed from the forcing ADRs and
    defaults from already-registered repos' contracts; per open dimension,
    options with one recommended + justification, owner picks; answers land
    in the contract before the initial commit. Contested, hard-to-reverse
    dimensions route to `/spectacular:decide`.
  - plan step 5: the new repo's first task is a scaffold task materializing
    the contract, its Verification checking each convention; the UI
    theme-bootstrap task folds into it.
  - implement step 8: contract-amendment path — a convention gap discovered
    mid-work is amended in `contract.md` directly under a gate (rides the
    task branch, or its own `chore(contract):` commit); an amendment
    contradicting an approved ADR needs a superseding ADR + re-plan instead.
  - decide step 1: states the boundary — a convention batch is not one
    forced decision; decide takes a single contested choice among them.

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
