# Spectacular — design state

Single source of truth for the design phase of **spectacular**, the third attempt at a
Claude Code plugin for AI-assisted SDLC (idea → brief → PRDs → architecture → breakdown →
implementation → release), after two failed attempts: `../speculation` (v0.3.0) and
`../speck` (v0.2.1). The original brief (`tmp.md`, deleted at publication — D-48; in git
history before v0.11.1) is condensed here.

This file plus design/spec.md (S-3 build spec) and design/karpathy-guidelines.md are the
complete design context; the repo's CLAUDE.md (auto-loaded) carries the ways of working
and the retro loop. Update this file at the end of every design session: move settled
items into Decisions, refresh Open questions, append to the Session log. It must never
contradict what was agreed in conversation.

## How to resume in a fresh session

CLAUDE.md loads automatically. Read Decisions, Deferred and Open questions here, then
design/spec.md for the parts you touch; the Session log is evidence, read on demand.
Status: the plugin is published to the team (D-48) and at 0.12.0 (D-49: code-repo
CLAUDE.md + README shape, onboard, scoped next, read-fresh, language); S-6 dogfood
continues in the pilot's directories, not here — remaining: ≥1 story through
acceptance PASS on the current plugin, and the first real teammate onboarding
(D-49's onboard has not run for real yet). Work here is processing review feedback
and retro briefs. Do not re-derive settled Decisions and do not re-explore ../speck
or ../speculation beyond what this file records.

## Ways of working

Moved verbatim (impersonal wording) to the repo's CLAUDE.md on 2026-08-19 (D-48), so
they load in every session on any machine. Numbering #1–#9 is unchanged and is what
docs/release.md and the repo-boundary hook cite. Origin, for the record: #1–#5 from the
original brief; #6 commit protocol and #7 repo boundary added 2026-08-03; #8 change
strategy D-37; #9 gate protocol + self-sufficiency D-41.

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
  reload prompting) stays deferred; trigger refined 2026-08-19 (D-48g): the
  manual form hurts, or a second person gains write access to the plugin
  repo — read-only teammates hand briefs over as GitHub issues.
- GitHub MCP (D-33): no current need — sibling layout reads across repos on
  disk; merge_flow: pr rides the gh CLI. The "collaborator without local
  siblings" trigger fired 2026-08-19 (team onboarding) and is met without an
  MCP: registry `remote` + git fetch/clone (D-49 read-fresh, onboard).
  Remaining triggers: first remote-only repo, or CI-status needs.
- People model for bugs and tasks (D-46): no `assignee:`/`severity:` fields;
  routing unit is the repo, severity is a triage judgment recorded in the
  Triage notes. Held again 2026-08-19 (D-49): onboarding derives access from
  GitHub and scoped next uses the registry `role` — nothing about people is
  stored. Trigger: a real team needs per-person routing or a
  severity-driven ranking that the owner cannot make by reading next.
- Dedicated design-system repo (D-35, frozen family U): imported design code
  stays workspace-resident reference material. Trigger: it becomes a
  build-time dependency consumed by multiple repos (a real component
  library FE/mobile import at build), or its size/tooling makes the
  workspace unwieldy.
