# <repo-name> — code repo of <product-name>

<one-liner>. This is a **spectacular** code repo, area `<role>` of a
multi-repo product whose documentation workspace is `../<workspace-dir>`
(its `.spectacular/registry.md` lists every repo; this repo points back
via `.spectacular/contract.md`).

Two files are imported into every session here — read them as part of
this file:

@.spectacular/contract.md
@../<workspace-dir>/CLAUDE.md

The second import is external to this repo — Claude Code asks once per
machine to allow it. If it did not load, read `../<workspace-dir>/CLAUDE.md`
before doing anything else: its gate protocol, commit protocol, language
rule and ways of working bind here too.

## What lives where

- **Truth lives in the workspace, never here.** The brief, PRDs, design
  specs, the architecture overview and the ADRs are in
  `../<workspace-dir>/` (`product/`, `architecture/`). Do not copy them into
  this repo; refer to them by reference (`prd-004`, `adr-003`).
- **Why was it built this way?** `../<workspace-dir>/architecture/overview.md`
  (short — read whole), then the ADRs touching this repo: their Decision
  Outcome, Consequences and Confirmation sections only — the options
  analysis justifies a choice, it does not bind the code.
- **What is this repo and how do I run it?** The contract above (stack,
  commands, conventions, toolchain notes) and `README.md` (prerequisites,
  getting started).
- **Work on this repo** — stories, tasks, bugs — lives in
  `../<workspace-dir>/delivery/`. `/spectacular:next` run here (or
  `/spectacular:next <repo-name>` in the workspace) shows what is ready for
  this repo and nothing else.

## Working here

- **Task work:** `/spectacular:implement [task-NNN]` — one task, one branch,
  one squashed mainline commit behind the landing gate. Anything that
  changes behavior, architecture or dependencies — a refactor included —
  is a task; maintenance work with no story is a standalone task, written
  by `/spectacular:plan "<task>"` in the workspace.
- **Housekeeping without a task** — docs, comments, formatting, `README.md`,
  this file, the contract and its Toolchain notes: edit under the commit
  protocol (proposed commit, explicit approval), Conventional Commits type
  matching the change (`docs`, `style`, `chore`), no `Task:` footer, landed
  per the contract's `merge_flow`. Nothing that changes behavior rides this
  path.
- **A problem in the architecture or the spec** found while working here is
  a workspace matter: a `changes/` proposal there (implement writes one), or
  `/spectacular:decide` — never an edit to workspace truth from here, never
  a silent workaround.
- **A gap in this repo's contract** — an undecided convention, a toolchain
  fact — is amended in `.spectacular/contract.md` under a gate; it is
  repo-local. Only an amendment contradicting an approved ADR needs a
  superseding ADR first.
- **This file and `README.md` are plugin-owned scaffolding** —
  `/spectacular:upgrade`, run in the workspace, keeps them aligned with the
  plugin's templates.
