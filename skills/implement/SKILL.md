---
name: implement
description: Execute one task inside a code repo — compile the just-in-time context capsule from the workspace, run a goal-driven loop until verification passes, and land exactly one squashed mainline commit.
argument-hint: [task-NNN]
---

# /spectacular:implement — execute a task

Runs **in a code repo**, not the workspace. One invocation drives one task from
`todo` to `done`: one branch, one squashed mainline commit.

## Steps

1. **Locate the workspace.** Read `.spectacular/contract.md` here; its
   `workspace:` path leads back. No contract → refuse: this is not a registered
   code repo; repos are created and registered by `/spectacular:plan`.
2. **Select the task.** The `task-NNN` argument if given; otherwise list this
   repo's ready tasks from the workspace (`repo:` matches the contract's
   `name:`, `status: todo`, all `depends_on` done, Verification filled). This
   filter is the task's Definition of Ready (workspace CLAUDE.md) — never
   start a task that fails it; name the missing piece instead. Exactly one
   ready → take it; several → show the list and ask.
3. **Compile the JIT context capsule.** Read exactly these, nothing more:
   - the task file;
   - its story: goal + the ACs this task serves;
   - the slice of the PRD those ACs come from;
   - `architecture/overview.md` and ADRs touching this repo;
   - this repo's `contract.md` (stack, commands, conventions);
   - the Learnings sections of this story's already-done tasks.

   The capsule is compiled fresh every time and never stored.
4. **Mark in-progress.** Task `status: in-progress`; the story too if it was
   `todo`.
5. **Goal-driven loop.** Before writing code, restate the task's Verification as
   a concrete, runnable check (test command, expected behavior) — extend the
   task's Verification section if it was vague. Branch `task-NNN-<slug>`.
   Implement, run the verification, loop until it passes. Use the contract's
   build/test/run commands.
6. **Land — one task, exactly one mainline commit,** message starting
   `task-NNN: `. Per the contract's `merge_flow`:
   - `pr`: push the branch, open a PR with `gh`, squash-merge it (`gh pr merge
     --squash`).
   - `local-rebase`: squash the branch to one commit, rebase onto the mainline,
     fast-forward it.

   History stays linear either way.
7. **Close out.** Walk the task's Definition of Done (workspace CLAUDE.md)
   explicitly and confirm each item: Verification passes, exactly one squashed
   mainline commit, Learnings appended, `status: done`. Learnings carry what
   the next task's capsule should know (surprises, decisions, sharp edges —
   not a diary).
   If this was the story's last open task, announce that the story is now
   **awaiting acceptance** and print its AC checklist for the human tester, plus
   how to record the verdict (see below).
8. **Discovered problem in workspace truth?** If the work reveals an
   architecture or spec problem, never edit workspace truth directly — write
   `changes/NNN-<slug>/proposal.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/change-proposal.md` (`status: draft`)
   and say so. Continue the task if possible; otherwise stop and name the
   blocker.

## Acceptance (context for step 7)

A story with all tasks done is *awaiting acceptance* — a derived state, stored
nowhere. A human tests the whole story against its ACs and records the verdict
by editing the story file: on PASS, append
`<date> — <name> — PASS: <note>` to the Acceptance log and set
`status: done`; on FAIL, append the FAIL line and run
`/spectacular:plan story-NNN` to re-plan.

## Next step

Recommend the next ready task in this repo by reference, with one line on why
it is next. If none is ready here, recommend `/spectacular:next` in the
workspace to re-derive state across all repos.
