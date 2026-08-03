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
> working". The v0.2.0 build (S-6 retro round, D-26…D-30) is complete on disk;
> S-6 dogfood is IN PROGRESS in the pilot's directory, not this repo — the
> pilot has run init → PRD map → one developed PRD → one ADR; plan → implement
> → acceptance remain. In this repo the remaining work is processing whatever
> review feedback or pilot retro observations Vladimir brings. Do not re-derive
> settled Decisions and do not re-explore ../speck or ../speculation beyond
> what this file records. Before the session ends, update STATE.md.

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
7. Repo boundary (added 2026-08-03): sessions in this repo never MODIFY
   project/workspace repos — suggestion-only (name the plugin skill to run
   there, or give precise manual steps). Reading them for analysis stays
   allowed. Enforced structurally by the PreToolUse hook in
   .claude/settings.json + .claude/hooks/repo-boundary.py (blocks outside
   Write/Edit/NotebookEdit and mutating Bash referencing outside paths).

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
- Full plugin-evolution loop (R-3) — trigger FIRED 2026-08-03 (first pilot
  observations processed in the S-6 retro round). The loop now runs in its
  manual v0.2 form: retro review mode executed in the plugin repo under the
  commit protocol (D-30c). Dedicated machinery (automated handoff ingestion,
  reload prompting) stays deferred; new trigger: the manual form hurts, or the
  plugin gains a second user.
- GitHub MCP (D-33): no current need — sibling layout reads across repos on
  disk; merge_flow: pr rides the gh CLI. Trigger: first remote-only repo, a
  collaborator without local siblings, or CI-status needs.
- Dedicated design-system repo (D-35, frozen family U): imported design code
  stays workspace-resident reference material. Trigger: it becomes a
  build-time dependency consumed by multiple repos (a real component
  library FE/mobile import at build), or its size/tooling makes the
  workspace unwieldy.
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
- D-25 (2026-08-03) Document standards adopted after the S-5 research round,
  ratified by Vladimir with one amendment. Adopted: MADR 4.0 structure for
  ADRs (our front matter/status vocabulary kept); FR-NNN requirements with
  must/should/could priorities and EARS ACs in PRDs; Connextra goal +
  Given/When/Then AC test scripts in stories (INVEST as plan's check); Moore
  positioning opener in the brief + three SVPG opportunity-assessment
  questions in init's interview; C4-lite overview template. Amendment
  (Vladimir): story AND task acceptance/verification must be repeatable test
  scripts with explicit steps (story ACs = GWT; task Verification =
  preconditions/steps/expected), and DoR/DoD adopted — resolved as UNIFORM
  definitions for both stories and tasks, stated once in the workspace
  CLAUDE.md template and enforced by plan/implement, never duplicated per
  item (per-item variability already lives in ACs/Verification). Kept
  without external standard (none exists / already framework-adopted): task
  format, change proposal (OpenSpec A1), contract.
- D-23 (2026-08-03, resolves OQ-13) Spec review: all "(stated)" mechanics in
  design/spec.md ratified as written, with two changes: (a) the personal-name
  denylist is kept, but as a committed CI grep (see D-12 revision); (b) the
  placeholder vocabulary is two-path — descriptive acme-* names in generic examples
  (the default, conventions-skipped path), plus a themed worked example (acme +
  constellations: orion/lyra/vega/atlas) used only in the naming-conventions docs.
  Both sets allowlisted.
- D-26 (2026-08-03, S-6 retro round) Workspace commit protocol: Ways of working
  #6 extends to every workspace. Skills never commit unprompted; each unit of
  work ends with a proposed commit message, committed only on explicit owner
  approval; the protocol lives in the workspace CLAUDE.md template so ad-hoc
  sessions inherit it. Unit-of-work grain: scaffold · approved brief · PRD-map
  stubs · each developed PRD (plus change proposals it opened) · each ADR with
  its overview update · each plan batch · each retro review's applied fixes.
  Exception: implement's code-repo commit stays mechanical (D-21 — one task =
  one squashed mainline commit IS the unit); its workspace status/Learnings
  edits get a proposed workspace commit at close-out. Root cause fixed: v0.1
  init explicitly instructed two autonomous commits while no other skill
  committed at all — wrong in both directions (dogfood observations 2 and 7).
