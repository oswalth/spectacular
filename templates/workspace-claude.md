# <product-name> — workspace

This is a **spectacular** workspace: the documentation home of a multi-repo
product. Code lives in sibling repositories; `.spectacular/registry.md` lists
them, and each code repo points back here via its `.spectacular/contract.md`.

## How this workspace works

- **State is derived, never stored.** Where things stand is always computed from
  artifact files and their front matter. There is no status file; if any summary
  disagrees with the files, the files win.
- **Files are the interface.** Manually editing any artifact — including
  front-matter statuses — is always legitimate.
- **Orientation:** run `/spectacular:next` to derive current state and get one
  recommended action.
- **Self-sufficient by design.** Everything a session needs lives in this
  repo's artifacts (and the registered repos' `CLAUDE.md` and contracts).
  Process rules are never carried in one person's session memory or
  machine-local config — a rule worth keeping becomes an artifact or
  template change, so any teammate on any machine gets identical behavior.
- **Fresh before derived.** A workspace shared through a remote is pulled
  before state is derived from it — `/spectacular:next` fetches and says
  when this checkout is behind. Code repos are read at their remote default
  branch, never at whatever a local checkout happens to hold (Ways of
  working §5).

## Language

Artifacts are written in **<artifact-language>** — chosen at init, for the
whole team. Everything that lands in a repo follows it regardless of the
language a conversation happens in: artifacts and their front matter,
commit messages, code comments, READMEs, Learnings, retro observations. The
conversation itself follows the user — the `language` setting of their
Claude Code (`/config` → Language, or `"language"` in
`~/.claude/settings.json`) or, absent one, the language they write in. Gate
questions, explanations and summaries come in that language; a translation
of an artifact is given in chat on request and never written to a file.

## Gate protocol

Every approval gate — artifact approvals, commit proposals, migration sets,
landing gates — follows the same rules:

- A gate ends with an **explicit question** naming the decision needed. The
  owner must always be able to tell that the session is waiting, and on what.
- Only an **explicit approve-like answer** approves ("approve", "yes, apply
  1 and 3"). A vague go-ahead ("ok", "go on", "keep working") approves
  nothing — re-present the open items and ask again. Silence is never
  consent.
- An approval **names what it covers**; partial approval is normal, and
  unapproved items stay proposals.

## Commit protocol

Nothing is committed unprompted — by a skill or by any session working here.
Each **unit of work** ends with a proposed commit message; the owner reviews
the diff and approves, and only then does the commit happen. In a workspace
with a remote the proposal carries its **push**: "commit and push" is one
question, and one explicit approval covers both. Declining the push is the
owner's call, but an unpushed commit is state the team cannot see (Fresh
before derived) — the exception, never the default. A workspace without a
remote pushes nothing.

One commit per unit of work: the scaffold; the approved brief; the PRD-map
stubs; each developed PRD — approved, or left as a draft for team review —
plus any change proposal it opened; each revision of a draft from review
comments; each ADR with its overview update; each plan batch; each task
claim (`in-progress`); each bug report and each triage; each standalone
task; each retro review's applied fixes.
`/spectacular:implement` is no exception (D-39): once verification passes it
presents the diff, the verification evidence, and both proposed commits —
the code-repo commit (one task = exactly one squashed mainline commit) and
the workspace close-out commit (statuses, Learnings) — and lands them, the
workspace push included, only on one explicit greenlight. The claim that
starts a task (`in-progress`) is its own proposed commit and push, asked at
the start — the team must see a task is taken while it runs.

Messages follow **Conventional Commits 1.0.0** (D-37). In a workspace almost
everything is `docs` (artifact content) or `chore` (scaffolding, statuses);
the artifact id is the scope, and cross-references ride git-trailer footers,
never the subject:

```
docs(prd-004): approve — payments
docs(prd-005): draft for review — reporting
chore(scaffold): init <product> workspace
chore(task-012): in-progress
docs(task-012): done — status + learnings

Refs: story-003
```

Code-repo commits use the type matching the change (`feat`, `fix`, …); a
commit that realizes a task carries the mandatory `Task: task-NNN` footer,
a housekeeping commit (see Work outside a PRD breakdown) carries none.
Workspaces carry **no versions and no
tags** — state is artifact statuses plus the plugin pin; tags mark releases,
and a workspace releases nothing. Code repos version and release per their
contract (`versioning`, `release_flow`). Commit messages never carry
AI-attribution trailers — no `Co-Authored-By: Claude …`, no
`Generated with …` — in any repo: workspace, code, or the plugin itself
(D-37).

