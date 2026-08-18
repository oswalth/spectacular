---
name: plan
description: Turn intent into ready tasks — break an approved PRD into stories and per-repo tasks (creating missing code repos with contracts) behind a blocking consistency check; fix a story after an acceptance FAIL or a defect found later; triage a bug report and route it to the work that fixes it; or write one standalone task for maintenance work with no story.
argument-hint: [prd-NNN … | story-NNN ["<defect>"] | bug-NNN | "<standalone task>"]
---

# /spectacular:plan — delivery breakdown

Turns intent into delivery artifacts: **stories** (user-visible slices) and
**tasks** (one repo's share of a story — or, for maintenance work, a
standalone task with no story). PRD → story → task is the mandatory spine
for capability delivery — every story names its `prd:`, every task its
`repo:`, and every task that delivers a story names its `story:`. plan is
the only skill that writes tasks, so the Definitions of Ready (workspace
CLAUDE.md) are enforced in one place.

Mode is chosen by the **content** of the argument:

- one or more `prd-NNN`, or no argument → **breakdown**;
- `story-NNN`, optionally followed by a defect description → **fix** for a
  known story (acceptance FAIL, or a defect found after acceptance);
- `bug-NNN` → **fix** via triage: find where the cause lives, then route;
- anything else — free text that is not a reference → **standalone task**.

A breakdown set is for tightly-coupled PRDs (2–3, no more) whose stories
genuinely interleave — one combined proposal, one gate; the owner's review
sitting grows with every PRD added, so coupling must earn its place.

## Breakdown

1. **Precondition:** every target PRD has `status: approved`; otherwise refuse
   and point at `/spectacular:prd`. No argument → suggest a target — the
   plannable PRD that unblocks the most, as a coupled set when its stories
   could not be ordered without a sibling — and let the owner confirm. Never
   plan every plannable PRD in one run: breakdown happens just-in-time, per
   PRD or small set, so each gate stays reviewable and later PRDs get
   planned against the learnings of implemented ones.
2. **Context:** read the target PRD(s), their approved design specs
   (`product/designs/` with `prd:` matching), `architecture/overview.md`,
   ADRs touching them, and `.spectacular/registry.md`. Also read every
   *other* approved PRD's front matter and scope, and all existing stories
   and tasks — ordering rarely stops at a PRD boundary, and the
   `depends_on` links proposed below are expected to cross it. If the PRD
   has user-facing surface and no
   design spec, say so and recommend `/spectacular:design` first — the owner
   may explicitly choose to plan without one. For each registered repo
   plausibly involved,
   dispatch the **repo-reader** subagent with the repo path and one specific
   question (what relevant capability exists, where the integration points are).
   Never guess at code you can inspect.
3. **Clarify pass.** When the PRD admits materially different breakdowns —
   slicing strategy, phasing, what ships first, story granularity — run at
   most 5 propose-then-ask questions: frame the option you recommend and
   why, and let the owner pick before stories are drafted. Challenge a
   slicing the owner dictates when it breaks INVEST or hides a dependency —
   justification plus a proposed alternative, their call final. Skip when
   the artifacts genuinely determine the breakdown, and say that you are
   skipping.
4. **Propose stories:** user-visible slices of the PRD. Every PRD AC maps to at
   least one story; each story lists the ACs it covers, plus `depends_on`
   between stories where ordering is real — including stories of other PRDs,
   already on disk or proposed in this same run. Execution order is never
   stored: with cross-PRD links written, `/spectacular:next` derives the
   interleaving. A story's Goal is the Connextra
   line (*As a <user>, I want <capability>, so that <benefit>*); its ACs
   restate the covered PRD ACs as Given/When/Then test scripts a human can
   execute step by step. Sanity-check each story against INVEST — independent,
   negotiable, valuable, estimable, small, testable.
5. **Propose tasks per story,** routed to repos. Each task carries a
   description and a **Verification** section — preconditions, numbered steps,
   expected result — written before any code exists. Stories and tasks
   implementing designed UI carry **Design references** — the design spec
   sections and source frames they realize (`design-NNN` + links).