- D-27 (2026-08-03, amends D-11 and D-23) Frozen naming-family taxonomy: the
  letter→family mapping is plugin-owned and product-independent, shipped as
  templates/naming-families.md — 16 families (A app services · B browser apps ·
  C client apps · D data · E integrations · F foundations · G governance, always
  the workspace repo · H hosting · I identity · J jobs · M machine intelligence
  · O observability · P platform · Q quality · S schemas · T tooling) plus
  reserved K/L/N/R/U/V/W/X/Y/Z, with family decision rules, a not-a-family list,
  and codename rules including a theme-viability check (every activated letter
  needs 5–10 candidates under the theme, or the theme is disqualified).
  Modeled on the enterprise repo-naming convention Vladimir supplied in-chat.
  Products no longer DEFINE groups — they ACTIVATE families and pick a theme;
  D-11's groups-first mechanics are superseded to that extent (optionality,
  theme-from-product-idea, and owner-supplied pools for later activations
  stand). Root cause fixed: greedy per-product letter assignment spent a
  canonical letter on the wrong family on first use (dogfood observation 3).
  D-23's themed vocabulary extends to letter-matched constellation names:
  acme-gemini / andromeda / bootes / cassiopeia / hydra (+ musca / mensa /
  monoceros as M examples), naming-conventions docs only.
- D-28 (2026-08-03) Propose-then-ask interviewing: init's BA interview and the
  clarify passes in prd and decide must frame before asking — a short synthesis
  of what is already known plus a strawman position, then 2–3 questions that
  reference the frame, then (init, per topic) a mini-summary the owner confirms.
  Root cause fixed: the v0.1 interview read as an interrogation — bare
  questions, no context, no suggestions, no summaries (dogfood observation 5).
- D-29 (2026-08-03) decide gains depth: state the decision's reversal cost up
  front and scale the whole treatment by it; bounded clarify pass (≤5 questions
  on what artifacts do not record — unstated preferences, prior experience,
  effort appetite, owned accounts/subscriptions, risk tolerance); an
  investigation step (web research on candidates' current state; repo-reader
  where registered code informs) mandatory for hard-to-reverse decisions;
  per-option failure modes in the trade-off table for hard-to-reverse
  decisions; and a no-smuggling rule — any new external dependency a decision
  introduces is either decided in the ADR or named an explicit follow-up
  decision. Root cause fixed: v0.1 decide ran name → drivers → options → table
  straight from artifacts; its first foundational ADR on the pilot was
  competent but under-investigated, and its consequences slipped an undecided
  vendor dependency into the overview (dogfood observation 6).
- D-30 (2026-08-03) Brief depth ladder, brief-delta discipline, retro UX.
  (a) The brief stays lean, but the template gains a "Product shape
  (capability sketch)" section — 2–4 lines per capability plus its sharpest
  open question — and init's gate presents the depth ladder (brief → PRD map →
  developed PRDs → stories/tasks) so deliberate thinness reads as intentional
  (dogfood observation 1). (b) prd's clarify pass must open a changes/
  proposal in the same session when an answer amends the approved brief —
  clarify answers may not strand brief deltas (two stranded deltas found on
  the pilot); stub PRDs may carry an optional "Notes for development" section
  (legalizing observed useful practice). (c) retro modes are chosen by
  argument CONTENT: one short observation → verbatim append; a multi-item
  argument → itemized dated entries, confirmed, then review offered; a bare
  call with no observations → offer interactive capture instead of a dead end
  (dogfood observation 4). Run inside the plugin repo, review mode IS the
  plugin-evolution loop.