## Layout

| Path | Contents |
|------|----------|
| `product/brief.md` | the product brief |
| `product/prds/` | one PRD per capability, `NNN-<slug>.md` |
| `product/designs/` | design specs (`NNN-<slug>.md`); `system/` holds imported design code + distilled `tokens.json` / `design-language.md` (git-canonical, with `provenance.md`) |
| `architecture/overview.md` | living architecture overview |
| `architecture/decisions/` | ADRs, `NNN-<slug>.md` |
| `delivery/stories/` | user-visible slices of a PRD |
| `delivery/tasks/` | one repo's share of a story — or a standalone task (no `story:`) for maintenance work |
| `delivery/bugs/` | bug reports, `NNN-<slug>.md` (evidence files in `NNN-<slug>/`) |
| `changes/` | amendment proposals to approved artifacts |
| `.spectacular/` | profile, code-repo registry, retro observations |
| `conventions.md` | naming conventions (optional) |

References are `<type>-<NNN>` and resolve by filename: `prd-001` →
`product/prds/001-*.md`, `design-002`, `adr-003`, `story-004`, `task-012`,
`bug-005` likewise. Numbering is per type, zero-padded to 3. The filename is
the identity.

## Work outside a PRD breakdown

Capability delivery flows PRD → story → task through `/spectacular:plan`.
Three kinds of work do not start from a PRD:

- **Something broke.** `/spectacular:bug "<what happened>"` files the report
  with its evidence; `/spectacular:plan bug-NNN` triages it — finds the
  story, task, or repo the cause lives in — and routes it to fix work. When
  the story is already known, `/spectacular:plan story-NNN "<defect>"` goes
  straight there: a defect in an accepted story is a late acceptance FAIL —
  the story returns to `in-progress`, gets fix tasks, and is re-tested to a
  fresh PASS. Bugs are never implemented directly; the fix is always a task.
- **Maintenance with no user-visible change** — an IaC change adding a team
  member, a dependency or runtime bump, a secret rotation, a data fix:
  `/spectacular:plan "<task>"` writes a **standalone task**, a task with no
  `story:`. New or changed behavior is never a standalone task; it belongs
  to a PRD (a change proposal when the PRD is approved) and then a story.
- **Housekeeping in a code repo** — docs, comments, formatting, `README.md`,
  `CLAUDE.md`, the contract and its Toolchain notes — needs no task: it is
  edited under the commit protocol, with the Conventional Commits type
  matching the change (`docs`, `style`, `chore`) and no `Task:` footer,
  landed per that repo's `merge_flow`. Anything that changes behavior,
  architecture or dependencies — a refactor included — is a task:
  standalone when it has no story.

## Reviews

Two things here are reviewed by people other than their author. Names are
written into the lines people add — no reviewer, owner or assignee is stored
anywhere else.

- **A draft PRD.** Its author leaves it at `status: draft`, committed and
  pushed; the team reads it on the default branch. A reviewer adds one line
  per comment to the PRD's `## Review` section —
  `- <date> — <name> — <comment> (FR-003 / AC-2 / Scope …)` — and commits it
  (any editor; the GitHub web editor counts). The author then runs
  `/spectacular:prd prd-NNN`: it proposes a resolution per open line — applied
  with the delta, or declined with the reason — and marks each line in place
  (` → <date> applied` / ` → <date> declined: <why>`). When every line is
  resolved and the team agrees, the author approves: `status: approved`,
  the Review section dropped (git keeps it), a declined point worth keeping
  moved to Clarifications. A PRD with open review lines is *in review*, not
  lingering — `/spectacular:next` tells the two apart. The author is whoever
  carries the PRD; nothing records it.
- **A story whose tasks are all done** is *awaiting acceptance* — derived,
  never stored: `/spectacular:next` lists it with its AC checklist, and the
  close-out that landed its last task wrote
  `<date> — <name> — READY: all tasks done, awaiting acceptance` into the
  story's Acceptance log (an event line, not a status). A reviewer — QA, PO,
  whoever the team names — tests **every** AC against the real thing and
  records the verdict in the same log: on PASS `<date> — <name> — PASS:
  <note>` and `status: done`; on FAIL `<date> — <name> — FAIL: <what failed>`,
  then `/spectacular:plan story-NNN` reopens tasks and/or adds fix tasks and
  the story is re-tested to a fresh PASS, never assumed fixed. A task is not
  accepted on its own — its landing gate and Verification are its done; the
  story is what gets accepted.