6. **Missing repo?** Propose creating it (consult `conventions.md` for the name
   if present, else `<product>-<role>`, e.g. `acme-api`): sibling directory per
   `.spectacular/profile.md`, `git init`, minimal README, and
   `.spectacular/contract.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/contract.md` — fill the workspace
   back-pointer, the registry name, and the stack/commands from the ADRs that
   forced the repo. The owner picks `merge_flow` at creation (`pr` needs a
   remote and `gh`; `local-rebase` needs neither). Append the repo to the
   registry. History stays linear either way, and task branches are always
   squashed.

   **Repo-bootstrap interview** — fill the contract's Conventions before the
   repo's initial commit; propose-then-ask, never a blank page:
   - *Frame first:* what the forcing ADRs already settle (stack, plus any
     conventions decided there), and defaults proposed from already-registered
     repos' contracts where a dimension carries across the product — that is
     what makes conventions repeatable between repos.
   - *Walk the dimensions:* the template's common core (architecture style,
     testing, tooling, build & packaging, quality gates) PLUS the
     stack-specific ones this repo's decided architecture implies — e.g.
     sync/async posture for an API, state management for a SPA, dataset
     versioning for ML. The list is open: derive it from the decisions, do
     not stop at the template.
   - *Per open dimension:* offer realistic options with one marked
     recommended and a one-line justification; the owner picks. A dimension
     that turns out genuinely contested and hard to reverse is a decision,
     not an interview answer — recommend `/spectacular:decide` for it.

   **Scaffold first task.** The new repo's first task materializes the
   contract — project skeleton, tooling, test harness with the decided
   fixture/test-data strategy, build & packaging — and its Verification
   checks each convention the interview recorded. For a UI repo, when
   `product/designs/system/tokens.json` exists: the contract's conventions
   name it as the theme source, and the theme bootstrap (materialize the
   tokens into the repo's stack — CSS variables/Tailwind, or the platform
   theme) folds into the scaffold task or follows it as the first UI task.
7. **Epic-trigger check.** Epics do not exist in v0.1. If any of these fires,
   say so explicitly and recommend recording it with
   `/spectacular:retro "epic trigger fired: …"` — that firing is the build
   trigger for epic machinery, not a license to improvise it now:
   - the owner states phased delivery of this PRD;
   - one goal pulls stories from more than one PRD;
   - more than ~12 stories for one PRD.

   A multi-PRD breakdown run is not the second trigger: that trigger is one
   goal spanning PRDs; a set run is several goals planned together, each
   story still naming exactly one `prd:`.
8. **Blocking consistency check** — repair your own proposal and re-check until
   all four pass; only then gate:
   - every PRD AC maps to ≥ 1 story;
   - every story has ≥ 1 task;
   - every task's `repo:` exists in the registry;
   - the combined story+task dependency graph — proposed items plus
     everything already on disk — is acyclic;
   - every story covering designed UI references an approved design spec,
     when the PRD has one (skipped only if the owner explicitly planned
     without a design spec in step 2).
9. **Gate.** Present the breakdown: stories with AC coverage, tasks with repo
   routing, any repos to create. For a multi-PRD run, group stories per PRD
   and show which are immediately ready versus blocked, so the derived
   interleaving is visible at approval time. Ask explicitly; only an explicit
   approve-like answer approves, and partial approval keeps the rest
   proposals (gate protocol, CLAUDE.md). On approval, create the repos and
   write the files, everything `status: todo`:
   - Story — `delivery/stories/NNN-<slug>.md` from
     `${CLAUDE_PLUGIN_ROOT}/templates/story.md`. The task list is never
     duplicated into the story body; it is derived from task files' `story:`
     links.
   - Task — `delivery/tasks/NNN-<slug>.md` from
     `${CLAUDE_PLUGIN_ROOT}/templates/task.md`, its Verification section
     filled from step 5.

   Everything written under this gate must meet the workspace's Definitions of
   Ready (workspace CLAUDE.md) — plan is the skill that makes items ready.

10. **Propose a commit** for the batch — workspace stories/tasks plus registry
   changes as one unit (e.g. `plan prd-001: stories and tasks`); commit only
   on the owner's explicit approval (workspace commit protocol, CLAUDE.md).
   A newly created code repo gets its own initial commit, likewise proposed.

## Fix (acceptance FAIL, later defect, or bug triage)

One loop, two entry points. It ends with fix work that meets the task DoR;
the human acceptance loop (D-22) then runs again — a fixed story is
re-tested to a fresh PASS, never assumed.

**Known story** — `story-NNN`, or a story whose Acceptance log ends in FAIL:

1. Read the story and its FAIL entry. If the owner reports the defect as the
   argument (`plan story-004 "checkout total ignores the discount"`), the
   FAIL entry does not exist yet: propose it — `<date> — <owner> — FAIL:
   <defect>` — and, when the story is already `done`, its return to
   `status: in-progress`; both land under the gate below (a defect in an
   accepted story is a late acceptance FAIL — the story is not done while
   one of its ACs is violated). Manual edits remain legitimate.
2. Diagnose: dispatch repo-reader on the suspect repos (the story's tasks'
   `repo:` values) with the failure as the question.
