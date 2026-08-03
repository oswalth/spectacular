# Spectacular v0.1 — build specification (S-3 output)

Drafted 2026-08-01 from the decisions in design/STATE.md (D-1…D-22). STATE.md stays the
decision log; this file holds the skill-level detail needed to build the tracer bullet.
Mechanics tagged **(stated)** were Claude-proposed and ratified in the 2026-08-03 spec
review (OQ-13 → D-23); the tag now only marks provenance. Everything else traces to a
D-number.

## Plugin repo layout (this repo)

```
spectacular/
├── .claude-plugin/                # plugin.json + marketplace.json — the repo is its
│                                  #   own marketplace (D-4, D-24; install flow in README)
├── skills/<name>/SKILL.md         # the seven skills (D-8: no plain commands)
├── agents/repo-reader.md          # the one subagent
├── templates/                     # workspace artifact templates (brief, prd, adr,
│                                  #   story, task, change-proposal, contract,
│                                  #   overview, workspace-claude) — single source
│                                  #   of each artifact's shape; added S-5 on
│                                  #   Vladimir's feedback. No epic template (D-19).
├── scripts/                       # docs generator only in v0.1, python3 stdlib
│                                  #   (lint + CI deferred — D-24)
├── docs/                          # published docs (R-7), partly generated (P-6)
├── README.md                      # install / update from private GitHub repo (D-4)
└── design/                        # design zone — committed during development,
                                   #   excluded from the released history (D-12 rev, OQ-14)
```

Skills are invoked as `/spectacular:<name>`.

## Workspace layout (created by init — D-15)

```
<workspace>/
├── CLAUDE.md                  # ways of working for sessions here; embeds Karpathy guidelines
├── README.md                  # human orientation
├── .spectacular/
│   ├── profile.md             # container layout (sibling-dir default) + plugin version pin (P-5)
│   ├── registry.md            # code-repo registry: name, relative path, role, one-liner (R-2)
│   └── observations.md        # retro append target (created on first use)
├── conventions.md             # optional naming conventions (D-11)
├── product/
│   ├── brief.md
│   └── prds/NNN-<slug>.md
├── architecture/
│   ├── overview.md            # living overview; created from template on first use
│   └── decisions/NNN-<slug>.md
├── delivery/
│   ├── stories/NNN-<slug>.md
│   └── tasks/NNN-<slug>.md
└── changes/<change-id>/       # A1 delta folders, amend-only (D-17)
```

Directories are created lazily by the skill that first writes into them **(stated)**.
init runs `git init` and makes the initial commit.

## Code-repo side (written by plan at creation/registration)

`<code-repo>/.spectacular/contract.md`

- Front matter: `workspace:` (relative path back — R-2 bidirectional, OpenSpec-Stores
  style), `name:` (registry name), `merge_flow: pr | local-rebase` (D-21; owner picks at
  creation; git history stays linear either way and task branches are ALWAYS squashed —
  gh squash-merge on `pr`, squash + rebase + fast-forward on `local-rebase`. One task =
  exactly one mainline commit, message starting with the task reference: `task-012: …`
  — D-21 as amended).
- Body: stack, commands (build / test / run), conventions. (speck's proven contract
  content, rewritten fresh — D-3.)

## References and numbering (D-15)

A reference is `<type>-<NNN>`: `prd-001` → `product/prds/001-*.md`, `adr-003` →
`architecture/decisions/003-*.md`, `story-004`, `task-012` likewise. Numbering is
per-type, zero-padded to 3. There is no `id:` front-matter field — the filename is the
identity, so nothing can drift; lint checks that references resolve.

## Front matter and statuses (D-18, D-20, D-22)

| Artifact | Front matter |
|---|---|
| brief | `status: draft \| approved` |
| PRD | `status: stub \| draft \| approved` · `depends_on: [prd-…]` (roadmap graph source) |
| ADR | `status: draft \| approved` · `prd:` (optional — which PRD forced it) |
| story | `status: todo \| in-progress \| done` · `prd:` (required) · `depends_on: [story-…]` · `epic:` (optional; unused until epic machinery exists — D-19) |
| task | `status: todo \| in-progress \| done` · `story:` · `repo:` (registry name) · `depends_on: [task-…]` |
| change | `status: draft \| approved \| applied` · `targets: [refs]` **(stated)** |