## Definitions of Ready and Done

Uniform for every item — defined once here, enforced by the skills
(`/spectacular:plan` only writes items that are ready; `/spectacular:implement`
checks ready before starting and walks done before closing). The item-specific
part of "done" lives in each story's Acceptance criteria and each task's
Verification; these definitions are the invariant rest.

**Story ready:** its PRD is approved; ACs are Given/When/Then test scripts
mapped from the PRD's ACs; every AC is covered by at least one task; a story
covering designed UI references the approved design spec sections it
implements (when its PRD has a design spec); its `depends_on` stories are
done.

**Story done:** all its tasks are done; a human tested every AC and logged
PASS in the Acceptance log; the human sign-off (never the plugin) flips
`status: done`.

**Task ready:** its story is ready (a standalone task has none); its `repo:`
is in the registry with a contract; Verification (preconditions, steps,
expected) is written; its `depends_on` tasks are done.

**Task done:** Verification passes; exactly one squashed mainline commit
(Conventional Commits subject, `Task: task-NNN` footer); Learnings appended;
`status: done`.

**Bug ready (for triage):** a one-line summary; where (page, screen or URL,
component, the flow); steps to reproduce with the input used — or the
observation when it cannot be reproduced yet; actual vs expected;
environment (platform, build or environment, account/role); reproducibility;
evidence attached or explicitly none. `/spectacular:bug` elicits these in at
most two rounds; a report may be filed with gaps — they are triage's first
questions.

**Bug done:** `status: closed` with a Resolution — fixed (every `routed_to`
target done: the fix task landed, or the story re-accepted with a PASS) or a
recorded non-fix resolution (not a bug, spec gap → change proposal,
duplicate, could not reproduce, won't fix).

## Ways of working (Karpathy guidelines)

### 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly — if uncertain, ask rather than guess.
- Present multiple interpretations — don't pick silently when ambiguity exists.
- Push back when warranted — if a simpler approach exists, say so.
- Stop when confused — name what's unclear and ask for clarification.

### 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

The test: would a senior engineer say this is overcomplicated? If yes, simplify.

### 3. Surgical changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused; leave
  pre-existing dead code alone unless asked.

The test: every changed line should trace directly to the request.

### 4. Goal-driven execution

Define success criteria. Loop until verified.

| Instead of… | Transform to… |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

For multi-step tasks, state a brief plan: each step paired with its verification.

### 5. Just-in-time reconnaissance

Plan first, write early, let the gates discover. Applies to every code repo.

- Once a task's context is compiled and before any further read, state the
  numbered plan (§4) and narrate progress against it. Reconnaissance no
  plan step needs is not done.
- No upfront survey. Read code at the step that changes or calls it — that
  file and its tests, never the whole tree. Look a tool, package or library
  up when the step that uses it starts: one batched lookup per question
  (`--help`, `--version`, one registry query).
- A failing gate — type check, lint, tests, build — is the discovery
  mechanism: run the repo's commands and let them say what is wrong;
  investigate that failure, then continue.
- Rehearse outside the repo only when an in-repo failure would be expensive
  to undo: remote or state-changing operations, irreversible writes, long
  jobs. A task branch plus git makes everything else free to retry in place.
- Run CLIs non-interactively (yes/defaults flags, stdin from `/dev/null`)
  under a timeout.
- Knowledge bought this way is repo-level: it goes to the repo contract's
  Toolchain notes at the landing gate, so the next task never pays for it
  again.
- Read a code repo **fresh** — at its remote default branch, not at whatever
  the local checkout holds: `git fetch` first (quietly, under a timeout). A
  checkout on the default branch, clean and not behind, is read in place;
  anything else is read through a detached temporary worktree of
  `origin/<default>` outside the repo — a developer's half-done branch is
  never taken for the repo's state. A repo missing locally is shallow-cloned
  from the registry's `remote` into scratch (`/spectacular:onboard` clones
  it properly); fetch failing → read the local checkout and say it may be
  stale; a `local-rebase` repo whose mainline is ahead of the remote is
  freshest locally — say so. Task branches start from the fetched
  `origin/<default>`.
