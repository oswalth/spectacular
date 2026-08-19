# Spectacular — build specification (S-3 output; v0.2 revisions folded in)

Drafted 2026-08-01 from the decisions in design/STATE.md (D-1…D-22). STATE.md stays the
decision log; this file holds the skill-level detail needed to build the tracer bullet.
Mechanics tagged **(stated)** were Claude-proposed and ratified in the 2026-08-03 spec
review (OQ-13 → D-23); the tag now only marks provenance. Everything else traces to a
D-number. The S-6 retro round (2026-08-03, D-26…D-30 → v0.2.0) is folded in throughout:
workspace commit protocol, frozen naming-family taxonomy, propose-then-ask
interviewing, deepened decide, brief capability sketch, content-aware retro. The S-6
feedback round (same day, D-31…D-34 → v0.3.0) adds: retro challenges observations, the
design stage (design specs + /spectacular:design), /spectacular:upgrade + upgrade
notes, and the MCP posture (GitHub MCP deferred). D-35 (same day → v0.4.0) adds
design-code import: workspace-resident, git-canonical, provenance-tracked. D-36
(same day → v0.5.0) adds distillation: imported design code yields tokens.json +
design-language.md, the artifacts that actually keep AI-generated UI consistent.
The retro-3 round (2026-08-04, D-39/D-40 → v0.8.0) removes the commit-protocol
exception (implement lands behind a landing gate) and extends upgrade's drift scan
to registered repos' contracts. The retro-5 round (2026-08-18, D-45/D-46 →
v0.10.0) adds work outside a PRD breakdown: standalone tasks (no story) for
maintenance, and the bug flow — bug reports as artifacts, triage as a plan
mode, post-acceptance defects as late FAILs.

## Plugin repo layout (this repo)

