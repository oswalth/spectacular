# Spectacular — design state

Single source of truth for the design phase of **spectacular**, the third attempt at a
Claude Code plugin for AI-assisted SDLC (idea → brief → PRDs → architecture → breakdown →
implementation → release), after two failed attempts: `../speculation` (v0.3.0) and
`../speck` (v0.2.1). The original brief is `../spectacular/tmp.md`; this file condenses it.

Read this file top to bottom and you are fully caught up — the only satellite files are
design/karpathy-guidelines.md (working principles) and design/spec.md (S-3 build spec).
Update it at the end of every design session: move settled items into Decisions, refresh
Open questions, append to the Session log. It must never contradict what was agreed in
conversation.

## How to resume in a fresh session

Open Claude Code in this repo and paste:

> Read design/STATE.md end to end, then design/spec.md — together they are the
> complete design context for the spectacular plugin. Follow STATE.md's "Ways of
> working". Design is complete; execute the next entry in the Session plan
> (S-5: build the tracer bullet per spec.md). Do not
> re-derive settled Decisions and do not re-explore ../speck or ../speculation
> beyond what this file records. Before the session ends, update STATE.md.

## Ways of working (from Vladimir's brief)

1. Always ask for clarification; never assume.
2. Do not overcomplicate.
3. Follow the Karpathy guidelines — full text in design/karpathy-guidelines.md
   (think before coding · simplicity first · surgical changes · goal-driven execution).
4. Plan for context rot: this file is the mechanism.
5. This directory is the plugin repo.
6. Commit protocol (added 2026-08-03): Claude never commits or pushes on its own.
   Flow: make changes → suggest a commit message → Vladimir reviews the diff and
   approves or challenges → commit (and push) only on his explicit ask.

## Requirements (given in the brief — challengeable, but not to be silently dropped)

- R-1 Targets Claude Code (fixed, NOT challengeable).
- R-2 Multi-repo model: one workspace repo (product docs, PRDs, architecture,
  epics/stories) plus zero or more code repos; bidirectional linkage; sibling-directory
  default; optional GitHub MCP for reading remote main branches.
- R-3 The plugin evolves via recorded feedback: capture friction in a project repo, hand
  it to the plugin repo, update, push, prompt the user to reload.
- R-4 Project bootstrap creating the main files (README, docs, CLAUDE.md, …).
- R-5 Every command ends by suggesting at least one concrete next action, with
  justification. No command leaves the user guessing.
- R-6 Small command set; add commands only when a real need appears.
- R-7 Published, human-friendly documentation kept in sync with actual plugin files
  (install / usage / update; commands ordered by project lifecycle).
- R-8 (added 2026-07-31) Every command documents a recommended model (haiku / sonnet /
  opus / fable): cheapest that works, upgraded only where the quality gain is
  significant and failure is costlier than the token premium. Escalation evidence
  comes from retro observations (R-3 loop). Per-component enforcement mechanics:
  OQ-12.

## Evidence: post-mortem of the two predecessors (explored 2026-07-30)

### Shared fatal pattern
Both attempts polished the planning front half (foundation / PRD / decide) and never
built the delivery back half (breakdown / implement). The chain FND → PRD → ADR worked;
no story, task, or line of product code was ever produced through either plugin. Both
repos contain honest post-mortems diagnosing overbuild in their predecessor — then
partially repeated it. Conclusion: the discipline must be structural (lint/CI), not
aspirational.

### speculation (first attempt, v0.3.0, 135 files)
- 10 artifact prefixes, 9 approval gates; ~75% of files are broken-workspace fixtures
  for a 12-rule validator — validating artifacts no installed command could produce.
- Built: bootstrap-project, foundation, prd, decide, next, validate, retrospective,
  improve-workflow. Never built: stories, decompose, implement, register-repo.