- D-31 (2026-08-03) Retro review challenges, never just accepts: observations
  are symptoms, not verdicts — root-causing may confirm, refine, or overturn
  them; the reviewer asks when an observation underdetermines the fix,
  proposes the better option where one exists, and states explicitly when a
  point stands exactly as written. Prompted by Vladimir's feedback on the
  first evolution-loop run (his points were accepted wholesale, zero
  questions asked). Applies equally to the plugin-repo form of the loop.
- D-32 (2026-08-03) /spectacular:upgrade + shipped upgrade notes: workspaces
  follow plugin version bumps without re-running lifecycle stages. Mechanics:
  compare the profile pin to the installed version → walk docs/upgrades.md
  sections (hand-maintained, one per workspace-affecting release) from pin to
  installed → drift-scan workspace files against current templates → apply
  gated fixes split by ownership (plugin-owned scaffolding edited directly;
  approved truth only via changes/, and only for concrete defects — template
  conformance alone never rewrites approved truth) → bump the pin → one
  proposed commit. Explicitly NOT its job: validating that upgraded skills
  "work" — the next real lifecycle stage does that; re-running completed
  stages is theater, and amend-only (D-17) forbids it anyway. Ratified via
  question round (upgrade skill chosen over next-integration and
  manual-per-retro).
- D-33 (2026-08-03) GitHub MCP deferred with a written trigger (Vladimir
  ratified the deferral): under the sibling layout the workspace and code
  repos already read each other from disk (registry + contract + repo-reader),
  and merge_flow: pr already rides the gh CLI, so a GitHub MCP adds nothing
  today. Trigger: first remote-only repo, a collaborator without local
  siblings, or CI-status needs. Recorded under Deferred. General MCP posture
  (with D-34): the plugin never ships or configures MCP servers; skills use
  connected MCPs opportunistically and degrade gracefully without them.
- D-34 (2026-08-03) Design stage adopted NOW — Vladimir's explicit call over
  Claude's defer-recommendation, consciously relaxing P-1 (a stage added
  before the tracer bullet closes; the counterargument was made and overruled
  by the owner: his UX role and design-driven FE/mobile delivery need design
  as first-class truth). Shape: design specs are truth artifacts at
  product/designs/NNN-<slug>.md (status draft|approved; front matter prd:
  required, sources: design-tool links; reference design-NNN);
  /spectacular:design RECORDS owner-authored UX — flows, screens with states
  and source frames, cross-cutting patterns, requirement mapping only where
  design constrains acceptance — and never generates UX; precondition:
  approved PRD; a design finding contradicting the PRD opens a changes/
  proposal. Consumers: plan reads approved design specs, warns when a
  UI-bearing PRD lacks one (owner may explicitly plan without), stories and
  tasks carry Design references, the A4 check gains a design-coverage clause,
  the story DoR gains the designed-UI clause; implement's capsule pulls
  referenced frames via a connected Figma/design-tool MCP, degrading to
  owner-confirmed links. Lifecycle position: after prd, before decide.
  Command set grows to nine (design, upgrade) — v0.3.0.
