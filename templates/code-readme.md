# <repo-name>

<one-liner> — the `<role>` repo of **<product-name>**. Product documentation
(brief, PRDs, architecture decisions, stories and tasks) lives in the
workspace repo, checked out as a sibling directory: `../<workspace-dir>`
<!-- plan: add the workspace remote URL in parentheses when it has one -->.

## Prerequisites

Tools assumed installed before any command below runs — one line each:
tool, version constraint, why. Whoever introduces a requirement adds it
here (a task that brings a new tool updates this list at its landing gate).

- <tool> <version constraint> — <why; e.g. runs the service locally>
- …

## Getting started

Clone this repo as a sibling of the workspace (`../<workspace-dir>`). The
canonical commands live in `.spectacular/contract.md`; mirrored here:

- build: …
- test: …
- run: …

## Working here

- `CLAUDE.md` routes Claude Code sessions: where truth lives, which rules
  bind here, task work vs housekeeping.
- Task work lands through `/spectacular:implement` — one task, one squashed
  mainline commit.
- New to the product, or on a new machine? `/spectacular:onboard` in the
  workspace checkout clones the repos you can reach and checks these
  prerequisites.
