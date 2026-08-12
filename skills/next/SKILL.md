---
name: next
description: Derive project state from artifact front matter — pending approvals, ready vs blocked work, stories awaiting acceptance, open changes — render the roadmap as text and a Mermaid graph, and make exactly one justified recommendation.
---

# /spectacular:next — where things stand, what to do

Read-only. State is derived fresh from files on every run — nothing is cached,
nothing is stored.

## Steps

1. **Locate.** `.spectacular/profile.md` here → this is the workspace.
   `.spectacular/contract.md` here → code repo: resolve the workspace via
   `workspace:` and filter task-level output to this repo. Neither → refuse:
   run this in a workspace or a registered code repo; for a brand-new product,
   `/spectacular:init` in an empty directory.
2. **Read front matter only** — brief, PRDs, design specs, ADRs, stories,
   tasks, change proposals, plus the registry. Open an artifact body only
   where derivation needs it (the AC checklist of a story awaiting
   acceptance).
3. **Validate while reading** (warn at the top of the output; never halt):
   references that resolve to no file; statuses outside their vocabulary
   (brief/design: draft·approved; PRD/ADR: stub·draft·approved; story/task:
   todo·in-progress·done; change: draft·approved·applied). This is the only
   workspace validation in v0.1.
4. **Derive** (never trust a stored summary):
   - drafts awaiting approval (brief, PRDs, designs, ADRs, changes);
   - **plannable** = PRD `approved` with no stories naming it in `prd:` — an
     approved spec whose breakdown nobody has run (`/spectacular:plan`);
   - **pending decisions** = ADRs still `stub` — the decision map waiting to
     be worked (`/spectacular:decide`);
   - **ready** = `todo` with every `depends_on` done · **blocked** = the rest,
     with the blocking reference named;
   - **awaiting acceptance** = story `in-progress` with all its tasks `done`
     and no PASS sign-off (tasks found via their `story:` links);
   - open changes (`draft`, or `approved` but not yet `applied`).
5. **Output:**
   - Roadmap as text: last thing done → in flight → ready next. Ready next
     lists every available action type — approvals, acceptances, ready tasks,
     plannable PRDs, pending decisions, developable stubs — never the PRD
     pipeline alone: the owner sees the whole option space even though the
     recommendation below stays single.
   - Mermaid graph: one node per PRD labeled with its reference, slug, and
     story rollup (`2/5 stories done`); edges from `depends_on`; mark each
     node's status.
   - Stories awaiting acceptance: the AC checklist, and the exact edit that
     records the verdict — on PASS append `<date> — <name> — PASS: <note>` to
     the story's Acceptance log and set `status: done`; on FAIL append the FAIL
     line and run `/spectacular:plan story-NNN`.
   - Warnings from step 3.

## Next step

Exactly **one** recommendation, with its justification, naming only commands
that exist (init, prd, design, decide, plan, implement, next, retro,
upgrade). Candidates come from every class step 4 derives — approve a draft,
accept a story, apply a change, implement a ready task, plan a plannable
PRD, work a pending decision, develop a ready stub — never from the PRD
pipeline alone. Rank candidate
actions by: unblocks the most downstream work → highest reversal cost (settle
hard-to-undo choices while they are still cheap) → smallest size. Lingering
drafts and stories awaiting acceptance outrank new work: an approval that takes
minutes is usually the cheapest unblock available. A pending decision that
gates planning (say, an empty registry — no task can become ready) outranks
developing another stub: more approved spec is worth little while everything
downstream waits on one choice.