- D-35 (2026-08-03) Design-code import is plugin-owned and git-canonical
  (both forks ratified by Vladimir over per-project-ad-hoc,
  dedicated-repo-now, and remote-only): ready design code — a Claude Design
  (claude.ai/design) project, an exported prototype, plain design files —
  is imported INTO the workspace, because the workspace is the hub every
  code repo already reads via its contract (FE, mobile, QA get it for
  free). Placement is two-level: product/designs/system/ for product-wide
  code (visual directions, foundations, component systems, themes) and
  product/designs/NNN-<slug>/ for one spec's screen prototypes. Every
  import directory carries provenance.md (source project id+URL,
  remote→local file map, import date, viewing notes, refresh procedure).
  Import is source-only (no deps, no build outputs). After import, git is
  the canon; the external tool stays the authoring surface; refresh is
  explicit and gated (structural diff → fetch changed only → owner
  approves). Imported code is REFERENCE for look and feel — implement
  translates it to each repo's stack, never pastes it. Mechanics live in
  /spectacular:design step 3 (import/refresh), reading Claude Design
  through Claude Code's built-in design-tool access (verified working:
  read methods need no extra auth on a logged-in session; plan-gated
  writes exist for a future push-back flow). Escalation deferred with a
  trigger: when design code becomes a build-time dependency consumed by
  multiple repos (a real component library), it graduates to a dedicated
  sibling repo under frozen family U. → v0.4.0.
  D-32 amended (2026-08-03, Vladimir-ratified → v0.4.1): equal pin and
  installed version no longer dead-end — upgrade runs the drift scan as a
  verification pass (hand-migrated workspaces can claim the right pin while
  missing pieces); findings follow the normal gated flow, no pin change.