Never stored, always derived (P-2): **blocked** (dep not done), **awaiting acceptance**
(story in-progress ∧ all its tasks done ∧ not signed off), epic status (from member
stories), the roadmap itself.

Story body: goal, acceptance criteria (mapped from the PRD), **Acceptance log**
(`date — who — PASS/FAIL: note`). The task list is NOT duplicated in the story body —
it is derived from task files' `story:` links (P-2).
Task body: description, verification (how "done" is checked — Karpathy #4), **Learnings**
(appended by implement on completion; feeds later capsules — A2).

Adopted document standards (S-5 research round, ratified 2026-08-03 — D-25):
ADRs follow MADR 4.0 section structure (spectacular front matter and status
vocabulary kept); PRD requirements are FR-NNN with must/should/could priorities,
PRD ACs in EARS form ("WHEN …, THE SYSTEM SHALL …") naming the FRs they verify;
story Goal is the Connextra line, story ACs are Given/When/Then test scripts
mapped from PRD ACs (INVEST as plan's sanity check); task Verification is
structured preconditions/steps/expected; the brief opens with Moore's
positioning statement and init's interview absorbs three SVPG
opportunity-assessment questions (alternatives, why now, success measure);
architecture/overview.md is created from a C4-lite template. DoR/DoD are
UNIFORM process rules — defined once in the workspace CLAUDE.md template for
both stories and tasks, enforced by plan (writes only ready items) and
implement (checks ready before start, walks done at close), never duplicated
into per-item files; the item-specific part of "done" remains the story's ACs
and the task's Verification. All artifact shapes live in templates/ only.

## Cross-cutting mechanics

- **Approval gate (stated):** the authoring skill presents the artifact and asks; on
  approval it flips the status itself. Manual front-matter edits are always legitimate —
  files are the interface. `next` surfaces lingering drafts.
- **Acceptance flow (D-22):** all tasks done → story is *awaiting acceptance* (derived);
  `next` names it and lists the ACs to test. A human (QA/PO) tests the whole story;
  explicit sign-off flips `done` + logs PASS — a manual edit of the story file, no
  dedicated skill in v0.1; `next` prints exactly what to edit (D-24). On FAIL: log
  the failure, then `plan`
  re-plan mode — diagnose (repo-reader on suspect repos), propose reopening task(s)
  and/or new fix tasks, gate, apply. Reopened tasks make the story mechanically leave
  awaiting-acceptance. Loop until PASS.
- **A4 blocking check** lives in plan (one place in v0.1): every PRD AC maps to ≥1
  story; every story has ≥1 task; every `repo:` exists in the registry; dependency
  graph is acyclic. Plan repairs its own output until the check passes, only then gates.
- **JIT capsule recipe (A2) (stated):** task + its story (goal, relevant ACs) + the
  PRD slice those ACs come from + architecture overview + ADRs touching this repo +
  repo contract + Learnings from prior done tasks of the same story. Compiled at
  implement time, never stored.
- **Change flow (D-17):** truth is written directly by init/prd/decide/plan under their
  gates. Only amendments to *approved* artifacts go through `changes/<id>/`
  (proposal.md: why + what deltas). On owner approval the deltas are merged into truth
  and the change marked `applied` in the same session **(stated)**. `next` surfaces
  open changes.
- **Epic triggers (D-19, machinery deferred):** plan checks (1) owner states phased
  delivery, (2) one goal pulls stories from >1 PRD, (3) >~12 stories for one PRD. If
  one fires, plan says so explicitly — that firing IS the build trigger for the epic
  machinery (P-4).

## The seven skills

Every skill: runnable in a fresh session, all context from artifacts (A6); ends with at
least one concrete, justified next action naming only commands that exist (R-5, P-3).
Model column = documentation-only recommendation (D-14).

### init — opus
Empty directory only (D-6; non-empty → refuse, name the brownfield deferral).
Flow: scaffold (CLAUDE.md embedding Karpathy guidelines, README, profile with plugin
version pin, empty registry) → `git init` + first commit → BA interview (problem, users,
goals, non-goals, constraints) → `product/brief.md` (draft) → optional naming step
(D-11: define groups first, then theme suggestion) → approval gate.
Next: approve brief if still draft; then `/spectacular:prd` for the map.

### prd — opus
Precondition: brief approved.
No PRDs yet → propose the PRD map: capabilities, one-line scopes, `depends_on` edges;
gate; on approval write one **stub** PRD per capability (D-20).
Stubs exist → pick target (argument, or suggest per roadmap); clarify pass (A3: bounded
structured questions, answers written back into the artifact); draft full PRD
(requirements, checkable ACs, explicit out-of-scope); gate → approved.
Next: next stub to develop, `/spectacular:decide` if the PRD forces a decision,
`/spectacular:plan` once approved.

### decide — opus (fable for foundational, hard-to-reverse ADRs)
Trigger: a forced architecture/technology decision (usually from prd or plan).
Flow: drivers → options → trade-off table → owner picks (never auto-picks) → ADR with
every rejected option and why → gate → approved → update `architecture/overview.md`
(create from template on first use) **(stated)**.
Next: back to the blocked prd/plan work.

### plan — sonnet (opus when cross-repo coupling is non-trivial)
Precondition: target PRD approved. Two modes.
Breakdown: read PRD + overview/ADRs + registry (repo-reader on relevant repos) →
propose stories (user-visible slices; AC coverage; `depends_on`) and per-story tasks
routed per repo → missing repo? propose creation: scaffold sibling dir, `git init`,
contract (owner picks `merge_flow` — D-21), registry entry (D-6) → epic-trigger check
(above) → A4 blocking check, repair until green → gate → write files (`todo`).
Re-plan (D-22): read the story's acceptance FAIL → diagnose with repo-reader → propose
reopened tasks (back to `todo`, note pointing at the failure) and/or new fix tasks →
gate → apply.
Next: `/spectacular:implement` in the repo of the highest-ranked ready task.

### implement — sonnet (owner escalates to opus after two failed goal-loops)
Runs in a code repo; finds the workspace via `contract.md`.
Flow: select task (argument, or: this repo's tasks with status todo, deps done) →
compile the JIT capsule → task `in-progress` (story too, if first) → goal-driven loop
(Karpathy #4: define verification first, loop until it passes) → branch per task →
squash to one commit (`task-NNN: …`) → mainline per `merge_flow`, history linear →
task `done` + append Learnings → if that
was the story's last task: announce *awaiting acceptance* and print the AC checklist
for the human tester.
A discovered architecture/spec problem becomes `changes/<id>/proposal.md` (draft) —
never a direct edit to workspace truth (A1).
Next: next ready task here, or `/spectacular:next` in the workspace.

### next — haiku (sonnet if ranking quality disappoints)
Workspace or code repo (via contract). Reads registry + all front matter only — no
bodies except where derivation requires ACs **(stated)**.
Derives: drafts awaiting approval, ready vs blocked stories/tasks, stories awaiting
acceptance, open changes; warns on unresolvable references or invalid statuses (this is
the only workspace validation in v0.1 — no standalone validator, avoiding speculation's
fixture trap **(stated)**).
Output: roadmap as text (last done → in flight → ready) AND a Mermaid graph of PRDs
with story rollup (D-10); ranks ready work by unblocks → reversal cost → size (speck's
ranking, D-3); exactly ONE recommendation with justification. In a code repo, filtered
to that repo's tasks.

### retro — haiku (append) / sonnet (review)
Append: one observation + timestamp to `.spectacular/observations.md`; zero questions.
Review: read observations + evidence, root-cause, propose workspace-level fixes
(applied under gate); plugin-level ideas become handoff briefs kept in the observations
file. The full R-3 plugin-evolution loop stays deferred (trigger: first accumulated
pilot observations).

## Subagent: repo-reader — sonnet

Read-only. Input: repo path + a specific question. Output: findings relevant to that
question (architecture, capabilities, integration points). Never writes. Dispatched by
prd / decide / plan.

Deferred, design settled (see STATE.md Deferred): a commit-hash-keyed cache at
`<code-repo>/.spectacular/summary.md` — repo-reader stamps its findings with the HEAD
hash it read; on the next dispatch, HEAD unchanged → reuse, changed → re-derive from
the diff since the stamp. Mechanically invalidated, never discipline-maintained.
Build trigger: retro observations of repeated costly scans.

## Lint and docs (P-3, P-6, D-12; enforcement deferred — D-24)

v0.1 ships NO lint scripts and NO CI (D-24): Vladimir is the only user, tests
everything himself, and the commit protocol (STATE.md Ways of working #6) puts his
review in front of every commit — that review is the interim guard. The five designed
rules below are deferred as a block; written trigger: the repo is published beyond
private personal use. Kept here as the spec of what gets built when the trigger fires:
1. Placeholder allowlist — example names in shipped files must come from the fixed
   vocabulary below (D-12a). (Until the trigger, Vladimir eyeballs example names at
   review time — D-24 note 2.)
2. No-vapor — every `/spectacular:<name>` mention in shipped files must exist in `skills/`.
3. Footer — every SKILL.md ends with a "Next step" section (R-5).
4. Docs-sync — generated docs match `skills/` on disk; the model table has exactly one
   row per shipped skill (R-8).
5. Personal-name denylist (D-12 as revised, D-23) — `design/denylist.txt` (committed
   with the design zone; pilot name added at dogfood time) grepped case-insensitively
   against shipped files only. The rule skips silently when the file is absent — which
   is exactly the state of the released repo, since design/ is excluded at release.
   No local hooks. Until the trigger: checked manually as part of the release
   procedure (OQ-14).

Docs (R-7): README (hand-written: quickstart + install/update from the private GitHub
repo per the verified flow — `/plugin marketplace add owner/repo`, `/plugin install
spectacular@<marketplace>`, `/plugin marketplace update <marketplace>`; note the
private-repo gotcha: background auto-update needs a credential helper — `gh auth
setup-git` or an ssh-agent-loaded key) + `docs/commands.md` generated from SKILL.md
front matter (`name`, `description`, `argument-hint`), ordered by lifecycle (init →
prd → decide → plan → implement → next → retro) + `docs/models.md` — the
hand-maintained recommended-model table (single source for R-8/D-14; reviewed at
every retro). README must reference every file under `docs/` — no docs file may live
unreferenced by README (D-24).

Placeholder vocabulary (D-12a allowlist, extensible; two-path per D-23): generic
examples use the descriptive set — product **acme**; workspace **acme-product**; repos
**acme-api**, **acme-web**, **acme-mobile**, **acme-infra**; people **alex**, **sam** —
the default path, since the D-11 naming step is optional. The naming-conventions docs
alone use a themed worked example demonstrating groups-then-theme: product **acme**,
theme constellations — **orion** (api), **lyra** (web), **vega** (mobile), **atlas**
(infra). Both sets are allowlisted.

## Pre-build notes — ratification record (2026-08-03, D-24)

The five S-4.5 pre-build notes were reviewed by Vladimir; surviving mechanics are
folded into the sections above. Outcomes:

1. Marketplace manifest — approved (plugin layout; README install/update flow with
   the credential-helper gotcha, see "Lint and docs" docs paragraph). The
   marketplace.json fields verified against CC docs: `name`, `owner.name`,
   `plugins: [{name, source: "./"}]`.
2. Placeholder-allowlist lint — removed from v0.1; Vladimir eyeballs example names at
   review time. The same feedback introduced the commit protocol (STATE.md Ways of
   working #6).
3. Acceptance recording as a manual story-file edit — approved (folded into the
   acceptance-flow mechanics). Trigger for more machinery: retro friction (P-4).
4. Docs generation from `name`/`description`/`argument-hint` frontmatter — approved
   (the `model:` field exists and stays deliberately unused — D-14), plus the new
   rule: README references every file under docs/.
5. Lint + CI as a whole — deferred to publication (D-24; see "Lint and docs" and
   STATE.md Deferred). S-5 build order: scaffold + manifests → skills in lifecycle
   order (init → prd → decide → plan → implement → next → retro) → repo-reader →
   docs generator + generated docs + README last (they need the skills on disk).

## Tracer bullet — definition of done (P-1)

On the pilot (specifics arrive in-chat at dogfood time — D-13): init → brief approved →
PRD map → ≥1 PRD approved → plan → ≥1 code repo created with contract → implement →
≥1 task merged per participating repo → ≥1 story through a human acceptance PASS →
retro append used ≥1×, next used throughout. Every stage crude; **no stage gets
deepened until this loop has closed** (P-1). decide and changes/ run only if the pilot
forces them.
