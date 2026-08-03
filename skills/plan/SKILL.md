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
3. **Propose stories:** user-visible slices of the PRD. Every PRD AC maps to at
   least one story; each story lists the ACs it covers, plus `depends_on`
   between stories where ordering is real. A story's Goal is the Connextra
   line (*As a <user>, I want <capability>, so that <benefit>*); its ACs
   restate the covered PRD ACs as Given/When/Then test scripts a human can
   execute step by step. Sanity-check each story against INVEST — independent,
   negotiable, valuable, estimable, small, testable.
4. **Propose tasks per story,** routed to repos. Each task carries a
   description and a **Verification** section — preconditions, numbered steps,
   expected result — written before any code exists. Stories and tasks
   implementing designed UI carry **Design references** — the design spec
   sections and source frames they realize (`design-NNN` + links).
5. **Missing repo?** Propose creating it (consult `conventions.md` for the name
   if present, else `<product>-<role>`, e.g. `acme-api`): sibling directory per
   `.spectacular/profile.md`, `git init`, minimal README, and
   `.spectacular/contract.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/contract.md` — fill the workspace
   back-pointer, the registry name, and the stack/commands/conventions the
   owner intends. The owner picks `merge_flow` at creation (`pr` needs a remote
   and `gh`; `local-rebase` needs neither). Append the repo to the registry.
   History stays linear either way, and task branches are always squashed.
6. **Epic-trigger check.** Epics do not exist in v0.1. If any of these fires,
   say so explicitly and recommend recording it with
   `/spectacular:retro "epic trigger fired: …"` — that firing is the build
   trigger for epic machinery, not a license to improvise it now:
   - the owner states phased delivery of this PRD;
   - one goal pulls stories from more than one PRD;
   - more than ~12 stories for one PRD.
7. **Blocking consistency check** — repair your own proposal and re-check until
   all four pass; only then gate:
   - every PRD AC maps to ≥ 1 story;
   - every story has ≥ 1 task;
   - every task's `repo:` exists in the registry;
   - the combined story+task dependency graph is acyclic;
   - every story covering designed UI references an approved design spec,
     when the PRD has one (skipped only if the owner explicitly planned
     without a design spec in step 2).
8. **Gate.** Present the breakdown: stories with AC coverage, tasks with repo
   routing, any repos to create. On approval, create the repos and write the
   files, everything `status: todo`:
   - Story — `delivery/stories/NNN-<slug>.md` from
     `${CLAUDE_PLUGIN_ROOT}/templates/story.md`. The task list is never
     duplicated into the story body; it is derived from task files' `story:`
     links.
   - Task — `delivery/tasks/NNN-<slug>.md` from
     `${CLAUDE_PLUGIN_ROOT}/templates/task.md`, its Verification section
     filled from step 4.

   Everything written under this gate must meet the workspace's Definitions of
   Ready (workspace CLAUDE.md) — plan is the skill that makes items ready.

9. **Propose a commit** for the batch — workspace stories/tasks plus registry
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
