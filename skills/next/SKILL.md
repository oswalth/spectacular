---
name: next
description: Derive project state from artifact front matter — pending approvals, ready vs blocked work, stories awaiting acceptance, open bugs, open changes — render the roadmap as text and a Mermaid graph, and make exactly one justified recommendation; scoped to one repo or one area (registry role) on request, so a developer sees only their work.
argument-hint: [repo-name | role]
---

# /spectacular:next — where things stand, what to do

Read-only. State is derived fresh from files on every run — nothing is cached,
nothing is stored.

## Steps

1. **Locate and scope.** `.spectacular/profile.md` here → this is the
   workspace. `.spectacular/contract.md` here → code repo: resolve the
   workspace via `workspace:`. Neither → refuse: run this in a workspace or
   a registered code repo; for a brand-new product, `/spectacular:init` in an
   empty directory. Then fix the **scope**: the argument — a registry `name`
   (one repo) or a registry `role` (every repo of that area); no argument in
   a code repo → that repo; no argument in the workspace → the whole
   project. An argument matching neither → say so and list the names and
   roles the registry knows. If the workspace has a remote, `git fetch`
   quietly (under a timeout) and say at the top when this checkout is
   behind `origin/<default>` — state derived from a stale checkout is
   stale (workspace CLAUDE.md, Fresh before derived).
2. **Read front matter only** — brief, PRDs, design specs, ADRs, stories,
   tasks, bugs, change proposals, plus the registry. Read it in **bulk**, not
   file by file: one scan per directory (`grep`/`head` across the glob) yields
   every status and link at once and stays affordable as `delivery/` grows into
   the hundreds — a shipping product accumulates far more terminal items than
   live ones. Open an artifact body
   only where derivation needs it: the AC checklist of a story awaiting
   acceptance, and the `## Review` section of a PRD draft (an open line is
   one without a ` → ` resolution).
3. **Validate while reading** (warn at the top of the output; never halt):
   references that resolve to no file (including a bug's `routed_to`);
   statuses outside their vocabulary (brief/design: draft·approved; PRD/ADR:
   stub·draft·approved; story/task: todo·in-progress·done·dropped; bug:
   open·closed; change: draft·approved·applied); and any `todo` or
   `in-progress` item whose `depends_on` names a `dropped` item — it can never
   become ready, so the owner either drops it too or edits its `depends_on`.
   This is the only workspace validation in v0.1.
4. **Derive** (never trust a stored summary):
   - drafts awaiting approval (brief, PRDs, designs, ADRs, changes) — a PRD
     draft with open Review lines is **in review** (count them), not
     lingering: its action is revise, by its author (`/spectacular:prd
     prd-NNN`), never approve;
   - **plannable** = PRD `approved` with no stories naming it in `prd:` — an
     approved spec whose breakdown nobody has run (`/spectacular:plan`);
   - **pending decisions** = ADRs still `stub` — the decision map waiting to
     be worked (`/spectacular:decide`);
   - **ready** = `todo` with every `depends_on` done · **blocked** = the rest,
     with the blocking reference named — standalone tasks (no `story:`)
     derive the same way and are labeled as such. A **`dropped`** item is
     neither: it counts for nothing in this step — not ready, not blocked,
     not covering an AC, not holding a story back (workspace CLAUDE.md,
     Dropping work that is no longer wanted);
   - **awaiting acceptance** = story `in-progress` with all its tasks `done`,
     a `dropped` task holding nothing back (tasks found via their `story:`
     links; a PASS sign-off would have flipped it to `done`) — a story
     reopened by a FAIL after acceptance re-enters this state the same way;
     the READY line implement writes into the Acceptance log is a record of
     when, never the source;
   - **untriaged bugs** = bug `open` with empty `routed_to` (needs
     `/spectacular:plan bug-NNN`) · **routed bugs** = `open` with targets,
     their fix state read off the targets (task todo/in-progress/done;
     story awaiting acceptance) · **fixed-but-open** = every target `done`
     yet the bug still `open` — print the closing edit;
   - open changes (`draft`, or `approved` but not yet `applied`).

   **Scoped run** — same derivation, narrowed to the scope's repos: tasks
   whose `repo:` is in scope (ready / blocked / in-progress, standalone ones
   labeled), each blocker named even when it sits in another repo; stories
   with at least one such task, awaiting acceptance included (acceptance is
   per story); bugs routed to those tasks or stories. Everything
   workspace-level — drafts, plannable PRDs, pending decisions, developable
   stubs, open changes, untriaged bugs — stays out of the view and collapses
   to one footer line with counts (`workspace-level: 2 drafts, 1 pending
   decision — bare /spectacular:next`), so nothing is hidden and nobody is
   bothered.
5. **Output:**
   - Roadmap as text: last thing done → in flight → ready next. Ready next
     lists every available action type — approvals, drafts in review (with
     their open-comment counts), acceptances, untriaged bugs, ready tasks
     (standalone ones marked), plannable PRDs, pending decisions, developable
     stubs — never the PRD pipeline alone: the owner sees the whole option
     space even though the recommendation below stays single.
     Completeness is over action *types*, never instances: when one type has
     more than ~10 instances, show the ten the ranking below puts first and
     give the rest as a count (`+31 more ready tasks`). Say that you
     truncated, and never truncate a type to zero — a type reduced to a
     count would vanish from the option space.
   - Mermaid graph: one node per PRD labeled with its reference, slug, and
     story rollup (`2/5 stories done`); edges from `depends_on`; mark each
     node's status. Bugs and standalone tasks are not in the graph — they
     are listed below it. A scoped run draws only the PRDs whose stories
     have tasks in scope.
   - Open bugs: untriaged ones, and routed ones with their fix state; for
     fixed-but-open bugs the exact closing edit — append `fixed via
     <target>` to Resolution and set `status: closed`.
   - Stories awaiting acceptance: the AC checklist, and the exact edit that
     records the verdict — on PASS append `<date> — <name> — PASS: <note>` to
     the story's Acceptance log and set `status: done` (closing any bug
     routed to the story the same way); on FAIL append the FAIL line and run
     `/spectacular:plan story-NNN`.
   - Warnings from step 3.

## Next step

Exactly **one** recommendation, with its justification, naming only commands
that exist (init, onboard, prd, design, decide, plan, implement, bug, next,
retro, upgrade). In a scoped run the recommendation is scope-local — the
best ready action on the scope's repos, or, when nothing is ready there,
the blocker by name and the command (or the person's area) that clears
it. Candidates come from every class step 4 derives — approve a draft, revise
a draft in review (its author's move — say so), accept a story, close a
fixed bug, triage an untriaged bug, apply a change,
implement a ready task, plan a plannable PRD, work a pending decision,
develop a ready stub — never from the PRD pipeline alone. Rank candidate
actions by: unblocks the most downstream work → highest reversal cost (settle
hard-to-undo choices while they are still cheap) → smallest size. Lingering
drafts, stories awaiting acceptance, and untriaged bugs outrank new work: an
approval that takes minutes is usually the cheapest unblock available, and a
triage is cheap while its outcome — a defect in delivered value — is not.
A routed bug's fix task is a ready task like any other; the owner may pull
it forward. A pending decision that
gates planning (say, an empty registry — no task can become ready) outranks
developing another stub: more approved spec is worth little while everything
downstream waits on one choice.