- Lint + CI (all five designed rules kept in spec.md "Lint and docs": placeholder
  allowlist, no-vapor, footer, docs-sync, denylist grep). Deferred by D-24 —
  the commit protocol (Ways of working #6) is the interim guard; the manual
  checklist lives in CLAUDE.md and docs/release.md step 5. The original trigger
  (team share) fired 2026-08-19 and the owner deferred again (D-48f): the owner
  is the only writer and reviews every diff. New trigger: a second person with
  write access, or a public release.

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
  Fulfilled 2026-08-19 (D-48): oswalth/spectacular, private, team read access.
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
  Revised 2026-08-19 (D-48): the design zone IS shared with the team — it is the
  plugin's decision log and what the retro loop root-causes against; "never a byte"
  now applies to a public release only (fresh repo, one clean commit, if that day
  comes). Shipped content stays impersonal and denylist-clean regardless.
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
  Amended 2026-08-18 (D-45): the spine is mandatory for *capability delivery*;
  maintenance work with no story is a standalone task (no `story:`).
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
  Amended 2026-08-18 (D-46): a defect found after acceptance is a *late FAIL* of
  the same loop — the story returns to `in-progress` and is re-tested to a fresh
  PASS; re-plan mode is renamed fix mode and also entered from a bug report.
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
- D-37 (2026-08-03) Unified change strategy across plugin, workspaces, and
  code repos (retro-driven). Conventional Commits was Vladimir's call over
  Claude's formalize-existing-grammar recommendation; the four resolution
  forks below were Claude-recommended and Vladimir-ratified.
  (a) Commit messages follow Conventional Commits 1.0.0 in every repo kind;
  artifact provenance rides git-trailer footers (`Task: task-NNN`,
  `Refs: prd-004`), never the subject — a bare `task-123` body line is not a
  valid CC footer and is invisible to tooling. Mapping: workspaces are mostly
  `docs`/`chore` with the artifact id as scope (`docs(prd-004): approve`);
  code repos use the type matching the change with a mandatory `Task:` footer;
  plugin scopes = skill/template/doc area, releases = `chore(release): X.Y.Z`.
  (b) Tags mark releases, never commits — "tag every commit with the latest
  version" is mechanically impossible (tag names are unique refs); any
  commit's version is derived (`git describe --tags`). Workspaces get NO
  versions and NO tags (state = artifact statuses + plugin pin; resolves the
  contradiction with the workspace-versioning idea). Historical plugin
  versions retro-tagged where a commit is reconstructable: v0.1.0 → ed4bce7,
  v0.4.0 → 6990da2, v0.5.0 → c117233 (post-rewrite SHAs, see amendment (f));
  0.2.0/0.3.0/0.4.1 shipped inside session commits — CHANGELOG entries only,
  no tags.
  (c) Versioning stays semver; the bump is DERIVED from CC types since the
  last tag (feat → minor, fix → patch, BREAKING CHANGE/`!` → major;
  workspace-facing release ⇒ ≥ minor). Code repos record
  `versioning`/`release_flow` in the contract; the release act (when to ship)
  stays with the release manager — manual now, automatable when CI arrives
  (D-24 trigger).
  (d) CHANGELOG.md added at the plugin root (Keep-a-Changelog-lite, backfilled
  from commit subjects); docs/upgrades.md stays the machine-consumed
  migration subset. Invariant: upgrades ⊆ changelog, held structurally by the
  atomic release commit checklist in docs/release.md (version bump +
  changelog + upgrades-if-workspace-facing + tag in one commit; denylist
  check per OQ-14 folded in). → v0.6.0.
  D-37 amended (2026-08-03, same session, Vladimir-directed): (e) commit
  messages never carry AI-attribution trailers (`Co-Authored-By: Claude …`,
  `Generated with …`) — banned across plugin, workspaces, and code repos;
  (f) the plugin's pre-release history was rewritten once to the CC grammar
  (local-only repo, no remote, no consumers — a never-again event once
  published); the retro-tag SHAs in (b) are post-rewrite values;
  (g) docs/release.md is referenced from shipped surfaces (implement step 6,
  retro's plugin-repo section, upgrades.md header, contract template
  comments), not only the design zone, so the procedure survives release —
  design/ is excluded from released history (D-12).
  D-37 amended (2026-08-19, D-49): (h) the `Task:` footer is mandatory for
  a code-repo commit that realizes a task; housekeeping commits (docs,
  comments, formatting, README, CLAUDE.md, contract, Toolchain notes) carry
  none — the rule had already been relaxed in practice by D-38d and D-40's
  `chore(contract)` commits; now it is stated.
- D-38 (2026-08-04) Repo-internal engineering conventions are elicited at
  repo birth and carried by the contract (retro round 2, pilot; in-chat
  observation, Vladimir-ratified with refinements). The gap: stack ADRs
  decide language/framework, but nothing elicited repo-internal principles
  (architecture style, testing philosophy, tooling, packaging) — the pilot's
  foundational stack ADR itself listed "conventions the owner must set and
  keep consistent alone" as an accepted risk with no place to set them; the
  contract template's Conventions section was an empty heading filled "as
  the owner intends", in passing. Root-cause verdicts: decide stays scoped
  to ONE forced decision (a convention batch is not one; cramming it into
  the stack ADR bloats it); repo creation stays with plan (moving it to
  decide would fork the contract/registry machinery); the missing piece is
  elicitation only — implement's capsule already carries the contract, so
  the contract IS the enforcement vehicle. Resolution:
  (a) templates/contract.md Conventions becomes a structured dimension
  list — common core (architecture style, testing, tooling, build &
  packaging, quality gates) as template prompts; the list is explicitly
  OPEN: stack-specific dimensions (sync/async posture, state management,
  dataset versioning, …) are derived per repo from its decided
  architecture, never limited to the template (Vladimir's refinement).
  (b) plan step 5 grows a repo-bootstrap interview (D-28 style): frame from
  the forcing ADRs + defaults from already-registered repos' contracts
  (cross-repo repeatability without a new workspace artifact); per open
  dimension, options with one recommended + justification, owner picks;
  answers land in the contract before the initial commit. A contested,
  hard-to-reverse dimension routes to decide instead.
  (c) The new repo's first task is a scaffold task materializing the
  contract, Verification checking each convention — generalizes the D-36
  theme-bootstrap pattern, which folds into it for UI repos.
  (d) Amendment path (Vladimir's refinement — "we missed the testing
  framework" case): the contract is code-repo-local, NOT workspace truth —
  implement amends it directly under a gate (rides the task branch, or its
  own chore(contract) commit); an amendment contradicting an approved ADR
  is workspace truth — superseding ADR via decide, then re-plan.
  (e) decide step 1 states the boundary explicitly. → v0.7.0.
- D-39 (2026-08-04, retro round 3, pilot) The D-26 exception is dead:
  implement never commits or pushes without an explicit greenlight. The
  pilot's first code-repo implement run auto-landed the squashed commit
  exactly as designed — and the owner experienced it as the plugin committing
  without permission, while the gated workspace close-out sat uncommitted
  next to it (reported as an inconsistency; it was the designed asymmetry).
  Verdict: the gate that starts a task does not substitute for reviewing the
  verified result; approval belongs between verification passing and anything
  landing. Resolution: implement step 6 becomes a landing gate — diff
  summary + verification evidence + both proposed commits (code repo,
  workspace close-out); one greenlight lands both, and it never carries
  across tasks or sessions. `pr` flow pushes only inside the approved
  landing; `local-rebase` pushes nothing (mainline push stays on explicit
  ask). D-21's grain is untouched: one task = exactly one squashed mainline
  commit. The commit protocol now has no exceptions.
- D-40 (2026-08-04, retro round 3, pilot) Code repos carry no plugin version
  pin; upgrade's drift scan covers their contracts instead. Observation:
  "code repos don't have the current plugin version set — I guess they
  should." Confirmed as a real coverage gap with a different fix: the pin's
  only consumer would be upgrade, which refused to look at code repos at
  all — so contract migrations kept shipping as "fix by hand" notes (0.6.0,
  0.7.0 upgrade notes). A per-repo pin is N more places to bump that go
  stale silently, and a code repo is never operated without its workspace
  (implement refuses without the back-pointer). Resolution: the drift scan
  walks `.spectacular/registry.md` and checks each repo's contract.md
  against the current template; fixes are gated per repo as their own
  `chore(contract): …` commits, structure only — undecided Conventions are
  findings, never auto-filled. The workspace pin stays the single version
  authority (P-5 holds). Reaffirmed 2026-08-19 (D-49) on the owner's own
  reasoning; the scan now also covers the code-repo CLAUDE.md and README,
  and lands per `merge_flow`.
- D-41 (2026-08-11, retro round 4, second workspace) Gate protocol,
  discussion-first, uniform challenge. Observation (Vladimir, interrupting a
  retro review that applied three proposed fixes after his reply "keep on
  working"): when intent is unclear, discuss first; even clear intent gets
  challenged when that genuinely helps; and he had sent the vague go-ahead
  only because the session looked stuck — only explicit approve-like
  messages approve. Root cause: no skill defined what counts as approval at
  a gate, and the existing machinery (D-28 propose-then-ask, D-31
  challenge) covered the authoring skills unevenly — plan's breakdown had
  no clarify pass at all. His "make it explicit in all skills" was
  challenged and refined: the rule binds at decision points (interviews,
  authoring, gates), not mechanical derivation/execution — next and upgrade
  need no discussion phase (Vladimir confirmed "next does not need this").
  Resolution, three parts: (1) gate protocol, defined once in the workspace
  CLAUDE.md template and referenced one-line by every gated skill: a gate
  ends with an explicit question naming the decision; only an explicit
  approve-like answer approves; vague go-aheads re-ask; silence never
  consents; approvals name their scope, partial approval normal. Ways of
  working #9 applies the same rule to this repo's sessions. (2) plan's
  breakdown gains a bounded clarify pass (the one authoring skill without
  one); implement stops and asks when the capsule genuinely underdetermines
  the task. (3) one challenge line at every authoring decision point (init
  generalized, prd, design, plan): justification plus proposed alternative,
  stated explicitly when the owner's point stands, never ritual; decide and
  retro already complied (D-29/D-31). Also ratified: repo
  self-sufficiency — process rules live in repo artifacts, never one
  person's session memory or machine-local config; any teammate on any
  machine gets identical behavior (extends P-2/A6/P-5; encoded in the
  workspace template and WoW #9).
- D-42 (2026-08-12, retro round 4, second workspace) next derives the whole
  action ladder. Observation: in a PRD-phase workspace (4 approved PRDs, 13
  stubs, no delivery/, empty registry) /next recommended developing the
  next stub and never surfaced decide or plan for the approved PRDs.
  Confirmed structural: step 4 derived only four candidate classes (drafts,
  ready/blocked, awaiting acceptance, open changes) — all empty in that
  state — so the recommendation could only collapse to stub development;
  the ranking rule (reversal cost) never saw decision candidates because
  nothing derived them. Resolution: step 4 additionally derives
  **plannable** (PRD approved, zero stories via `prd:` links) and **pending
  decisions** (ADR stubs — D-44); ready-next lists every available action
  type while the recommendation stays single; candidates come from every
  derived class, and a decision gating planning (empty registry) outranks
  developing another stub. Front-matter-only derivation preserved.
- D-43 (2026-08-12, retro round 4, second workspace) plan reads sibling
  truth and takes tightly-coupled PRD sets. Observation: owner unsure
  prd-N is fully implementable before prd-N+1; wanted interleaved story
  order across PRDs. Challenged and split: a stored global schedule is
  refused (D-18 — order is derived, would rot); interleaving falls out of
  cross-PRD `depends_on` + next's ready derivation. Confirmed gap: plan's
  context read only the target PRD + designs/overview/ADRs/registry —
  never sibling PRDs or existing stories, so cross-PRD links happened only
  if the model volunteered, and forward coupling surfaced late.
  Resolution: context includes every other approved PRD's front
  matter/scope and all existing stories/tasks; cross-PRD depends_on
  expected (same-run links too); breakdown accepts 2–3 tightly-coupled
  PRDs with a combined acyclicity check (proposed + on-disk) and a gate
  grouped per PRD showing ready-vs-blocked; explicitly not epic trigger 2
  (one goal spanning PRDs ≠ N goals planned together). Bare plan suggests
  a target (or coupled set) and never plans all plannable PRDs in one run —
  JIT batches keep gates reviewable and let later PRDs profit from
  implemented learnings; plan-all was Vladimir's floated idea, analyzed
  and recommended against (context exhaustion, rubber-stamp gates,
  staleness); he confirmed suggest-only on 2026-08-12.
- D-44 (2026-08-12, retro round 4, second workspace) The decision map is
  persisted as ADR stubs — decide gains map mode. Observation: a free-form
  /next answer produced a good decision inventory (waves, ordering) that
  then evaporated in chat; owner wants to review/refactor/order decisions
  as an artifact ("same stuff like we have with bare /prd"). Tension with
  "architecture is not a phase" resolved: every stub names its forcing
  artifact (Forced by note; empty registry with approved PRDs counts and
  heads the map); nothing speculative; re-scans append, never rewrite.
  Mirrors D-20 exactly: map approval writes stub files; the backlog has
  one source — ADR front matter. ADR vocabulary becomes stub → draft →
  approved (extends D-18); working `adr-NNN` fills the stub in place,
  keeping number and file. next derives pending decisions from the stubs
  (D-42); the two compose with D-43 into decide → plan → implement
  visibility at every /next run.
- D-45 (2026-08-18, retro round 5, in-chat question) Standalone tasks.
  Observation: "how do I create singular tasks?" — a DevOps engineer adding a
  team member through IaC has no story to hang a task on. Root cause: D-19
  made the spine mandatory for every task and plan wrote tasks only from a
  PRD breakdown or a FAIL, so maintenance/operations work was structurally
  impossible to record — worse than ceremony, since work then happens that no
  artifact reflects (contra P-2). Resolution: a task without `story:` is a
  **standalone task** — `repo:` + Verification make it ready; written only by
  plan's new standalone mode (free-text argument, chosen by content like
  retro's modes) behind one challenge (new/changed user-visible behavior
  belongs to a PRD → story) and ≤3 clarify questions; implement/next/DoR gain
  "(if any)" clauses; no acceptance step. The standing-"ops PRD/story"
  alternative was rejected (a never-accepted story contradicts D-19/D-22).
  D-19 amended accordingly. Need was hypothetical at decision time — P-4
  consciously overridden on Vladimir's explicit call: "not possible at all"
  is a wall for any real team.
- D-46 (2026-08-18, retro round 5, in-chat question) Bug flow — report →
  triage → fix. Observation: "how do I create a bug task for a story that is
  already done?" Vladimir's framing "bug task" was challenged: a defect in an
  accepted story is a **late acceptance FAIL** — the D-22 loop already covers
  it (`plan story-NNN "<defect>"` writes the FAIL entry, returns the story to
  in-progress, adds fix tasks; re-tested to a fresh PASS), and a standalone
  bug task would lose the AC link and skip re-acceptance. His counter-gap
  stood: the reporter usually does not know the story and must not have to
  investigate first. Resolution, three parts. (1) Bug reports are artifacts —
  `delivery/bugs/NNN-<slug>.md`, `bug-NNN`, `status: open | closed`,
  `routed_to: []` — because report and triage are different acts by
  different people in different sessions (A6, D-16 rationale). (2) A tenth
  skill, `bug`: cheap intake, zero investigation, but NOT zero questions —
  Vladimir overturned that proposal (the reporter's context is richest at
  report time; retro's one-sentence rule does not transfer): it maps the
  argument onto a **bug DoR** (workspace CLAUDE.md: summary, where, steps,
  actual/expected, environment, reproducibility, evidence, regression,
  related), elicits gaps in ≤2 propose-then-ask rounds, files even with
  gaps. (3) Triage lives in **plan** (fix mode, `bug-NNN`) — plan stays the
  single writer of tasks and its FAIL diagnosis is the engine; triage adds
  "find the story first" behind a **narrowing funnel** on Vladimir's ask
  (front matter + slugs → capped candidate story bodies → repo-reader on
  candidate repos only → overview + touching ADRs; widen only on ask; state
  what was not examined), ≤5 rounds, converge or offer 2–3 candidates, then
  route under one gate: violated AC → late-FAIL loop; real work without an
  AC → standalone task(s); not a defect → closed at triage with a Resolution
  (spec gap opens a changes/ proposal). One link direction (bug.routed_to →
  fixing work); a routed bug stays open until fixed — implement closes it
  when the last routed task lands, the re-acceptance PASS closes a
  story-routed one, next nudges fixed-but-open and ranks untriaged bugs
  with lingering drafts. Bugs are never implemented directly. Investigation
  precedes routing (repo-reader makes that cheap), routing unit is the repo
  — no people model; assignee/severity fields deferred (see Deferred).
  Untriaged bugs outrank new work in next. D-22 amended accordingly.
- D-47 (2026-08-18, retro round 6, pilot implement runs) Plan-first,
  section-scoped capsule, just-in-time reconnaissance, a home for
  repo-level Learnings. Observation (Vladimir, in-chat, plus briefs P1–P3
  from the pilot workspace's own retro): implement "does a lot of stuff for
  5–10 minutes without writing a single line of code", ~150k tokens, in
  both the api and the web repo — reading pyproject/CI/Dockerfiles,
  checking docker, running existing tests, inspecting packages. Evidence
  taken from the three implement transcripts (tool-call timelines, context
  size at first write, thinking-block sizes), not memory: two scaffold
  tasks and one feature task, all on a frontier model at very high effort,
  spent 10–20 minutes and 126–172k context before the first in-repo write.
  Root causes: (1) step 3 mandated whole-document reads — MADR ADRs (30–50
  KB per session) and a whole PRD were a third of the pre-code context in
  every run; (2) the skill said nothing about reading the code repo, so
  one run cat'ed the entire tree (41k, the largest agent-chosen cost);
  (3) no plan placement — Karpathy #4 sat in the capsule and still all
  three planned inside 24–32k-token thinking blocks (5–7 minutes each,
  invisible to the owner); the web run rehearsed an interactive CLI in a
  scratch directory and hung 5 minutes on its prompt; (4) repo-level facts
  (version pins, CLI traps, lint quirks) had no home but story-scoped task
  Learnings, so the api repo pushed them into its contract by hand as a
  separate commit and the web workspace invented a local "Toolchain
  notes" section. Challenged (D-31): "tasks were not too hard" — scaffold
  tasks materialize a whole contract by construction (D-38c), so the
  existence of toolchain reconnaissance was proportionate and only its
  manner was wasteful; the baseline test run and docker check cost 4 s and
  stay; package-internals research was legitimate work the previous
  task's Learnings had deferred there — mis-ordered, not wrong; P1's
  overview scoping refused (short by design, ~4k tokens); P2's "plan
  before the first read" inverted to capsule first, then plan; the
  invisible deliberation is the owner's model/effort lever, not the
  skill's. Resolution: (a) implement step 3 reads by section — workspace
  CLAUDE.md added to the capsule, PRD → only the story's mapped ACs and
  cited FRs, ADRs → Decision Outcome/Consequences/Confirmation only
  (options analysis never), DoR from front matter; (b) workspace CLAUDE.md
  template gains Ways of working §5 "Just-in-time reconnaissance" (plan
  after the capsule and before any further read, code read at the step
  that touches it — never the whole tree, one batched lookup per question,
  a failing gate is the discovery mechanism, rehearse outside the repo
  only when in-repo failure is expensive to undo, CLIs non-interactive
  under a timeout, knowledge bought → contract); implement step 5 places
  the printed plan and references §5 (D-41 define-once pattern);
  (c) contract template gains `## Toolchain notes`; the landing gate
  presents Learnings triaged — repo-level as a contract diff on the task
  branch, story-level for the task file — so one greenlight covers both;
  task template Learnings comment; upgrade's drift scan reports a
  contract missing the section (empty heading fine); (d) models.md gains
  a Retro evidence
  section recording the deliberation cost — the sonnet recommendation for
  implement stands. Not done: splitting scaffold tasks (manner, not size,
  was the defect) and any numeric time-box (the plan is the time-box).
  → v0.11.0.
- D-48 (2026-08-19, retro round 7, publication) The plugin is published
  to a private GitHub repo (oswalth/spectacular) shared read-only with
  the owner's team — D-4 fulfilled. Root cause of the readiness gaps:
  D-12 (design zone never ships, reasoned as "personal by nature") and
  D-24 (lint/CI deferred until team share) were decided for a single-user
  repo, while D-41 requires the plugin repo to be self-sufficient for a
  team — and a team that extends the plugin via retro needs the decision
  log that D-12 excluded. Resolutions: (a) OQ-14 resolved for the team
  share — same repo, history intact, pushed as is; D-12 revised: the
  design zone is shared with the team as the plugin's decision log; the
  "never a byte" guarantee narrows to a public release, for which the
  fresh-repo-with-one-clean-commit option stays on record. (b) tmp.md
  deleted — condensed in STATE.md since S-1, unreferenced otherwise, and
  the only absolute client-machine path in the repo. (c) The plugin repo
  gains a CLAUDE.md (auto-loaded, impersonal): two-zone rule, Ways of
  working #1–#9 moved there verbatim (numbering kept), how a retro round
  runs here, checklists for adding a skill / agent / template, the manual
  checks. STATE.md keeps a pointer. (d) README: local-checkout section
  removed as marked, owner filled in, "Evolving the plugin" section
  (briefs reach the repo in-chat or as GitHub issues — read-only teammates
  cannot push), docs/release.md now referenced (D-24 note 4 had been
  violated since 0.6.0), squash wording aligned to the CC grammar.
  retro SKILL.md names issues as a brief carrier. (e) Manifests: author,
  repository, marketplace description (validate warnings). (f) Lint + CI:
  trigger fired, owner consciously deferred again — the only writer is
  the owner, who reviews every diff (commit protocol); new trigger: a
  second person with write access, or a public release. The five rules
  stay specified in spec.md; the manual checklist lives in CLAUDE.md and
  docs/release.md step 5. (g) R-3 trigger refined: a second *user* does
  not fire the machinery trigger when that user is read-only — briefs
  travel as issues; the manual loop stays. → v0.11.1 (patch: nothing
  workspace-facing).
- D-49 (2026-08-19, retro round 8, in-chat, team onboarding) Code repos
  become self-sufficient session homes; the team joins through the
  plugin. Observations (Vladimir, in-chat): (1) code repos have no
  CLAUDE.md — an ad-hoc session had to be pointed by hand at the contract,
  overview and ADRs; (2) no sanctioned path for small changes without a
  task; (3) a new teammate is being onboarded — clone, tools, integrations,
  per access level; (4) code-repo READMEs must state prerequisites; (5) the
  upgrade flow across versions and repos, PRs, whether code repos need a
  pin; plus three new asks: conversation in the teammate's language with
  English artifacts, next scoped per area/repo, reads via GitHub first.
  Root-caused against plan step 6 (git init + minimal README + contract —
  nothing a session auto-loads), implement (capsule reads the workspace
  CLAUDE.md, so only skill-driven sessions inherited the rules; branched
  from wherever the checkout sat), the registry (no remote URL — a fresh
  workspace clone cannot reconstruct the constellation; D-33's
  "collaborator without local siblings" trigger), upgrade (per-repo commits
  ignored `merge_flow`), next (code-repo mode filtered tasks only), the
  workspace template (no artifact-language rule), Claude Code's memory
  imports (verified in docs: relative to the importing file, external
  imports approved once per project, four hops) and its `language` setting
  (verified in the installed 2.1.235 binary: "Preferred language for
  Claude responses"). Verdicts: (1) confirmed — structural, contra D-41
  self-sufficiency; (2) refined — D-45's standalone task is too heavy for a
  docstring and the "mandatory Task footer" was already relaxed by
  D-38d/D-40: the line is drawn, refactors challenged onto the task side
  (Karpathy §4) and the owner agreed; (3) confirmed, two gaps (registry
  remote; procedure) — access is derived from GitHub, never stored (D-46
  holds); the P-4 tension (prospective need) was stated and overridden by
  the real onboarding; (4) stands as stated; (5) mostly already designed
  (D-32/D-40: one run in the workspace, notes walked in order, per-repo
  scan) — two gaps (merge_flow; documentation), D-40 reaffirmed; language
  → user-level setting + artifact language chosen at init (Vladimir's
  refinement over a fixed English rule), no per-command argument; scoped
  next by registry name or role; "GitHub first" challenged — wrong for
  local-rebase mainlines and for the workspace, and repo-reader needs a
  filesystem — refined to git fetch-first with a temporary worktree of
  origin/<default>, local as flagged fallback. Resolution, all approved
  (A–G + Q1–Q4): (a) templates/code-claude.md — imports
  `@.spectacular/contract.md` + `@../<workspace>/CLAUDE.md` (define once),
  routing (truth in the workspace, never copied; why = overview + ADR
  outcome sections; task vs housekeeping; architecture problems go back to
  the workspace; contract gaps repo-local), fallback pointer; plan writes
  it, upgrade scans it; (b) housekeeping rule — D-37 (h), workspace
  template commit protocol + "Work outside a PRD breakdown" third bullet;
  (c) templates/code-readme.md with Prerequisites — bootstrap interview
  proposes them, scaffold task verifies "a machine with only these runs
  build/test/run", implement's landing gate adds what a task introduced,
  upgrade scans; (d) registry `remote` column (plan fills, upgrade
  backfills from origin) and `role` = area key; (e) skill onboard (sonnet):
  plugin vs pin → fresh workspace → reachability per registry remote
  (ls-remote; refused = no access) → area pick over reachable roles →
  clone chosen → README prerequisites checked, installs only under a gate
  naming the tools → integrations derived (gh, design-tool MCP — never
  configured) → orientation; idempotent; (f) upgrade lands code-repo change
  sets per `merge_flow` (PR / mainline commit), reports unreachable repos,
  scans CLAUDE.md/README/registry; README Update paragraph; (g) workspace
  template: Language section (`<artifact-language>` filled by init), Fresh
  before derived, §5 read-fresh bullet; init asks the artifact language;
  next `[repo-name | role]` scoped derivation with a one-line
  workspace-level footer, workspace fetch; implement branches from fetched
  origin/<default>; repo-reader dispatch lines (plan, decide) and the
  agent's "read as given"; retro translates observations into the artifact
  language. D-33 stays deferred with its trigger partly met by git; D-46
  deferral held. → v0.12.0 (minor: new skill, new templates, workspace
  template sections).

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
- OQ-14 resolved 2026-08-19 → D-48 (team share: same repo, history intact). Original
  framing kept: Release mechanics for v0.1 (deliberately decided at release time — not
  blocking): fresh published repo receiving one clean v0.1 commit (keeps private
  iteration history; airtight against design-zone leakage) vs same-repo orphan
  squash + force-push (one repo, but destroys the iteration history and
  force-pushed-away commits can linger fetchable on GitHub for a while). Trigger:
  tracer bullet complete and release near.
- OQ-15 resolved 2026-08-18 → D-45 (standalone tasks) + D-46 (bug flow); the
  original framing kept below for the record.
- OQ-15 (opened 2026-08-18, retro question in the plugin repo) Singular work
  outside a PRD breakdown: (a) a bug in an already-accepted (done) story;
  (b) operations/maintenance work with no product story at all (e.g. a
  DevOps engineer adding a team member through IaC). Root cause against the
  skills: D-19 makes PRD → story → task mandatory and only plan writes tasks
  (breakdown or acceptance-FAIL re-plan), so (b) is impossible today, and
  (a) is only reachable via a manual late-FAIL log entry + `plan story-NNN`
  — undocumented, and no rule says how a `done` story returns to
  `in-progress`. Proposal under gate: (a) is a *late acceptance FAIL*, not
  a new task — re-plan mode accepts a defect description, logs the FAIL,
  flips the story back to in-progress, adds fix tasks; the D-22 loop then
  runs to a fresh PASS. (b) **standalone tasks** — a task file with no
  `story:` (repo + Verification required), authored by a third plan mode
  from a free-text argument, challenged when it smells like new
  user-visible behavior; implement/next/DoR gain "(if any)" clauses;
  D-19 amended to "mandatory spine for capability delivery". P-1/P-4
  tension noted (delivery back half not yet run for real): build now iff a
  real case exists, else defer with that trigger — Vladimir's call.

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
  were processed in this repo (retro round, D-26…D-30, v0.2.0); a second
  retro round after the pilot's stack ADR produced the repo-bootstrap
  conventions machinery (D-38, v0.7.0); plan has run (six stories, 21
  tasks across three repos) and implement has landed two scaffold tasks
  and reached the gate on a third — retro round 6 (D-47, v0.11.0) came out
  of those runs. Remaining: ≥1 story through acceptance PASS, on the
  updated plugin.

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
- S-6 (cont. 6) 2026-08-04: Retro round 2 from the pilot, in-chat (no
  observations file in this repo — plugin-mode retro). After the pilot's
  foundational stack ADR, Vladimir asked whether decide should also have
  covered repo-internal architecture, created the repo, and defined
  repo-specific principles (async-first, DDD, test fixtures/factories,
  package manager, multistage Docker), wanting a repeatable
  from-day-1 elicitation per code repo. Root-caused against the skills:
  decide's one-decision scope and plan's repo-creation ownership both
  CONFIRMED correct (challenged his fold-into-decide framing); the
  elicitation gap CONFIRMED as stated — plan filled Conventions "as the
  owner intends" with no interview, template heading empty, while the
  pilot's own ADR flagged unset conventions as an accepted risk. Four
  fixes proposed; Vladimir ratified all with refinements (open
  dimension list derived from the repo's decided architecture;
  interactive options with a recommended one; a contract-amendment
  method distinct from ADR-level changes) → D-38 applied across
  contract template, plan, implement, decide, spec → v0.7.0. He will
  test via the pilot's next plan session. Commits proposed per
  protocol.
- S-6 (cont. 7) 2026-08-11: Retro round 4 — first findings from a second
  workspace (wardx/gdansk), in-chat. Two observations root-caused: (1)
  /next never surfaces decide/plan for approved PRDs — confirmed
  structural (step 4 derives no plannable-PRD or pending-decision
  candidates, so the recommendation collapses to stub development); (2)
  multi-PRD planning — split three ways: decide already product-scoped
  (overturned), a persisted decision backlog missing (confirmed),
  interleaved story order = plan's missing sibling-PRD/story context
  (confirmed as cross-PRD depends_on gap; a stored schedule refused per
  D-18). Fixes proposed: A next candidate classes, B plan sibling context
  + PRD sets, C decide map mode → ADR stubs. Vladimir replied "keep on
  working"; Fix A was partially applied and he interrupted — the reply
  was not approval (the session had merely looked stuck to him). Fix A
  reverted. His directive: skills must make discussion-first and
  justified-challenge explicit. Nine-skill compliance audit run; his
  "all skills" framing challenged (decision points only; he confirmed
  next needs nothing); C1 gate protocol / C2 plan clarify pass +
  implement ambiguity stop / C3 uniform challenge line each explicitly
  approved → D-41 applied (workspace-claude template gains ## Gate
  protocol + self-sufficiency bullet; one-line gate references in init,
  prd, design, decide, plan, implement, upgrade, retro; plan steps
  renumbered 3→10 with clarify inserted; spec cross-cutting + plan flow;
  WoW #9; stale "plan step 5" pointer fixed in upgrades.md 0.7.0 note).
  Also his rule, now encoded: never rely on session memory for process —
  all three repo kinds self-sufficient for a possible team, identical
  across machines/accounts. Retro fixes A/B/C pending re-gate under the
  new protocol; release intended as one 0.9.0 once they settle. Commits
  proposed per protocol, uncommitted.
- S-6 (cont. 8) 2026-08-12: Vladimir approved the compliance diff and,
  re-gated per the new protocol, all three retro fixes explicitly (A
  approve / B agree / C agree) → D-42/D-43/D-44 applied across next, plan,
  decide, spec. Two open points handled per D-31/D-41: (1) his "each
  commit should have a version bump" challenged against his own D-37
  (tags mark releases, commits never stamp versions) — his fallback
  option taken instead: compliance batch staged separately, retro fixes
  layered on top, one chore(release): 0.9.0 to follow; (2) his floated
  bare-plan-plans-everything idea analyzed on his ask (10 PRDs ≈ 300 work
  items: context exhaustion, unreviewable gate, stale-by-implementation
  stories) → recommended and encoded as suggest-target-or-coupled-set,
  never plan-all (D-43); he confirmed. Gate protocol exercised as
  designed: his partial approval landed commit 1 alone (51ab9e9); the
  rest stayed proposals until his explicit "all changes are approved" —
  then feat commit 2, chore(release): 0.9.0, tag v0.9.0, push and local
  plugin update, all on his ask.
- S-6 (cont. 9) 2026-08-18: Retro question in-chat: how to create singular
  tasks — a bug fix on a done story; an ops/IaC change with no story.
  Root-caused against plan/implement/next/templates (see OQ-15): the
  bug case is a late acceptance FAIL that D-22 already covers but no
  skill documents past first acceptance; the ops case is structurally
  impossible under D-19. Proposal (late-FAIL re-plan + standalone tasks)
  presented with an explicit gate; nothing applied, no commit. Awaiting
  Vladimir: real case or hypothetical (P-4), and which parts to build.
  His answer: hypothetical; both approved anyway (P-4 consciously
  overridden — "not possible at all" is a wall for any real team); on A he
  raised a gap: the reporter usually does NOT know which story a bug
  belongs to — wants intake of what happened → agent-driven investigation
  (artifacts + code repos, clarifying questions until confident or a few
  options) → the ticket planned by the agent; cites the usual QA→assign→
  investigate→fix/hand-over flow. Bug-flow design proposed (bug report
  artifact + cheap capture skill, triage as a plan mode); awaiting his
  explicit approval before applying A+B together. His round 2: (1)
  capture must NOT be zero-question — elicit best-practice bug evidence
  against a bug DoR, bounded, then structure and file (conceded: the
  reporter's context is richest at report time; my zero-question idea
  imported retro's rationale wrongly); (2) confirm triage routes, never
  closes a fixable bug, and devs implement tasks not bugs (correct — only
  not-a-bug/duplicate/can't-reproduce close at triage); (3) triage must
  not read every story/task on a big project → narrowing funnel (front
  matter + slugs → candidates → bodies → repo-reader on candidate repos
  only → widen only on ask). Refined design pending his approval.
  "approve design" → D-45/D-46 applied: new skills/bug + templates/bug.md;
  plan rewritten into breakdown / fix (known story + late FAIL, bug triage
  funnel + routing) / standalone modes; implement (story-optional DoR and
  capsule, bug evidence in capsule, bug close-out); next (bug classes,
  ranking, closing edits, standalone labels); task template (story:
  optional), workspace CLAUDE.md template (bugs row, "Work outside a PRD
  breakdown", bug DoR/DoD, grain); generate-docs lifecycle + regenerated
  commands.md; README, models.md; spec.md throughout ("ten skills").
  Release files staged for chore(release): 0.10.0. Commits proposed per
  protocol. Vladimir: "approved. commit, push and update plugin locally"
  → feat commit d016c35, chore(release): 0.10.0 commit 2971149, tag
  v0.10.0; push impossible — the repo has no remote configured (and no
  GitHub repo exists yet; README still describes the local-checkout
  install), reported, no remote invented; local plugin updated via
  `claude plugin marketplace update spectacular` + `claude plugin update
  spectacular@spectacular` → 0.10.0 in the cache (restart to apply).
- S-6 (cont. 10) 2026-08-18: Retro round 6 in this repo, review mode —
  Vladimir's in-chat observation (implement spends 5–10 minutes and ~150k
  tokens before the first line of code, in the api and the web repo) plus
  the workspace retro's briefs P1–P3 (its W1/W2 already applied locally
  there). Evidence taken from the three implement transcripts — tool-call
  timelines, context size at first write, thinking-block sizes — rather
  than memory; verdicts and the four-part fix recorded as D-47: P1
  confirmed for ADRs/PRD and challenged for the overview; P2 confirmed
  with plan-after-capsule and a no-whole-tree clause; P3 confirmed with
  gate-time triage; "tasks not hard" challenged (scaffold = whole
  contract); baseline tests / docker check not a defect; invisible
  deliberation at xhigh effort named as an owner-held lever (models.md).
  Presented with an explicit gate naming items A–E; "approve all" →
  applied across implement (steps 2, 3, 5, 6, 7, 8), workspace-claude /
  contract / task templates, models.md, spec.md; release files staged for
  chore(release): 0.11.0 (minor — template changes are workspace-facing;
  upgrade note: CLAUDE.md §5, per-repo Toolchain notes heading via the
  drift scan). Commits proposed per protocol; landed on his ask as
  bf44b5f (feat) + fe843e4 (chore(release): 0.11.0), tag v0.11.0.
- S-7 (round 7) 2026-08-19: Retro review in this repo — publication
  readiness. Vladimir wants a private GitHub repo shared read-only with
  his team; asks whether tmp.md and design/STATE.md belong, and how to
  keep the repo lean yet extensible via retro. Root-caused against the
  tree, D-12/D-24/OQ-14/R-3 and a manual run of the five deferred lint
  rules over shipped files (all clean except: README does not reference
  docs/release.md — D-24 note 4 violated since 0.6.0). Findings: tmp.md
  is unreferenced beyond this file's pointer, condensed here since S-1,
  and carries a client-machine absolute path → delete; STATE.md is the
  plugin's decision log and the retro loop's evidence → stays, but the
  plugin repo has no CLAUDE.md, so its ways of working live only in the
  design zone (contra D-41 self-sufficiency); D-24's lint+CI trigger and
  D-12's design-zone exclusion collide with a team that must extend the
  plugin; OQ-14 must resolve now. Proposal presented under an explicit
  gate (items A–H + the one owner decision: design zone visible to the
  team with history intact, vs clean root). Vladimir: all items except D
  (lint + CI — deferred again, new trigger recorded), history intact;
  Claude creates the GitHub repo and pushes, he adds readers by hand.
  Applied as D-48: tmp.md deleted; CLAUDE.md written, Ways of working
  moved there; README publication edits; retro SKILL.md issues clause;
  manifests; docs/release.md step 5; spec.md layout + lint section;
  denylist header; D-4/D-12/OQ-14/Deferred updated. Release
  chore(release): 0.11.1 (patch), tag v0.11.1. Repo created and pushed
  with all tags on his ask: github.com/oswalth/spectacular (private);
  readers added by Vladimir by hand. Local plugin cache not touched (not
  asked) — the local marketplace still points at the checkout.
- S-8 (round 8) 2026-08-19: Retro review in this repo — Vladimir's in-chat
  suggestions after working in the pilot's api repo and while onboarding a
  new teammate (five observations + three new asks; see D-49). Evidence:
  plan/implement/upgrade/next skills, the templates, D-32/D-37/D-40/D-45/
  D-46, Claude Code docs for CLAUDE.md `@` imports and the installed binary
  for the `language` setting. First gate (A–G + three owner calls):
  approved with "agree" on the verdicts (refactors task-side, onboard now,
  import-based CLAUDE.md) and one refinement — onboarding must respect
  access levels; second gate (Q1–Q4): derived access + role as area key,
  user-level conversation language + artifact language chosen at init,
  scoped next by name/role with a footer, fetch-first via git instead of
  GitHub reads — all agreed. Applied in one pass: templates code-claude /
  code-readme (new), workspace-claude (Language, Fresh before derived,
  housekeeping bullet, commit-protocol footer wording, §5 read-fresh);
  skills init (language question, registry `remote` + role semantics,
  README pointer), plan (three plugin-owned files, prerequisites in the
  interview, scaffold verification line, read-fresh dispatch), implement
  (branch from fetched origin, README prerequisites at the gate), decide
  (read-fresh dispatch), upgrade (scans + merge_flow landing + unreachable
  repos), next (scope argument, scoped derivation, footer, workspace
  fetch), retro (observation language), onboard (new); repo-reader note;
  generate-docs LIFECYCLE + commands.md; models.md; README; upgrades.md
  0.12.0; CHANGELOG 0.12.0; plugin.json 0.12.0; spec.md throughout;
  D-33/D-37/D-40/D-46 notes here. Commits proposed per protocol; on
  Vladimir's "commit, release, push, update local plugin": feat d8e8004,
  chore(release): 0.12.0 8de1573, tag v0.12.0, pushed to
  github.com/oswalth/spectacular with tags; local marketplace (now GitHub
  source) refreshed and the plugin updated 0.11.1 → 0.12.0 at user scope
  (restart to apply). Open evidence: the first real `/spectacular:onboard`
  run and the pilot's `/spectacular:upgrade` to 0.12.0 (registry remotes,
  code-repo CLAUDE.md/README sets via PRs, Language section).