- Pilot leakage: fictional pilot "zulu"/"zulu-api" baked into schemas and fixtures.
- Docs out of sync with disk (uncommitted skills; README counts wrong).
- Genuinely good: lint rules making hallucination structural — the operating model may
  name zero commands; every skill must end with "## Next step"; /next reads the real
  skills dir and prints "no command yet" instead of inventing one. Derived state.

### speck (second attempt, v0.2.1, 22 files, in live use at WardX workspace `gdansk`)
- 8 skills with a uniform shape (Purpose → Steps → Gate → Next step). Artifact chain
  FND → PRD → EPIC → STORY → TASK, six deep — never produced a story.
- Never built: breakdown, implement, evolve — referenced ~18 times as "not built yet".
- Pilot leakage: real client name (WardX/gdansk, absolute paths) in README, skills,
  CHANGELOG, design notes.
- Genuinely good (carry forward): state derived from artifact front matter, never
  stored; /speck:next reads front matter only and ranks by unblocks → reversal cost →
  size; "long fuse" items (waiting on external answers) surfaced separately; two-mode
  /retro (cheap append vs. full review); "recommend only what exists" guard;
  "deliberately left out" table where every deferred feature has a written trigger;
  register-repo writing per-repo contracts plus a workspace registry.

### Mapping to the six failure reasons in the brief
1. Too complicated, never reached development → confirmed; root cause is build order
   (planning depth before pipeline breadth), not the artifact model itself.
2. No workspace↔code linkage → designed in both, register-repo even built in speck,
   but never exercised because implement never existed.
3. Hallucination / example project treated as basis → both leaked pilot names into
   shipped plugin content; the fix is lint-enforced placeholders, not carefulness.
4. Commands ending without next actions → solved well by both (footers + derived
   /next); adopt, don't redesign.
5. Suggesting non-existent commands → speculation's structural approach (scripts read
   the real skills dir) beats speck's disciplined "not built yet" annotations.
6. Unclear PRD/architecture ordering; want a roadmap graph → real gap; speck's phase
   derivation is the seed; the branching-graph view is still to design (OQ-9).

## Framework research (S-2, 2026-07-30): BMAD v6.10 · spec-kit v0.15 · OpenSpec v1.7

All three MIT, very active, tool-agnostic. None natively handles multi-repo products —
OpenSpec's "Stores" (beta) comes closest and independently validates our workspace-repo
model: the planning repo is plain git, the tool NEVER auto-syncs, code repos hold an
explicit pointer to it. Recurring community criticism of all three: heavy artifact
volume before code ("illusion of work" — our failure #1 by another name), advisory-only
quality gates, spec/code drift. BMAD's persona "agents" are conversational personas
(main-session prompts), not subagents.

Adoption candidates (A-x; ALL ADOPTED — D-9):
- A1 OpenSpec change model — specs/ is current truth per capability; changes/<id>/ are
  delta folders (ADDED/MODIFIED/REMOVED …); apply, then merge deltas into truth, then
  archive. Replaces speck's 209-line change taxonomy with a mechanical flow.
- A2 BMAD JIT context capsule — compile a task's context bundle (PRD slice,
  architecture, repo contract, prior-task learnings) at implement time, not planning
  time; avoids staleness; fits multi-repo (compiled from workspace, consumed in a code
  repo). BMAD claims ~90% token savings vs upfront embedding.
