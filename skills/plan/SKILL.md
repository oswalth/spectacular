---
name: plan
description: Break an approved PRD into stories and per-repo tasks — creating missing code repos with contracts — behind a blocking consistency check; or re-plan a story after an acceptance FAIL.
argument-hint: [prd-NNN | story-NNN]
---

# /spectacular:plan — delivery breakdown

Turns an approved PRD into delivery artifacts: **stories** (user-visible slices)
and **tasks** (one repo's share of a story). PRD → story → task is the mandatory
spine — every story names its `prd:`, every task its `story:` and `repo:`.

Mode: a `story-NNN` argument (or a story whose Acceptance log ends in FAIL)
selects **re-plan**; a `prd-NNN` argument or none selects **breakdown**.

## Breakdown

1. **Precondition:** the target PRD has `status: approved`; otherwise refuse and
   point at `/spectacular:prd`. No argument → suggest the approved PRD with the
   fewest existing stories.
2. **Context:** read the PRD, its approved design specs (`product/designs/`
   with `prd:` matching), `architecture/overview.md`, ADRs touching it, and
   `.spectacular/registry.md`. If the PRD has user-facing surface and no
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
   between stories where ordering is real. A story's Goal is the Connextra
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
8. **Blocking consistency check** — repair your own proposal and re-check until
   all four pass; only then gate:
   - every PRD AC maps to ≥ 1 story;
   - every story has ≥ 1 task;
   - every task's `repo:` exists in the registry;
   - the combined story+task dependency graph is acyclic;
   - every story covering designed UI references an approved design spec,
     when the PRD has one (skipped only if the owner explicitly planned
     without a design spec in step 2).
9. **Gate.** Present the breakdown: stories with AC coverage, tasks with repo
   routing, any repos to create. Ask explicitly; only an explicit
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

## Re-plan (after an acceptance FAIL)

1. Read the story and its FAIL entry in the Acceptance log.
2. Diagnose: dispatch repo-reader on the suspect repos with the failure as the
   question.
3. Propose reopening tasks (`status:` back to `todo` plus a note pointing at the
   FAIL entry) and/or new fix tasks. Reopened work mechanically takes the story
   out of awaiting-acceptance.
4. Gate, then apply. Loop with the human tester until the story's log ends in
   PASS.

## Next step

Recommend `/spectacular:implement` in the specific repo of the highest-ranked
ready task (all `depends_on` done), naming the task and the repo path — that is
where idea turns into code. If nothing is ready, name the blocker and the
command that clears it.