- D-36 (2026-08-03) Distill imported design code; raw code stays. Vladimir
  challenged design-code HTML in the workspace as the consistency
  mechanism; a web-research round (design-token/AI-agent practice)
  confirmed the split: raw imported code is provenance + component-detail
  reference, while AI-generation consistency comes from two small distilled
  artifacts in product/designs/system/ — tokens.json (primitive + SEMANTIC
  tokens; the cross-platform source each repo materializes via a
  theme-bootstrap first task) and design-language.md (one page of rules
  riding in every UI task's capsule). design's import step distills and
  re-distills on refresh, gated; implement's capsule always carries the
  distilled pair for UI tasks and opens raw code only on component demand;
  plan names the tokens source in UI repo contracts and proposes the theme
  bootstrap. Templates shipped: design-tokens.json, design-language.md.
  Both forks Vladimir-ratified (adopt distillation; keep raw code).
  No per-screen wireframes required — screen structure comes from PRD ACs +
  design-spec flows; final screens are Figma artifacts only where the owner
  chooses. → v0.5.0.

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
- S-5 (2026-08-03): build the tracer bullet: plugin scaffold + manifests, seven
  skills, repo-reader, docs generator + README. No lint/CI (D-24). ✓ done —
  built and self-checked; awaiting Vladimir's review + first commit of shipped
  content (commit protocol).
- S-6: dogfood — install the plugin from this repo, run the tracer bullet end to
  end on the pilot (specifics arrive in-chat — D-13; "release" meaning asked
  there — OQ-7). Runs in the pilot's own directories, NOT in this repo; this
  repo only receives retro-driven fixes afterwards. ← IN PROGRESS: the pilot
  ran init → brief approved → PRD map (6 stubs) → one PRD developed and
  approved → one foundational ADR; seven friction observations came back and
  were processed in this repo (retro round, D-26…D-30, v0.2.0). Remaining:
  plan → implement → ≥1 story through acceptance PASS, on the updated plugin.

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
- S-5 2026-08-03 (autonomous session): v0.1 built per spec.md in the D-24 order.
  On disk: .claude-plugin/plugin.json + marketplace.json (v0.1.0); seven skills
  under skills/<name>/SKILL.md; agents/repo-reader.md; scripts/generate-docs.py
  (stdlib, fails loudly on skills↔lifecycle mismatch); docs/commands.md
  (generated); docs/models.md (hand-maintained per D-14); README.md (install/
  update incl. credential-helper gotcha; references both docs files per D-24).
  Self-checked all five deferred lint rules manually: denylist clean; only the
  seven real commands mentioned anywhere; every SKILL.md ends in "## Next step";
  docs regenerate identically; both manifests parse. Build-level choices for
  Vladimir's review (all within ratified spec, none contradicting a D-number):
  (a) Karpathy guidelines ship inside the workspace CLAUDE.md template at
  skills/init/workspace-claude-md.md — init cannot read design/ since it is
  excluded at release; (b) the themed constellation example (D-23) lives in
  init's naming step, v0.1's only naming-conventions doc; (c) marketplace
  owner.name is the impersonal "spectacular maintainers" (D-12a); (d)
  repo-reader is structurally read-only via tools: Read/Glob/Grep; (e) change
  references follow per-type numbering: change-NNN → changes/NNN-<slug>/
  proposal.md. Nothing committed — commit message suggested in-chat per the
  commit protocol. Next: Vladimir reviews the diff and commits; then S-6
  dogfood on the pilot.
- S-5 (cont.) 2026-08-03: Vladimir's build review, five points. (1) No
  repo-creation command — confirmed intentional: plan creates code repos in its
  breakdown (D-10/R-6; repos exist only because a task needs a home). (2+4)
  templates/ dir added to shipped layout (spec.md layout updated): brief, prd,
  adr, story, task, change-proposal, contract + workspace-claude.md (moved from
  skills/init/, renamed per feedback). Artifact shapes now live ONLY in
  templates/ — skills reference ${CLAUDE_PLUGIN_ROOT}/templates/*, no inline
  format blocks left to drift. No epic template (D-19 machinery deferred).
  (3) marketplace.json owner.name → "oswalth" (Vladimir's explicit ask;
  narrows D-12a impersonality for this one functional field). (5) Temporary
  README section on local-checkout usage, verified against current CC docs:
  --plugin-dir + /reload-plugins recommended; local marketplace add needs ./
  prefix; installed copies live in ~/.claude/plugins/cache so local edits need
  marketplace update or reinstall; claude plugin validate. Marked for removal
  at publication. Still nothing committed.
- S-5 (cont. 2) 2026-08-03: Vladimir asked where the templates came from —
  answer: distilled from spec.md (D-15…D-22), not from any proven external
  standard — and requested research into industry-proven formats. Two research
  passes (product docs; engineering docs) against primary sources. Findings:
  MADR 4.0 (2024) is the living markdown-ADR standard and maps 1:1 to decide's
  flow; EARS ("WHEN … THE SYSTEM SHALL …", Rolls-Royce 2009) is the emerging
  cross-tool AC syntax for AI-consumed specs (AWS Kiro et al.); spec-kit's
  FR-NNN numbered requirements + measurable SC pattern is the AI-era PRD
  consensus; Connextra story line + INVEST are near-universal; Moore's
  positioning statement and SVPG's opportunity-assessment questions fit the
  brief/interview; task formats are genuinely non-standardized (ours already
  matches Wake's SMART guidance); arc42 is ceremony for this scale, C4
  levels 1–2 fit a minimal overview. Proposals P1–P6 presented in-chat
  (MADR-align ADR; EARS ACs; FR-NNN+MoSCoW in PRDs; Moore line + SVPG
  questions in brief/init; Connextra story goal; new templates/overview.md).
  UNRATIFIED — awaiting Vladimir's approve/challenge; nothing applied,
  nothing committed.
- S-5 (cont. 3) 2026-08-03: Vladimir ratified P1–P6 with one amendment
  (structured, step-by-step testable ACs for stories AND tasks; DoR/DoD) →
  D-25 recorded and applied. Templates rewritten (adr → MADR 4.0; prd →
  FR-NNN + EARS; story → Connextra + GWT scripts; task → structured
  Verification; brief + Positioning; overview.md new); workspace-claude.md
  gains the uniform DoR/DoD section; skills updated (init interview + brief
  positioning; prd FR/EARS rules; plan Connextra/GWT/INVEST + DoR framing;
  implement DoR check + DoD walk; decide MADR + overview template). spec.md
  synced (layout comment; "Adopted document standards" paragraph). Full
  verification sweep re-run. Awaiting Vladimir's commit.
- S-6 2026-08-03 (retro round, this repo): first half of dogfood ran in the
  pilot workspace (init → brief approved → PRD map → one PRD approved → one
  ADR — per D-13 no specifics recorded here). Vladimir brought seven friction
  observations in-chat via /spectacular:retro; each was root-caused against
  the pilot artifacts and the v0.1 skill texts, plus two findings of Claude's
  own (clarify answers stranding approved-brief deltas; an ADR consequence
  smuggling an undecided vendor dependency into the overview). R-3's
  evolution-loop trigger thereby fired; the loop ran in its manual form under
  the commit protocol. Fixes recorded as D-26…D-30 and applied: workspace
  commit protocol everywhere (skills init/prd/decide/plan/implement/retro +
  workspace-claude.md template); frozen naming-family taxonomy shipped as
  templates/naming-families.md with init's naming step rewritten to
  activate-families-then-theme; propose-then-ask interviewing in init/prd/
  decide; decide deepened (reversal cost, clarify, investigate, failure
  modes, no-smuggling); brief template + init gate carry the capability
  sketch and depth ladder; prd opens change proposals for brief deltas and
  legalizes stub Notes; retro modes made content-aware with interactive
  capture and the plugin-repo case documented. plugin.json → 0.2.0; docs
  regenerated; pilot names added to design/denylist.txt (design zone only);
  manual denylist grep over shipped files clean. Matching workspace-side
  fixes applied directly in the pilot (conventions rewritten to the frozen
  taxonomy, profile pin bumped, CLAUDE.md gains the commit protocol, two
  change proposals opened for the stranded brief deltas, observations marked
  addressed). Nothing committed in either repo — commit messages suggested
  in-chat per the protocol. Remaining S-6: plan → implement → acceptance on
  the pilot with v0.2.0.
- S-6 (cont.) 2026-08-03: Vladimir's feedback on the retro round, three
  points. (1) The evolution loop accepted his observations wholesale, zero
  questions — must clarify/challenge/confirm explicitly → D-31; retro
  SKILL.md amended, spec.md synced. (2) Open discussion: how a live workspace
  follows plugin upgrades without re-init — proposed /spectacular:upgrade
  (per-version upgrade notes + mechanical drift scan; plugin-owned
  scaffolding edited directly under gate, approved truth only ever amended
  via changes/; the pin in profile.md is the version anchor), with the
  counterpoint that upgraded skills are validated by the NEXT lifecycle
  stage, not by re-running completed ones. (3) Open discussion: MCP posture —
  GitHub MCP challenged as no-current-need (sibling layout reads across
  repos on disk; merge_flow: pr already rides the gh CLI; trigger would be a
  remote-only repo or a second collaborator), Figma MCP acknowledged as a
  real upcoming need for design-driven FE/mobile tasks; minimal shape
  proposed (design references in story/task + capsule fetch when connected,
  plugin never ships MCP config). Decisions pending Vladimir's answers.
- S-6 (cont. 2) 2026-08-03: Vladimir answered the three forks → D-32 (the
  /spectacular:upgrade skill, over next-integration and manual-per-retro),
  D-33 (GitHub MCP deferred with trigger, as recommended), D-34 (FULL design
  stage now — overruling the defer-recommendation; P-1 consciously relaxed).
  Built and applied: skills/design + templates/design.md; skills/upgrade +
  docs/upgrades.md (hand-maintained per-version migration notes, 0.1.0→0.3.0
  covered); plan (design context, Design references on stories/tasks, A4
  design-coverage clause), implement (capsule pulls design slices, fetches
  frames via connected design-tool MCP, degrades to links), next (designs in
  reads/vocab/drafts; nine-command list), story/task templates (optional
  Design references), workspace-claude.md (designs layout row, design-NNN
  reference example, designed-UI DoR clause); generator lifecycle → nine
  skills, docs regenerated; models.md + design (opus) and upgrade (sonnet)
  rows; README updated (nine commands, upgrade flow + upgrades.md reference,
  MCP posture note); plugin.json → 0.3.0; denylist grep clean. Pilot
  workspace upgraded to the 0.3.0 notes (pin, CLAUDE.md layout/reference/DoR
  deltas) — the first manual execution of exactly what /spectacular:upgrade
  automates. Nothing committed — messages suggested per the protocol.
  Remaining S-6 unchanged: design (optional for prd-001) → plan → implement
  → acceptance on the pilot.
- S-6 (cont. 3) 2026-08-03: Vladimir raised design-code import (he had
  created a design-code visual direction in Claude Design for the pilot).
  Grounded the discussion in the actual tooling first: Claude Code's design
  access verified live — writable design-system projects listed, the
  pilot's design project read (a regular PROJECT type; reads work through
  the logged-in session, no extra auth; per-file fetch capped at 256 KiB;
  writes are plan-gated and incremental). Question round → D-35 (plugin
  convention + skill support over per-project ad-hoc; workspace-resident
  git-canonical over dedicated-repo-now and remote-only, both
  recommendations accepted; source identified via pasted project URL).
  Applied: design SKILL.md gains the design-code convention section and an
  import/refresh step 3; design template sources widened + cross-cutting
  pointer to system/; implement capsule reads imported code from the
  workspace and translates, never pastes; workspace-claude.md designs row
  reworded; docs/upgrades.md 0.4.0 section; README (design row + import
  posture paragraph); plugin.json → 0.4.0; docs regenerated. Pilot-side:
  the design project's two files imported to product/designs/system/
  (direction-01.dc.html + support.js, relative link preserved) with
  provenance.md; pin → 0.4.0; CLAUDE.md row reworded. New Deferred entry:
  dedicated design-system repo (family U) with a build-time-dependency
  trigger. Nothing committed — messages suggested per the protocol.
- S-6 (cont. 4) 2026-08-03: v0.4.0 committed on Vladimir's explicit ask
  (plugin: one commit; pilot: four logical units drawing the missing git
  lines). Plan review — Vladimir challenged the next-steps plan; outcomes:
  bare change-NNN references must be spelled out (they are the two brief
  amendment proposals in the pilot's changes/); NEW BOUNDARY — sessions in
  this repo never modify project repos again, suggestions only (skills
  first, precise manual steps as fallback); his "design already produced
  decision 001" clarified via question round → he meant adr-001 from
  decide, so the two plan-blocking ADRs (mobile framework, backend stack)
  stand; upgrade's equal-version dead-end fixed as verification mode (D-32
  amended → v0.4.1). Design-truth workflow stated by Vladimir: Claude
  Design code = exploratory reference for component look; FINAL screen
  designs will be created as artifacts in Figma (the design-spec sources) —
  matches D-35's reference-not-truth stance; workspace-side wording tweak
  suggested to him, not applied (boundary). v0.4.1 uncommitted — message
  suggested per protocol.
- S-6 (cont. 5) 2026-08-03: Two Vladimir points. (1) The repo boundary made
  STRUCTURAL — Ways of working #7 recorded; PreToolUse hook added
  (.claude/settings.json + .claude/hooks/repo-boundary.py) blocking
  Write/Edit/NotebookEdit outside this repo and mutating Bash referencing
  outside paths (reads stay allowed); pipe-tested 9/9 scenarios; arms after
  /hooks or a session restart (settings file created mid-session). (2) He
  challenged workspace-stored design-code HTML as the consistency
  mechanism; web research → D-36 distillation convention applied
  (design/implement/plan skills, two new templates, upgrades.md 0.5.0
  section, workspace-claude designs row) → v0.5.0. Pilot-side to run by
  Vladimir there: distill direction-01 via /spectacular:design prd-001 (or
  a direct distill ask), per upgrades.md 0.5.0. Uncommitted (v0.4.1 +
  v0.5.0 + hook) — message suggested per protocol.