- A3 spec-kit clarify — a bounded structured-question gate whose answers are written
  back into the artifact (Karpathy #1, mechanized).
- A4 Blocking consistency check — spec-kit analyze / BMAD implementation-readiness
  cohesion check, made BLOCKING per P-3 (advisory-only is their observed weak point).
- A5 Proportionality valve — OpenSpec skip_specs / BMAD path routing: small changes may
  legitimately skip the full pipeline (counters failure #1).
- A6 Fresh-session doctrine (BMAD) — every skill must be runnable in a fresh session,
  pulling all context from artifacts. Corollary of P-2; adopted without debate.
Rejected as principle-contradicting: BMAD's 34-workflow/6-persona surface and stored
sprint-status.yaml (violates P-2, R-6); spec-kit's mandatory full pipeline and ~800
lines of markdown per feature; non-blocking gates; single-repo/branch-per-feature
assumptions.

## v0.1 command set (scope approved — D-10; specified in design/spec.md — S-3)

Skills (user-facing, main session; each ends with a justified next step — R-5):
1. init — in an empty workspace dir: scaffold (CLAUDE.md, README, profile, registry) +
   BA interview → product brief. Optional naming-conventions step per D-11 (theme
   suggested from the product idea).
2. prd — propose the PRD map first (gated), then one PRD at a time with a clarify pass
   (A3); checkable acceptance criteria; explicit out-of-scope.
3. decide — just-in-time ADR: drivers → options → trade-off table → owner picks
   (speck's shape, kept).
4. plan — PRD → stories → tasks routed per repo; proposes creating missing code repos
   (greenfield, D-6): scaffold + contract + registry entry.
5. implement — in a code repo: pick/receive a task, compile the JIT context capsule
   (A2) from the workspace, goal-driven loop (Karpathy #4), update task status; a
   discovered architecture change becomes a delta proposal (A1), never a direct edit
   to workspace truth.
6. next — derived state (P-2): dependency graph ready/blocked + one ranked
   recommendation with justification; renders the roadmap as text + Mermaid (OQ-9).
7. retro — two-mode (cheap append / full review). The full plugin-evolution loop (R-3)
   has a written trigger: first accumulated observations from the pilot.

Subagents: repo-reader — reads a code repo, reports architecture/capabilities relevant
to a stated question; dispatched by prd/decide/plan. Nothing else in v0.1.
Scripts: docs generator only (P-6). Lint + CI deferred to publication (D-24). No plain
commands at all.

## Deferred, with triggers (P-4 discipline)

- Epic machinery (semantics settled in D-19): plan's epic-trigger check firing on the
  pilot for the first time is the build trigger. Until then no epic files, no epic:
  fields in use.
- Repo-summary cache for repo-reader (design settled 2026-08-03; recorded in
  spec.md): commit-hash-keyed cache at <code-repo>/.spectacular/summary.md —
  findings stamped with the HEAD hash read; reused on match, re-derived from the
  diff on mismatch; never discipline-maintained (that would be stored state
  vulnerable to drift, contra P-2). Trigger: retro observations of repeated costly
  repo-reader scans on the pilot.
- Task-level model recommendation: plan could stamp a recommended model per
  story/task based on the task's own complexity. Vladimir's explicit concern,
  deliberately deferred — needs research on model↔task-type fit plus real
  cost/quality data. Trigger: tracer bullet complete AND retro observations about
  implement cost/quality exist.
- Brownfield onboarding (per D-6). Trigger: a real existing-product need after the
  pilot proves the greenfield path.
- Full plugin-evolution loop (R-3) beyond retro's append mode. Trigger: first
  accumulated retro observations from the pilot.
- Lint + CI (all five designed rules kept in spec.md "Lint and docs": placeholder
  allowlist, no-vapor, footer, docs-sync, denylist grep). Deferred by D-24 —
  Vladimir tests everything himself for now; the commit protocol (Ways of working
  #6) is the interim guard, and the denylist is checked manually as part of the
  release procedure (OQ-14). Trigger: the repo is published beyond private
  personal use (team share or public).

## Reference: lean AI-assisted SDLC order (corrected)

1. Product brief — problem, users, goals, non-goals, constraints. One doc. (No separate
   "PDD" needed.)
2. PRDs — one per capability, with checkable acceptance criteria and explicit
   out-of-scope.
3. Architecture — not a phase: one living architecture overview per system, plus ADRs
   written just-in-time when a PRD forces a decision. A separate "ARD" is enterprise
   ceremony; skip it.
4. Delivery breakdown — epics only if scale demands them → stories (user-visible
   slices) → tasks (one repo's share of a story).
5. Implementation — in code repos: task → branch → code + tests → PR.
6. Verification — repo tests plus an acceptance check against story/PRD criteria.
7. Release — versioning / changelog / deploy, per repo kind.
Cross-cutting, any time: retro/feedback (product and process), derived roadmap / next.

## Decisions

- D-1 (2026-07-30, resolves OQ-1) Pilot: a brand-new pet project — real stakes without
  work-project blast radius. Which project: OQ-11.
- D-2 (2026-07-30, resolves OQ-2) Build order: tracer bullet — confirms P-1.
- D-3 (2026-07-30, resolves OQ-3) Speck posture: carry the proven mechanisms
  (catalogued in the evidence section) but write every file fresh in this repo; no
  forking, no clean room.
- D-4 (2026-07-30, resolves OQ-4) Distribution: private GitHub repo, used by Vladimir
  only at first; shared with the team if it proves out. No public marketplace for now.
  Implication: install/update flow must work from a private GitHub repo.
- D-5 (2026-07-30) Principles P-2…P-6 adopted as written — all six principles active.
- D-6 (2026-07-30, resolves OQ-8) v0.1 is greenfield only: new workspace, new code
  repos, all created through the plugin. Brownfield support needs a written trigger
  (P-4) to earn its way in.
- D-7 (2026-07-30, resolves OQ-5) No speck compatibility constraint. If spectacular
  proves out on the pilot, a one-off gdansk migration gets written later.
- D-8 (2026-07-30) Unit mapping: every user-facing workflow step is a skill (main
  session, can interview); subagents only as silent read-only workers dispatched by
  skills; lint and docs-sync are deterministic scripts run in CI; no plain commands.
- D-9 (2026-07-30) Adoptions A1–A6 all adopted (see Framework research).
- D-10 (2026-07-30, resolves OQ-9) v0.1 command set scope approved as listed below.
  next renders the roadmap both as text (last done → current → ready actions with
  justification) and as a Mermaid graph.
- D-11 (2026-07-30, refined 2026-07-31, resolves OQ-10) Naming conventions: optional
  init step. Order of operations: the step first defines the GROUPS (letters) this
  project might plausibly need, each with a description of what belongs in it; then
  init suggests a theme derived from the product idea (trading platform →
  ports/trading cities; language-learning app → world languages; …) such that every
  DEFINED group genuinely has 5–10 candidate names. Letters outside the defined
  groups are unreserved — the user may activate them later, with the understanding
  that supplying candidates for them is then the user's responsibility. Group
  definitions live in the project workspace's conventions file; the plugin ships only
  the template and the suggestion logic (P-5).
- D-12 (2026-07-31) Two-zone repo. (a) Shipped plugin content — skills/, scripts/,
  docs/, README, .claude-plugin/ — impersonal from day one; examples use a fixed
  placeholder vocabulary, lint-enforced (P-3). (b) Design zone — design/, tmp.md —
  personal by nature (it names the predecessors, WardX, the failures) and NEVER
  enters git: .gitignore'd before the first commit. The repo has no git history yet,
  so nothing needs scrubbing; the published repo will never contain a byte of the
  design zone.
  Refined 2026-07-31: gitignore alone is NOT the guarantee — shipped content itself
  must be checked. Two lint layers: (a) PUBLIC structural lint, shipped and run in
  CI — example/project names in any shipped file must come from a fixed placeholder
  allowlist, plus the no-vapor-commands and next-step-footer rules; (b) PRIVATE
  personal-name denylist (wardx, gdansk, speck, speculation, pilot name once known,
  …) living in the design zone and run locally before every push — it cannot ship,
  because committing the denylist would itself leak the names.
  Revised 2026-08-03 (with D-23): version control starts immediately and the design
  zone IS committed during development, to track session-to-session iterations. The
  no-leak guarantee moves from gitignore to the release procedure — the released
  v0.1 history must contain no design-zone bytes; exact mechanics parked as OQ-14.
  The denylist is therefore now a committed design-zone file (design/denylist.txt)
  checked by a plain CI grep over shipped files only — no local hooks; it vanishes
  at release with the rest of design/, so it still never ships.
  Amended 2026-08-03 (D-24): the CI grep, like all lint/CI, is deferred to
  publication; until then the denylist file stays committed and is checked manually
  at release time.
- D-13 (2026-07-31, supersedes OQ-11's "record the pilot" intent) Pilot details never
  enter the spectacular repo at all — not even the design zone. The plugin design is
  project-blind; pilot specifics are provided in conversation only at dogfood time,
  in the pilot's own workspace directory. Any shape question that matters for design
  is asked and answered abstractly. Allowed abstract categories (refined 2026-07-31):
  repo count and kinds, ways of working, MCP integrations (GitHub, Jira, Figma, …).
  Never the brief, the idea, the domain, or any naming.
- D-14 (2026-07-31, resolves OQ-12; revised same day) Model guidance is
  RECOMMENDATION-ONLY, carried in the plugin's documentation — never hardcoded into
  skills or subagents. Everything inherits the session model; the user always
  chooses. The generated docs (R-7) include a per-command recommended-model table
  (draft below), reviewed at every retro; escalation is the user's decision,
  evidenced by retro observations — no auto-ladder. Verified facts kept for
  reference: skills and subagents technically support `model:` frontmatter pins
  (aliases haiku/sonnet/opus/fable; a skill's pin lasts only until the next user
  prompt; a subagent's is fixed per definition; fable needs CC ≥ 2.1.170) —
  spectacular deliberately uses none of them in v0.1.

  Model tiering draft (refine in S-3; review at every retro — the model landscape
  moves): init/prd/decide → opus (judgment-dense, low volume, huge downstream blast
  radius; fable reserved for foundational hard-to-reverse ADRs) · plan → sonnet, opus
  when cross-repo coupling is non-trivial · implement → sonnet, escalate to opus when
  a task fails its goal-driven loop twice · next → haiku, sonnet if ranking quality
  disappoints · retro → haiku (append) / sonnet (review) · repo-reader subagent →
  sonnet, haiku variant only if inventory-style questions prove common.

- D-15 (2026-08-01) Workspace layout: lifecycle dirs — product/ (brief, prds/),
  architecture/ (overview, decisions/), delivery/ (stories/, tasks/), changes/, plus
  .spectacular/ (profile, registry, observations) and optional conventions.md. Code
  repos carry .spectacular/contract.md with a workspace back-pointer (R-2). References
  are derived from paths (`prd-001` → product/prds/001-*.md); no id: field to drift.
  Full tree: design/spec.md.
- D-16 (2026-08-01) Tasks are separate files (delivery/tasks/NNN-slug.md) with their
  own front matter — uniform P-2 derivation; implement addresses one task file for the
  A2 capsule. Not embedded in story bodies.
- D-17 (2026-08-01) A1 scope in v0.1 is amend-only: init/prd/decide/plan write truth
  directly under their gates; changes/ is used solely to amend already-approved
  artifacts (change status: draft → approved → applied).
- D-18 (2026-08-01) Two status vocabularies, lint-enforced: truth artifacts draft →
  approved (PRDs add an initial `stub` — D-20); delivery artifacts todo → in-progress
  → done. "Blocked" and "awaiting acceptance" are always derived, never stored; epics
  store no status at all.
- D-19 (2026-08-01) Delivery hierarchy: PRD → story → task is the mandatory spine
  (story.prd and task.story/task.repo required). PRD = durable spec of a capability
  (never "done", amended via A1); epic = closable delivery batch. Epics are adopted as
  plugin-proposed containers under three mechanical triggers owned by plan (phased
  delivery of one PRD; one goal spanning >1 PRD; >~12 stories per PRD) — never a
  per-project judgment call. Epic status is always derived from member stories.
  Machinery deferred (see Deferred).
- D-20 (2026-08-01) The PRD map is persisted as stub PRDs: map approval writes one PRD
  file per capability (status: stub, one-line scope, depends_on filled). The roadmap
  graph has exactly one source — PRD front matter.
- D-21 (2026-08-01) Merge flow is a per-repo contract choice made at repo creation:
  `pr` (via gh) or `local-rebase`. Git history stays linear either way (rebase-based;
  Vladimir's explicit preference). implement always branches per task, then follows
  the contract.
  Amended 2026-08-03: always squash — one task = exactly one mainline commit
  (gh squash-merge on pr; squash + rebase + fast-forward locally). The squashed
  commit message starts with the task reference (task-NNN: …), anchoring R-2
  linkage in mainline history.
- D-22 (2026-08-01) Story "done" is set only by explicit human acceptance: when all
  tasks are done the story is derived-awaiting-acceptance; QA/PO tests the whole
  story's ACs; sign-off flips done and logs PASS in the story's Acceptance log. On
  FAIL: log it, then plan's re-plan mode (gated) diagnoses via repo-reader and
  proposes reopening tasks and/or new fix tasks. Loop until PASS.
- D-24 (2026-08-03) S-4.5 pre-build notes ratified with changes. Approved: marketplace
  manifest (note 1); acceptance sign-off as a manual story-file edit, no dedicated
  skill (note 3); docs generation from name/description/argument-hint plus a new
  rule — README must reference every file under docs/, none may live unreferenced
  (note 4). Changed: the placeholder-allowlist lint is removed from v0.1 (note 2 —
  Vladimir eyeballs example names at review time); ALL lint and CI are deferred
  (note 5, see Deferred) with the written trigger "published beyond private personal
  use" — Vladimir tests everything himself until then. Interim structural guard: the
  commit protocol (Ways of working #6) puts human review in front of every commit.
  This consciously relaxes the post-mortem's "discipline must be structural" lesson
  during private development; it becomes structural at the publication gate. S-5
  build order revised: scaffold + manifests → skills in lifecycle order →
  repo-reader → docs generator + README last.
- D-23 (2026-08-03, resolves OQ-13) Spec review: all "(stated)" mechanics in
  design/spec.md ratified as written, with two changes: (a) the personal-name
  denylist is kept, but as a committed CI grep (see D-12 revision); (b) the
  placeholder vocabulary is two-path — descriptive acme-* names in generic examples
  (the default, conventions-skipped path), plus a themed worked example (acme +
  constellations: orion/lyra/vega/atlas) used only in the naming-conventions docs.
  Both sets allowlisted.

## Principles (all adopted — D-2, D-5)

- P-1 Tracer bullet: v0.1 must run the entire pipeline idea → merged code on a real
  pilot, every stage crude; no stage gets deepened until the whole pipeline has run.
- P-2 State is derived from artifacts, never stored.
- P-3 Structurally honest: lint/CI forbids naming non-existent commands, requires
  next-step footers, and bans pilot/project names in plugin content. (Enforcement
  deferred to publication — D-24; interim guard is the commit protocol.)
- P-4 Nothing enters the plugin that real use has not required.
- P-5 The plugin owns the process model; each workspace owns only its profile and a
  plugin-version pin.
- P-6 Docs are generated from / checked against actual plugin files, so they cannot
  drift.

## Open questions

Queue empty as of S-4.5 (2026-08-03): every remaining item below is parked with a
written trigger that has not fired. Nothing here blocks S-5 — go to the Session plan.

- OQ-1…OQ-6, OQ-8…OQ-10 resolved → D-1…D-11; karpathy guidelines captured in
  design/karpathy-guidelines.md.
- OQ-7 What does "release" mean for the pilot (deploy target, versioning)? Asked at
  dogfood time in the pilot workspace, not here (D-13).
- OQ-11 Superseded by D-13: pilot details are deliberately withheld from this repo;
  Vladimir provides them in-chat when the tracer bullet first runs.
- OQ-12 resolved → D-14.
- OQ-13 resolved → D-23 (spec review, 2026-08-03).
- OQ-14 Release mechanics for v0.1 (deliberately decided at release time — not
  blocking): fresh published repo receiving one clean v0.1 commit (keeps private
  iteration history; airtight against design-zone leakage) vs same-repo orphan
  squash + force-push (one repo, but destroys the iteration history and
  force-pushed-away commits can linger fetchable on GitHub for a while). Trigger:
  tracer bullet complete and release near.

## Session plan

- S-1 (2026-07-30): ground in evidence; settle principles and the four forks above. ✓ done
- S-2 (2026-07-30, same chat session): command set scope, unit mapping, adoptable
  flows from BMAD-METHOD / spec-kit / OpenSpec. ✓ done
- S-3 (2026-07-31…2026-08-01): specify each v0.1 skill, artifact formats, directory
  layout, next-step graph, docs + lint strategy, model table. ✓ done — output is
  design/spec.md; open remainder is the spec review (OQ-13).
- S-4 (2026-08-03): spec review — Vladimir's five notes processed → git started,
  D-12/D-21 revised, D-23, OQ-14 opened, repo-cache deferral recorded. ✓ done
- S-4.5 (2026-08-03): pre-build audit — OQ queue confirmed empty; D-4 install path
  verified against current CC docs; five pre-build notes appended to spec.md
  (unratified). ✓ done
- S-5: build the tracer bullet: plugin scaffold + manifests, seven skills,
  repo-reader, docs generator + README. No lint/CI (D-24). Pilot specifics arrive
  only at dogfood time (D-13). ← next

## Session log

- S-1 2026-07-30: Explored both predecessor repos (summaries above). Read WardX
  conventions.md as a naming-convention example. Wrote this file. Asked OQ-1…OQ-4 as
  structured questions. /karpathy-guidelines skill unavailable in the session.
- S-1 (cont.) 2026-07-30: Two question rounds answered → D-1…D-7 recorded; all six
  principles adopted. S-1 scope complete. Still open before S-3: OQ-11 (pilot name) and
  OQ-6 (karpathy guidelines). Next: S-2, the command set.
- S-2 2026-07-30 (same chat session): Karpathy guidelines received →
  design/karpathy-guidelines.md (OQ-6 resolved). Researched BMAD v6.10 / spec-kit
  v0.15 / OpenSpec v1.7 (summary above); proposed adoption candidates A1–A6 and the
  draft v0.1 command set; asked ratification questions (unit mapping, adoptions,
  command set, conventions). All four ratified → D-8…D-11.
- S-2 (cont.) 2026-07-31: D-11 refined per Vladimir (groups defined first; unreserved
  letters are user-owned). New: R-8 (per-command model recommendation), D-12
  (two-zone repo, design zone never in git — .gitignore created), D-13 (pilot details
  never in this repo). Model mechanics verified against CC docs → D-14 (skills and
  subagents pin via frontmatter; skill pins last one turn; fable valid, CC ≥ 2.1.170;
  no auto-escalation). S-2 fully complete; S-3 unblocked — pilot no longer needed
  before spec work.
- S-2 (cont. 2) 2026-07-31: Three refinements from Vladimir. D-12 refined: gitignore
  alone insufficient → two lint layers (public placeholder-allowlist in CI; private
  personal-name denylist local in the design zone). D-13 refined: allowed abstract
  question categories listed (repo count/kinds, ways of working, MCP integrations) —
  never brief/idea/domain. D-14 revised: model guidance is docs-only recommendation,
  nothing pinned, everything inherits; task-level model recommendation recorded under
  "Deferred, with triggers". S-3 ready to start.
- S-3 2026-08-01 (chat session started 2026-07-31): Workspace artifact model settled
  via four question rounds → D-15 (layout: lifecycle dirs), D-16 (tasks as files),
  D-17 (amend-only change scope), D-18 (two status vocabularies). PRD-vs-epic
  discussed in depth at Vladimir's request (spec vs. delivery batch; three divergence
  cases; plugin-owned mechanical triggers instead of per-project "optional") → D-19
  (spine + triggered epics, machinery deferred). Then D-20 (stub PRDs as the map),
  D-21 (per-repo merge flow, linear history), D-22 (human acceptance flips story done;
  FAIL → gated re-plan; flow designed from Vladimir's multi-repo upload-story
  example). Wrote design/spec.md — full v0.1 spec: seven skills, repo-reader,
  cross-cutting mechanics, lint/docs strategy, placeholder vocabulary, tracer-bullet
  definition of done. New OQ-13: review the "(stated)" mechanics in spec.md before
  building. Next session: S-4.
- S-4 2026-08-03 (spec review): Vladimir's five review notes processed. Git started
  immediately — design zone committed from now on (D-12 revised; the no-leak
  guarantee moved to the release procedure; release mechanics parked as OQ-14 with
  trade-offs recorded there). The resume prompt now names spec.md explicitly (the
  gap behind note 2 — STATE.md referenced it internally but the paste-in prompt
  didn't). Repo-summary suggestion challenged and settled as a deferred
  commit-hash-keyed cache (Deferred section) — mechanical invalidation instead of
  discipline-maintained updates. D-21 amended: always squash, task reference leads
  the mainline commit message. OQ-13 resolved → D-23: all stated mechanics
  ratified; denylist kept as committed CI grep; placeholder vocabulary two-path
  (descriptive default + themed naming-conventions example). design/denylist.txt
  created. Next: S-5, build the tracer bullet.
- S-4.5 2026-08-03 (autonomous session): The resume prompt pointed at Open questions,
  but the queue is empty — OQ-7 (dogfood time) and OQ-14 (release time) are parked
  with unfired triggers and were deliberately NOT re-opened. Ran the pre-build audit
  of spec.md instead. D-4 feasibility verified against current Claude Code docs
  (code.claude.com/docs/en/plugin-marketplaces.md): a private repo doubles as its own
  marketplace via .claude-plugin/marketplace.json; add/install/update commands
  confirmed; private-repo auth rides the user's gh/SSH credentials; one gotcha
  (background auto-update needs a credential helper) goes in the README. Five
  build-level gaps resolved as spec.md "Pre-build notes" — Claude-proposed and
  UNRATIFIED: marketplace manifest added to layout; lint rule 1 scans code
  spans/fences only (rule 5 keeps full-text coverage); D-22 sign-off is a manual
  story-file edit, no new skill; docs generate from name/description/argument-hint
  frontmatter (model: field confirmed to exist and deliberately unused per D-14);
  S-5 build order puts lint + CI before any skill. Resume prompt rewritten to point
  at S-5. Nothing was ratified this session; Vladimir nods through or challenges the
  notes when S-5 starts.
- S-4.5 (cont.) 2026-08-03: Vladimir ratified the five pre-build notes with changes
  → D-24. Notes 1/3/4 approved (note 4 adds: README must reference every docs/
  file); note 2's allowlist lint removed from v0.1; note 5 defers ALL lint + CI,
  trigger: publication beyond private personal use. New Ways of working #6 — the
  commit protocol (no unprompted commits; suggest message → Vladimir reviews →
  commit/push only on explicit ask). D-12 amended (denylist checked manually until
  the trigger), P-3 annotated (enforcement deferred), spec.md updated throughout
  (layout, lint/docs section, acceptance mechanics, ratification record, build
  order). S-5 next: scaffold + manifests → skills → repo-reader → docs + README.