```
spectacular/
├── .claude-plugin/                # plugin.json + marketplace.json — the repo is its
│                                  #   own marketplace (D-4, D-24; install flow in README)
├── .claude/                       # repo-boundary PreToolUse hook (Ways of working #7)
├── CLAUDE.md                      # plugin-repo rules: two zones, Ways of working #1–#9,
│                                  #   retro loop, add-a-skill/agent/template, manual
│                                  #   checks (D-48 — self-sufficiency for a team, D-41)
├── skills/<name>/SKILL.md         # the ten skills (D-8: no plain commands;
│                                  #   design + upgrade added by D-32/D-34,
│                                  #   bug by D-46)
├── agents/repo-reader.md          # the one subagent
├── templates/                     # workspace artifact templates (brief, prd, adr,
│                                  #   story, task, bug, change-proposal, contract,
│                                  #   overview, workspace-claude, naming-families)
│                                  #   — single source of each artifact's shape;
│                                  #   added S-5 on Vladimir's feedback;
│                                  #   naming-families (frozen letter taxonomy)
│                                  #   added S-6 (D-27). No epic template (D-19).
├── scripts/                       # docs generator only in v0.1, python3 stdlib
│                                  #   (lint + CI deferred — D-24)
├── docs/                          # published docs (R-7), partly generated (P-6)
├── README.md                      # install / update from the private GitHub repo (D-4),
│                                  #   "Evolving the plugin" (D-48)
└── design/                        # design zone — the plugin's decision log; shared with
                                   #   the team, never shipped publicly (D-12 rev, D-48)
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
├── conventions.md             # optional naming conventions (D-11, D-27: activated
│                              #   families + theme + pools; taxonomy frozen in the
│                              #   plugin's templates/naming-families.md)
├── product/
│   ├── brief.md
│   ├── prds/NNN-<slug>.md
│   └── designs/                   # design truth (D-34, D-35)
│       ├── NNN-<slug>.md          #   design specs: owner-authored UX as truth
│       ├── NNN-<slug>/            #   one spec's imported screen prototypes
│       └── system/                #   product-wide imported design code +
│                                  #   distilled tokens.json / design-language.md
│                                  #   (each import dir carries provenance.md)
├── architecture/
│   ├── overview.md            # living overview; created from template on first use
│   └── decisions/NNN-<slug>.md
├── delivery/
│   ├── stories/NNN-<slug>.md
│   ├── tasks/NNN-<slug>.md    # story tasks and standalone tasks (D-45)
│   └── bugs/NNN-<slug>.md     # bug reports (D-46); NNN-<slug>/ holds evidence files
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
  content, rewritten fresh — D-3.) Conventions is a structured dimension list
  (common core in the template: architecture style, testing, tooling, build &
  packaging, quality gates; stack-specific dimensions added per repo) — filled by
  plan's repo-bootstrap interview at creation, amended in place later (gated,
  never against an approved ADR) — D-38. Plus **Toolchain notes** (D-47): repo-level
  facts every task would otherwise rediscover — version pins and blocks, CLI flags and
  traps, lint quirks, layout facts — written by implement at the landing gate from the
  repo-level share of a task's Learnings; terse, pruned; never decided conventions.

## References and numbering (D-15)

A reference is `<type>-<NNN>`: `prd-001` → `product/prds/001-*.md`, `design-002` →
`product/designs/002-*.md`, `adr-003` →
`architecture/decisions/003-*.md`, `story-004`, `task-012`, `bug-005` likewise. Numbering is
per-type, zero-padded to 3. There is no `id:` front-matter field — the filename is the
identity, so nothing can drift; lint checks that references resolve.

## Front matter and statuses (D-18, D-20, D-22)

| Artifact | Front matter |
|---|---|
| brief | `status: draft \| approved` |
| PRD | `status: stub \| draft \| approved` · `depends_on: [prd-…]` (roadmap graph source) |
| design | `status: draft \| approved` · `prd:` (required) · `sources: [links]` (D-34) |
| ADR | `status: stub \| draft \| approved` · `prd:` (optional — which PRD forced it); stubs persist the decision map (D-44), mirroring D-20 |
| story | `status: todo \| in-progress \| done` · `prd:` (required) · `depends_on: [story-…]` · `epic:` (optional; unused until epic machinery exists — D-19) |
| task | `status: todo \| in-progress \| done` · `story:` (absent on a standalone task — D-45) · `repo:` (registry name) · `depends_on: [task-…]` |
| bug | `status: open \| closed` · `routed_to: [story-… \| task-…]` (the work that fixes it, written by triage — D-46) |
| change | `status: draft \| approved \| applied` · `targets: [refs]` **(stated)** |

Never stored, always derived (P-2): **blocked** (dep not done), **awaiting acceptance**
(story in-progress ∧ all its tasks done — a PASS would have flipped it; a story
reopened by a late FAIL re-enters the same way), bug **untriaged** (open, no
routed_to) / **routed** (fix state read off the targets) / **fixed-but-open**
(all targets done), epic status (from member stories), the roadmap itself.

Story body: goal, acceptance criteria (mapped from the PRD), **Acceptance log**
(`date — who — PASS/FAIL: note`). The task list is NOT duplicated in the story body —
it is derived from task files' `story:` links (P-2).
Task body: description, verification (how "done" is checked — Karpathy #4), **Learnings**
(appended by implement on completion; feeds later capsules — A2; story-level only —
repo-level facts go to the contract's Toolchain notes, D-47).

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

- **Approval gate (stated; protocol per D-41):** the authoring skill presents the
  artifact and asks an explicit question naming the decision; on approval it flips the
  status itself. Only an explicit approve-like answer approves — a vague go-ahead
  ("ok", "keep working") re-asks, silence is never consent, and an approval names what
  it covers (partial approval is normal). Defined once in the workspace CLAUDE.md
  template (## Gate protocol); every gated skill references it. Manual front-matter
  edits are always legitimate — files are the interface. `next` surfaces lingering
  drafts.
- **Workspace commit protocol (D-26):** skills never commit unprompted; every unit of
  work ends with a proposed commit message, committed only on explicit approval.
  Grain: scaffold · approved brief · PRD-map stubs · each developed PRD (+ its change
  proposals) · each ADR + overview update · each plan batch · each retro review's
  fixes. No exceptions since D-39: implement's code-repo commit (one task = one
  squashed mainline commit stays the grain — D-21) lands behind a landing gate, one
  greenlight covering it and the workspace status/Learnings close-out commit.
  Recorded in the workspace CLAUDE.md template so ad-hoc sessions inherit it.
- **Propose-then-ask interviewing (D-28):** init's BA interview and the clarify passes
  in prd, design, decide, and plan frame before asking — synthesis of what's known + a
  strawman, then 2–3 questions referencing the frame, then (init, per topic) a
  confirmed mini-summary. At decision points, owner inputs that would hurt the product
  are challenged — justification plus a proposed alternative, stated explicitly when
  the point stands as-is — never ritually (D-41).
- **MCP posture (D-33, D-34):** the plugin never ships or configures MCP servers.
  Skills use connected MCPs opportunistically and degrade gracefully without them —
  design/implement read Figma frames through a connected design-tool MCP, else plain
  links with owner confirmation. GitHub MCP deferred (STATE.md Deferred).
- **Design-code import (D-35):** ready design code (Claude Design project, exported
  prototype, plain files) is imported into the workspace, git-canonical and
  source-only: product/designs/system/ for product-wide code, NNN-<slug>/ for one
  spec's screens, provenance.md per import dir (source, file map, date, refresh
  procedure). External tool = authoring surface; refresh = gated structural diff.
  Imported code is reference — implement translates to each repo's stack, never
  pastes. Escalation to a dedicated family-U repo has a written trigger (Deferred).
  Distillation (D-36): after import (and every refresh) design derives, gated,
  system/tokens.json (primitive + semantic tokens; each UI repo materializes them
  via a theme-bootstrap first task, contract names the source — plan) and
  system/design-language.md (one-page rules); implement's UI-task capsule always
  carries the distilled pair and opens raw code only on component demand.
  Templates: design-tokens.json, design-language.md.
- **Acceptance flow (D-22):** all tasks done → story is *awaiting acceptance* (derived);
  `next` names it and lists the ACs to test. A human (QA/PO) tests the whole story;
  explicit sign-off flips `done` + logs PASS — a manual edit of the story file, no
  dedicated skill in v0.1; `next` prints exactly what to edit (D-24). On FAIL: log
  the failure, then `plan`
  fix mode — diagnose (repo-reader on suspect repos), propose reopening task(s)
  and/or new fix tasks, gate, apply. Reopened tasks make the story mechanically leave
  awaiting-acceptance. Loop until PASS. A defect found *after* acceptance is a
  **late FAIL** of the same loop (D-46): `plan story-NNN "<defect>"` writes the FAIL
  entry, returns the story to `in-progress`, adds fix tasks under the gate; the story
  is re-tested to a fresh PASS — never assumed fixed.
- **Standalone tasks (D-45):** maintenance work with no user-visible change (IaC
  team-member add, dependency bump, rotation, data fix) is a task **without
  `story:`** — `repo:` + Verification make it ready; written only by plan's
  standalone mode from a free-text argument, behind one challenge (new/changed
  behavior belongs to a PRD, then a story) and ≤3 clarify questions; implemented
  like any task, no acceptance step (Verification is its done); listed by next,
  outside the PRD graph. The spine PRD → story → task stays mandatory for
  capability delivery.
- **Bug flow (D-46):** report → triage → fix. `bug` files `delivery/bugs/NNN-<slug>.md`
  (`open`, `routed_to: []`) — maps what the reporter says onto the bug DoR
  (workspace CLAUDE.md: summary, where, steps, actual/expected, environment,
  reproducibility, evidence, regression, related), elicits gaps in ≤2
  propose-then-ask rounds, files even when gaps remain. `plan bug-NNN` triages
  behind a narrowing funnel (front matter + slugs → candidate stories' bodies,
  capped → repo-reader on candidate repos only → overview + touching ADRs; widen
  only on ask; state what was not examined), ≤5 rounds total, converges or offers
  2–3 candidate causes, then routes under one gate: violated AC → late-FAIL loop
  on that story; real work without an AC → standalone task(s); not a defect →
  closed at triage with a Resolution (spec gap opens a changes/ proposal). One link
  direction — bug.routed_to → fixing work; a routed bug stays open until fixed:
  implement closes it when the last routed task lands, the re-acceptance PASS
  closes a story-routed one, next nudges fixed-but-open. Bugs are never
  implemented directly. No assignee/severity fields (deferred, STATE.md).
- **A4 blocking check** lives in plan (one place in v0.1): every PRD AC maps to ≥1
  story; every story has ≥1 task; every `repo:` exists in the registry; dependency
  graph is acyclic. Plan repairs its own output until the check passes, only then gates.
- **JIT capsule recipe (A2) (stated):** workspace CLAUDE.md + task + its story (goal,
  relevant ACs) + from the PRD only the ACs those story ACs map from and the FRs they
  cite + any open bug routed to the task or its story + architecture overview (whole —
  short by design) + from each ADR touching this repo only Decision Outcome /
  Consequences / Confirmation (Context and Drivers skimmed on need; options analysis
  never) + repo contract (incl. Toolchain notes) + Learnings from prior done tasks of
  the same story. Read by section, not by file — a whole ADR or PRD never enters the
  capsule (D-47). A standalone task skips the story/PRD/design lines. Compiled at
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

## The ten skills

Every skill: runnable in a fresh session, all context from artifacts (A6); ends with at
least one concrete, justified next action naming only commands that exist (R-5, P-3).
Model column = documentation-only recommendation (D-14). Lifecycle order:
init → prd → design → decide → plan → implement → bug → next → retro → upgrade.

### init — opus
Empty directory only (D-6; non-empty → refuse, name the brownfield deferral).
Flow: scaffold (CLAUDE.md embedding Karpathy guidelines + §5 just-in-time reconnaissance
+ commit protocol, README,
profile with plugin version pin, empty registry) → `git init` + proposed scaffold
commit (D-26) → BA interview (problem, users, goals, non-goals, constraints;
propose-then-ask per topic with confirmed mini-summaries — D-28) →
`product/brief.md` (draft; capability sketch 2–4 lines per capability — D-30a) →
optional naming step (D-27: frozen family taxonomy from templates/naming-families.md;
activate families, pick a viability-checked theme, write pools) → approval gate
presenting the depth ladder (D-30a) → proposed closing commit.
Next: approve brief if still draft; then `/spectacular:prd` for the map.

### prd — opus
Precondition: brief approved.
No PRDs yet → propose the PRD map: capabilities, one-line scopes, `depends_on` edges;
gate; on approval write one **stub** PRD per capability (D-20; stubs may carry an
optional Notes-for-development section — D-30b) → proposed commit (D-26).
Stubs exist → pick target (argument, or suggest per roadmap); clarify pass (A3: bounded
structured questions, propose-then-ask — D-28; answers written back into the artifact;
an answer amending the approved brief opens a changes/ proposal in the same session —
D-30b); draft full PRD (requirements, checkable ACs, explicit out-of-scope); gate →
approved → proposed commit.
Next: next stub to develop, `/spectacular:decide` if the PRD forces a decision,
`/spectacular:plan` once approved.

### design — opus
Precondition: target PRD approved. Records owner-authored UX as truth (D-34) — never
generates UX. Flow: pick target (argument, or approved UI-bearing PRD without a spec)
→ context (PRD + brief; inventory frames via connected design-tool MCP, else
owner-provided links — never invent screens) → import ready design code when the
owner has it (D-35: into system/ or the spec's folder, provenance.md, gated refresh
when an import already exists) → clarify pass (≤5, propose-then-ask: flows in scope,
platform conventions, states worth specifying, deliberately undesigned areas) →
draft design-NNN from templates/design.md (flows → screens with sources and states;
cross-cutting pointing into system/; requirement mapping only where design
constrains acceptance; open design questions; a PRD contradiction opens a changes/
proposal) → gate → approved → proposed commit (spec + imported code as one unit).
Next: `/spectacular:plan` for the PRD, or the opened change proposal's approval first.

### decide — opus (fable for foundational, hard-to-reverse ADRs)
Trigger: a forced architecture/technology decision (usually from prd or plan).
Map mode (D-44): a bare call scans the approved brief + PRD bodies + plan blockers
(an empty registry with approved PRDs is itself a forced decision) and persists the
decision backlog, gated, as ADR stubs — reference, one-line scope, Forced-by note,
reversal-cost note, suggested order; nothing speculative, re-scans only append.
Working `adr-NNN` develops a stub in place.
Repo-internal convention batches are NOT one decision — they route to plan's
repo-bootstrap interview; decide takes a single contested one (D-38).
Flow (deepened per D-29): name the decision + its reversal cost (scales the whole
treatment) → clarify pass (≤5 questions on what artifacts don't record) → investigate
(web research; repo-reader — mandatory when hard to reverse) → drivers → options →
trade-off table (+ per-option failure modes when hard to reverse) → owner picks
(never auto-picks) → ADR with every rejected option and why, new external
dependencies decided or named follow-up decisions (no smuggling) → gate → approved →
update `architecture/overview.md` (create from template on first use) **(stated)** →
proposed commit (ADR + overview as one unit — D-26).
Next: back to the blocked prd/plan work.

### plan — sonnet (opus when cross-repo coupling is non-trivial, or a triage spans repos)
plan turns intent into ready tasks and is the only skill that writes them (DoR
enforced in one place). Mode by argument content: `prd-NNN…`/bare → breakdown;
`story-NNN ["<defect>"]` → fix for a known story; `bug-NNN` → fix via triage;
free text → standalone task (D-45/D-46; details in "Cross-cutting mechanics").
Breakdown precondition: every target PRD approved; it takes one PRD or a
tightly-coupled set of 2–3 (D-43) — never all plannable PRDs at once (JIT batches
keep gates reviewable).
Breakdown: read target PRD(s) + overview/ADRs + registry (repo-reader on relevant
repos) + every other approved PRD's front matter/scope + all existing stories and
tasks — cross-PRD `depends_on` expected; execution order stays derived by next,
never stored (D-43) →
clarify pass when the PRD admits materially different breakdowns (D-41) →
propose stories (user-visible slices; AC coverage; `depends_on`, cross-PRD allowed)
and per-story tasks routed per repo → missing repo? propose creation: scaffold sibling dir, `git init`,
contract (owner picks `merge_flow` — D-21), registry entry (D-6); repo-bootstrap
interview fills the contract's Conventions (frame from forcing ADRs + defaults from
registered repos' contracts; common + stack-derived dimensions, open list;
recommended option + justification per question; contested hard-to-reverse dimension
→ decide) and a scaffold first task materializes them, Verification checking each —
theme bootstrap folds in for UI repos (D-38) → epic-trigger check
(above) → A4 blocking check, repair until green → gate → write files (`todo`) →
proposed commit for the batch (D-26).
Fix (D-22, D-46): read the story's acceptance FAIL — or write it from the defect
argument, returning a done story to in-progress — → diagnose with repo-reader →
propose reopened tasks (back to `todo`, note pointing at the failure) and/or new fix
tasks (Verification starts from the reproduction) → gate → apply. From a bug: the
triage funnel and routing above, then the same fix steps.
Standalone (D-45): challenge once → ≤3 clarify questions (repo, Verification,
deps) → task without `story:` → gate → write → proposed commit.
Next: `/spectacular:implement` in the repo of the highest-ranked ready task.

### implement — sonnet (owner escalates to opus after two failed goal-loops)
Runs in a code repo; finds the workspace via `contract.md`.
Flow: select task (argument, or: this repo's tasks with status todo, deps done,
Verification filled; story ready when there is one — standalone tasks have none) →
compile the JIT capsule (by section — D-47) → task `in-progress` (story too, if first)
→ print the numbered plan before any further read, lookup or command (step + check,
Verification restated as runnable commands — Karpathy #4) → branch per task →
goal-driven loop with just-in-time reconnaissance (workspace CLAUDE.md Ways of working
§5, D-47: code read at the step that touches it, never the whole tree; one batched
lookup per question; a failing gate is the discovery mechanism; rehearse outside the
repo only when in-repo failure is expensive to undo; CLIs non-interactive under a
timeout; one line of narration per step) → landing gate (D-39): diff summary +
Learnings triaged (repo-level → contract Toolchain notes on the branch; story-level →
task file) + verification evidence + both proposed commits, explicit greenlight before
anything lands → squash to one commit (CC subject +
`Task: task-NNN` footer — D-37) → mainline per `merge_flow`, history linear →
task `done` + append Learnings → close any open bug whose every routed_to target is
now done (`fixed via task-NNN`; a story-routed bug waits for the re-acceptance PASS)
→ workspace commit for the status/Learnings/bug
edits under the same greenlight (D-26 as amended by D-39; grain per D-21) → if that
was the story's last task: announce *awaiting acceptance* and print the AC checklist
for the human tester (a standalone task has no acceptance step).
A discovered architecture/spec problem becomes `changes/<id>/proposal.md` (draft) —
never a direct edit to workspace truth (A1). A contract-convention gap is amended in
`contract.md` directly, gated — rides the task branch or its own `chore(contract):`
commit; an ADR-contradicting change needs a superseding ADR + re-plan instead (D-38).
Next: next ready task here, or `/spectacular:next` in the workspace.

### bug — haiku (sonnet if the evidence elicitation misses obvious gaps)
Workspace or code repo (via contract). Cheap intake, zero investigation (D-46):
map the argument onto the bug DoR → ≤2 propose-then-ask rounds framed with what
was inferred, only for the gaps; evidence files under `delivery/bugs/NNN-<slug>/`
→ write `bug-NNN` (`open`, `routed_to: []`), unknowns marked, filing never blocked
→ proposed commit `docs(bug-NNN): report — <slug>`.
Next: `/spectacular:plan bug-NNN` (or `plan story-NNN "<defect>"` when the story is
known).

### next — haiku (sonnet if ranking quality disappoints)
Workspace or code repo (via contract). Reads registry + all front matter only — no
bodies except where derivation requires ACs **(stated)**.
Derives: drafts awaiting approval, plannable PRDs (approved, no stories — D-42),
pending decisions (ADR stubs — D-42/D-44), ready vs blocked stories/tasks
(standalone tasks labeled), stories awaiting acceptance, untriaged / routed /
fixed-but-open bugs (D-46), open changes; warns on unresolvable references
(including `routed_to`) or invalid statuses (this is
the only workspace validation in v0.1 — no standalone validator, avoiding speculation's
fixture trap **(stated)**).
Output: roadmap as text (last done → in flight → ready; ready lists every available
action type, never the PRD pipeline alone — D-42) AND a Mermaid graph of PRDs
with story rollup (D-10); candidates from every derived class (approve/accept/close-fixed-bug/triage/apply →
implement → plan → decide → develop stub), ranked by unblocks → reversal cost → size
(speck's ranking, D-3) — untriaged bugs rank with lingering drafts, above new work;
exactly ONE recommendation with justification. In a code repo,
filtered to that repo's tasks.

### retro — haiku (append) / sonnet (review)
Modes chosen by argument CONTENT (D-30c). One short observation → append verbatim
with timestamp to `.spectacular/observations.md`, zero questions, no commit ceremony.
Multi-item argument → split into individual dated entries, confirm once, append all,
offer review. Bare call → review: read observations + evidence, root-cause, propose
workspace-level fixes (applied under gate, then proposed commit — D-26); plugin-level
ideas become handoff briefs kept in the observations file; no observations → offer
interactive capture. Observations are challenged, not just accepted —
confirmed, refined, or overturned explicitly (D-31). Run inside the plugin
repo, review mode IS the R-3 plugin-evolution loop (trigger fired
2026-08-03; manual form).

### upgrade — sonnet
Workspace only (profile.md present). Aligns the workspace with the installed plugin
version (D-32): compare pin vs installed → collect docs/upgrades.md sections from pin
to installed → drift-scan workspace files against current templates (CLAUDE.md
sections; conventions.md vs the frozen taxonomy; .spectacular files; each registry
repo's contract.md vs the contract template — D-40, code repos have no pin of their
own) → propose the
migration set split by ownership (plugin-owned scaffolding: direct gated edits;
approved truth: changes/ proposals, concrete defects only — conformance alone never
rewrites approved truth; code-repo contracts: gated per-repo `chore(contract): …`
commits, structure only) → apply, bump pin → one proposed commit. Equal versions run
the drift scan as a verification pass (D-32 as amended: hand-migrated workspaces can
claim the right pin while missing pieces; findings follow the gated flow, no pin
change). Not its job: validating upgraded skills — the next lifecycle stage does that.
Next: `/spectacular:next`.

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

v0.1 ships NO lint scripts and NO CI (D-24): the owner is the only writer, tests
everything, and the commit protocol (CLAUDE.md Ways of working #6) puts owner review in
front of every commit — that review is the interim guard. The five designed rules below
are deferred as a block; the original trigger (published beyond private personal use)
fired at the 2026-08-19 team share and the owner deferred again (D-48f) — new trigger: a
second person with write access, or a public release. Until then CLAUDE.md "Manual
checks" and docs/release.md step 5 run the checkable subset by hand. Kept here as the
spec of what gets built when the trigger fires:
1. Placeholder allowlist — example names in shipped files must come from the fixed
   vocabulary below (D-12a). (Until the trigger, Vladimir eyeballs example names at
   review time — D-24 note 2.)
2. No-vapor — every `/spectacular:<name>` mention in shipped files must exist in `skills/`.
3. Footer — every SKILL.md ends with a "Next step" section (R-5).
4. Docs-sync — generated docs match `skills/` on disk; the model table has exactly one
   row per shipped skill (R-8).
5. Personal-name denylist (D-12 as revised, D-23) — `design/denylist.txt` (committed
   with the design zone; pilot name added at dogfood time) grepped case-insensitively
   against shipped files only. The rule skips silently when the file is absent — the
   state of a public release, where design/ is excluded (D-12 rev, D-48).
   No local hooks. Until the trigger: checked manually as part of the release
   procedure (OQ-14; step 5 of docs/release.md — D-37).

Docs (R-7): README (hand-written: quickstart + install/update from the private GitHub
repo per the verified flow — `/plugin marketplace add owner/repo`, `/plugin install
spectacular@<marketplace>`, `/plugin marketplace update <marketplace>`; note the
private-repo gotcha: background auto-update needs a credential helper — `gh auth
setup-git` or an ssh-agent-loaded key) + `docs/commands.md` generated from SKILL.md
front matter (`name`, `description`, `argument-hint`), ordered by lifecycle (init →
prd → design → decide → plan → implement → bug → next → retro → upgrade) +
`docs/models.md` — the hand-maintained recommended-model table (single source for
R-8/D-14; reviewed at every retro) + `docs/upgrades.md` — the hand-maintained
per-version workspace migration notes consumed by `/spectacular:upgrade` (D-32).
README must reference every file under `docs/` — no docs file may live
unreferenced by README (D-24).

Placeholder vocabulary (D-12a allowlist, extensible; two-path per D-23, extended by
D-27): generic examples use the descriptive set — product **acme**; workspace
**acme-product**; repos **acme-api**, **acme-web**, **acme-mobile**, **acme-infra**;
people **alex**, **sam** — the default path, since the naming step is optional. The
naming-conventions docs alone use a themed worked example, letter-matched to the
frozen family taxonomy (D-27): product **acme**, theme constellations —
**acme-gemini** (G, workspace), **acme-andromeda** (A, API), **acme-bootes** (B, web
portal), **acme-cassiopeia** (C, mobile app), **acme-hydra** (H, infra), plus
**musca / mensa / monoceros** as M-family pool examples. The pre-D-27 set
(orion / lyra / vega / atlas) stays allowlisted for history. All sets allowlisted.

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