3. Propose reopening tasks (`status:` back to `todo` plus a note pointing at
   the FAIL entry) and/or new fix tasks under the same story. A fix task's
   Verification starts from the reproduction: the check that fails today
   and must pass (Karpathy #4). Reopened or new work mechanically takes the
   story out of awaiting-acceptance.
4. Gate — explicit question, explicit approval (gate protocol, CLAUDE.md) —
   then apply. Loop with the human tester until the story's log ends in
   PASS.

**Bug report** — `bug-NNN` (filed by `/spectacular:bug`):

1. **Read the report.** Gaps against the bug DoR (workspace CLAUDE.md) are
   your first questions to the reporter or owner — the whole triage spends
   at most **5** propose-then-ask rounds, including the convergence step
   below.
2. **Narrow before you read** — triage compiles what it needs, like the
   implement capsule; it never reads every story of a large product:
   - *Index, cheap:* front matter and filename slugs only — PRDs, design
     specs, stories, tasks — plus the registry. Nothing else yet.
   - *Candidates:* match the report's *where* (page, screen, flow,
     component) against those slugs and design-spec screen names →
     candidate PRD(s) → their stories. Open the **bodies** of candidate
     stories only (their ACs) and the Learnings of their done tasks —
     default cap around 5–8 stories; only the owner widens it.
   - *Repos:* the candidate tasks' `repo:` values → dispatch repo-reader on
     those repos only (usually one or two), question = the symptom plus the
     suspected component; it reads only what bears on the question.
   - *Architecture:* `architecture/overview.md` always; ADRs only those
     touching the candidate repos.
   - *Nothing narrows?* Ask the reporter before reading wider; still
     nothing → ask the owner to name a PRD or repo. Always state what you
     did not examine.
3. **Converge.** Confident → name the cause and where it lives (story and
   violated AC, or repo and component). Not confident → present 2–3
   candidate causes with their evidence and let the owner pick; that
   question counts within the 5 rounds. Never route on a guess presented as
   a finding.
4. **Route — one gate covering the whole set:**
   - a story's AC is violated → the known-story loop above: FAIL entry
     citing `bug-NNN`, story back to `in-progress` if it was done, fix
     task(s) per repo — or an existing not-yet-done task that already
     covers the fix;
   - no AC violated but real work is needed → standalone task(s), per the
     mode below;
   - not a defect → close the bug at triage with a Resolution: spec gap
     (open `changes/NNN-<slug>/proposal.md` from
     `${CLAUDE_PLUGIN_ROOT}/templates/change-proposal.md` and cite it), not
     a bug, duplicate of `bug-NNN`, could not reproduce, won't fix — with
     why.
   Present the routing and the fix work explicitly; only an explicit
   approve-like answer applies it. On approval write everything: the
   story/task edits, `routed_to: [story-NNN | task-NNN …]` in the bug
   (targets are the work that fixes it — a bug closed at triage gets none),
   and the bug's **Triage** section — date, what was examined and what was
   not, candidates, decision. A routed bug stays `open` until its fix is
   verified: implement closes it when the last routed task lands; a story
   target closes it with the re-acceptance PASS (`/spectacular:next` prints
   the edit).
5. **Propose a commit** — `docs(bug-NNN): triage — routed to <targets>` (or
   `closed: <resolution>`), the story/task files included — committed only
   on explicit approval.

## Standalone task (maintenance work with no story)

For work that keeps the product running without changing what users see —
an IaC change adding a team member, a dependency or runtime bump, a secret
rotation, a data fix. Argument = the free-text request.

1. **Challenge first, once.** If the request adds or changes user-visible
   behavior it is not a standalone task: it belongs to a PRD — a `changes/`
   proposal when the PRD is approved, a new capability otherwise — and then
   a story. Say so with the justification; the owner's call is final, and
   say explicitly when the request stands as a standalone task.
2. **Clarify, at most 3 propose-then-ask questions:** the target repo (from
   the registry, one recommended with a reason), the Verification
   (preconditions, steps, expected — how anyone confirms it is done), and
   `depends_on` if any. Skip what the request already settles.
3. **Draft** `delivery/tasks/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/task.md` **without** the `story:` line —
   `repo:` and Verification are what make it ready (task DoR, workspace
   CLAUDE.md). Description names the why in one paragraph and links the
   ADR or bug it serves when there is one.
4. **Gate** — explicit question, explicit approval — then write the file,
   `status: todo`.
5. **Propose a commit** — `docs(task-NNN): standalone task — <slug>` —
   committed only on explicit approval.

## Next step

Recommend `/spectacular:implement` in the specific repo of the highest-ranked
ready task (all `depends_on` done), naming the task and the repo path — that is
where idea turns into code; after a fix or standalone run, that is the task
just written. If nothing is ready, name the blocker and the command that
clears it. A bug closed at triage with a spec-gap resolution points at its
change proposal's approval instead.
