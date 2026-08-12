---
name: implement
description: Execute one task inside a code repo — compile the just-in-time context capsule from the workspace, run a goal-driven loop until verification passes, and land exactly one squashed mainline commit behind the owner's landing gate.
argument-hint: [task-NNN]
---

# /spectacular:implement — execute a task

Runs **in a code repo**, not the workspace. One invocation drives one task from
`todo` to `done`: one branch, one squashed mainline commit — landed only on the
owner's explicit greenlight.

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
   - the design spec sections the task's Design references name (`design-NNN`);
     for any UI task additionally the distilled design system when present —
     `product/designs/system/tokens.json` and `design-language.md` ALWAYS
     ride in the capsule, and generated UI references tokens, never invented
     values. Open the raw imported design code only when a specific
     component's look needs it; pull Figma frames through the connected
     design-tool MCP when one is available; otherwise ask the owner to
     confirm visuals from the links before building UI. Imported design code
     is reference for look and feel — translate it to this repo's stack and
     idioms, never paste it in;
   - `architecture/overview.md` and ADRs touching this repo;
   - this repo's `contract.md` (stack, commands, conventions);
   - the Learnings sections of this story's already-done tasks.

   The capsule is compiled fresh every time and never stored.
4. **Mark in-progress.** Task `status: in-progress`; the story too if it was
   `todo`.
5. **Goal-driven loop.** Before writing code, restate the task's Verification as
   a concrete, runnable check (test command, expected behavior) — extend the
   task's Verification section if it was vague. If the capsule genuinely
   underdetermines the task — two readings implying different code — stop
   and ask the owner before building; never pick an interpretation
   silently. Branch `task-NNN-<slug>`.
   Implement, run the verification, loop until it passes. Use the contract's
   build/test/run commands.
6. **Landing gate — nothing lands without a greenlight (D-39).** Verification
   green does not end the loop; it opens the gate. Present, in one stop:
   - what changed — the files touched and a short diff summary;
   - the verification evidence — the check that ran and its passing result;
   - the proposed code-repo commit message, per Conventional Commits 1.0.0 —
     subject `type(scope): summary` with the type matching the change
     (`feat`, `fix`, …) and footer `Task: task-NNN` (D-37; the task id never
     goes in the subject);
   - what landing will do per the contract's `merge_flow` (below);
   - the workspace close-out commit that follows in step 7 (statuses,
     Learnings).

   Then wait for the owner's explicit approval — an approve-like answer to
   this explicit question; "ok, continue"-style replies do not open the
   gate, re-ask (gate protocol, workspace CLAUDE.md). No commit, push, PR,
   or merge happens before it — "verification passed" is a report, not a
   license. One
   greenlight covers landing the whole task: this code-repo commit and the
   step-7 workspace commit. On approval, land per `merge_flow`:
   - `pr`: push the branch, open a PR with `gh`, squash-merge it (`gh pr merge
     --squash`).
   - `local-rebase`: squash the branch to one commit, rebase onto the mainline,
     fast-forward it. Pushing the mainline stays on explicit ask.

   One task = exactly one squashed mainline commit either way (D-21), history
   linear. Commits never bump versions or create tags: the release act (when
   to ship, derive the bump from CC types since the last tag, tag `vX.Y.Z`)
   belongs to the contract's `versioning`/`release_flow` and follows
   `${CLAUDE_PLUGIN_ROOT}/docs/release.md` (D-37).
7. **Close out.** Walk the task's Definition of Done (workspace CLAUDE.md)
   explicitly and confirm each item: Verification passes, exactly one squashed
   mainline commit, Learnings appended, `status: done`. Learnings carry what
   the next task's capsule should know (surprises, decisions, sharp edges —
   not a diary).
   If this was the story's last open task, announce that the story is now
   **awaiting acceptance** and print its AC checklist for the human tester, plus
   how to record the verdict (see below).

   The **workspace** edits this step makes (statuses, Learnings) land as
   their own workspace commit (e.g. `docs(task-NNN): done — status +
   learnings`) under the step-6 greenlight — it covered both commits, so
   commit now without re-asking. A greenlight never carries across tasks or
   sessions (D-39). Pushing the workspace stays on explicit ask (workspace
   commit protocol, CLAUDE.md).
8. **Discovered problem in workspace truth?** If the work reveals an
   architecture or spec problem, never edit workspace truth directly — write
   `changes/NNN-<slug>/proposal.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/change-proposal.md` (`status: draft`)
   and say so. Continue the task if possible; otherwise stop and name the
   blocker.

   A gap in this repo's **contract** is different — a convention never
   decided (say, no testing framework was ever picked) is not workspace
   truth. Propose the amendment; on the owner's approval edit `contract.md`
   directly — it rides the task branch, or lands as its own
   `chore(contract): …` commit when no task is in flight. But an amendment
   that would contradict an approved ADR (e.g. switching frameworks) IS a
   workspace-truth problem: superseding ADR via `/spectacular:decide` first,
   then re-plan what it invalidates.

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
