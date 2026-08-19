# spectacular — plugin repo

This repository is the source of the **spectacular** Claude Code plugin (skills,
agents, templates, docs) and its own marketplace. Anyone opening Claude Code
here — owner or teammate, any machine — works under the rules below; nothing
about how this repo is maintained lives in session memory or local config.

## Two zones

- **Shipped plugin content** — `skills/`, `agents/`, `templates/`, `scripts/`,
  `docs/`, `README.md`, `CHANGELOG.md`, `.claude-plugin/`. Impersonal: examples
  use the placeholder vocabulary (product **acme**, workspace **acme-product**,
  repos **acme-api / acme-web / acme-mobile / acme-infra**, people **alex**,
  **sam**; the constellation set only in naming-conventions docs). Never a real
  client, project, person or machine path. `design/denylist.txt` lists the
  tokens that must never appear in shipped files.
- **Design zone** — `design/`. The plugin's own memory: `design/STATE.md`
  (requirements, principles, decisions **D-NNN**, deferred items with written
  triggers, open questions, session log) and `design/spec.md` (the build
  spec). It is committed and shared with the team as the decision log; it
  does not ship publicly.

## Before changing anything

Read `design/STATE.md` **Decisions**, **Deferred, with triggers** and **Open
questions**, then `design/spec.md` for the parts you touch. A change that
contradicts a D-number is made by *revising* that decision in STATE.md and
saying so — never silently. Deferred items stay deferred until their written
trigger fires. The Session log is evidence for root-causing; read the entries
you need, not the whole file.

## Ways of working

The numbering is referenced from `docs/release.md` and the repo-boundary hook —
keep it stable.

1. Always ask for clarification; never assume.
2. Do not overcomplicate.
3. Follow the Karpathy guidelines — full text in `design/karpathy-guidelines.md`
   (think before coding · simplicity first · surgical changes · goal-driven
   execution).
4. Plan for context rot: `design/STATE.md` is the mechanism — update it before
   a session ends (settled items into Decisions, refresh Open questions, append
   to the Session log).
5. This directory is the plugin repo; workspaces and code repos are elsewhere.
6. **Commit protocol.** Claude never commits or pushes on its own. Flow: make
   changes → propose a commit message → the owner reviews the diff and approves
   or challenges → commit (and push) only on the owner's explicit ask.
7. **Repo boundary.** Sessions here never MODIFY project/workspace/code repos
   that use the plugin — suggestion-only (name the plugin skill to run there,
   or give precise manual steps). Reading them for analysis stays allowed.
   Enforced structurally by the PreToolUse hook in `.claude/settings.json` +
   `.claude/hooks/repo-boundary.py` (needs `python3`; blocks Write/Edit/
   NotebookEdit outside this repo and mutating Bash that references outside
   paths).
8. **Change strategy (D-37).** Conventional Commits; tags mark releases only —
   a commit's version is derived via `git describe`, never stamped. Releases
   follow `docs/release.md`: one atomic release commit keeps `plugin.json`,
   `CHANGELOG.md`, `docs/upgrades.md` and the tag in sync. No AI-attribution
   trailers (`Co-Authored-By: Claude …`, `Generated with …`) in any commit.
9. **Gate protocol + self-sufficiency (D-41).** At any approval gate only an
   explicit approve-like answer approves; a vague go-ahead ("ok", "keep
   working") re-asks, and every gate ends with an explicit question. Process
   rules live in repo artifacts, so the plugin, every workspace and every code
   repo behave identically on any machine or account.

## Evolving the plugin (the retro loop)

Friction is captured where it happens: `/spectacular:retro` in a workspace
appends observations; its review mode root-causes them and writes
**plugin handoff briefs** (what hurt, evidence, proposed change) into that
workspace's `.spectacular/observations.md`. Briefs reach this repo in-chat or
as issues on the GitHub repo. A maintainer then runs `/spectacular:retro` in a
checkout of this repo, which is review mode for the plugin itself:

1. Root-cause each brief against the skills, templates and docs — not memory.
   Confirm, refine or overturn it; say explicitly when a point stands.
2. Propose the change set under an explicit gate (rule 9). Apply only the
   approved items.
3. Record the outcome in `design/STATE.md` (a D-number for decisions, the
   session-log entry) and fold mechanics into `design/spec.md`.
4. Regenerate docs (`python3 scripts/generate-docs.py`), run the manual checks
   below, propose the commit (rule 6), then release per `docs/release.md`.

### Adding a skill

`skills/<name>/SKILL.md` with front matter `name` (= directory), `description`,
optional `argument-hint`; body ends with a `## Next step` section that
recommends only commands that exist. Then: add `<name>` to `LIFECYCLE` in
`scripts/generate-docs.py` (the generator fails loudly on any mismatch
between that list and `skills/` on disk), add a row to `docs/models.md`, a row
to the README command table, regenerate `docs/commands.md`, and bump the next
release (minor). Artifact shapes belong in `templates/` — skills reference them
via `${CLAUDE_PLUGIN_ROOT}/templates/…`, never inline them.

### Adding an agent

`agents/<name>.md` with front matter `name`, `description`, `tools`. Agents are
silent workers dispatched by skills (D-8); a read-only agent declares only
`Read, Glob, Grep`. Mention it in the README and in the skills that dispatch it.

### Adding or changing a template

Edit `templates/<artifact>.md`; every skill that writes that artifact reads the
template, so nothing else duplicates the shape. Template changes are
workspace-facing: the release is at least minor and `docs/upgrades.md` gets a
section telling existing workspaces what to realign (`/spectacular:upgrade`
reads it).

## Manual checks (lint and CI are deferred — see STATE.md Deferred)

Before proposing a commit that touches shipped content:

- `python3 scripts/generate-docs.py` → `git diff docs/commands.md` is empty;
  `docs/models.md` has exactly one row per skill.
- Every `/spectacular:<name>` mentioned in shipped files exists under
  `skills/`; every `SKILL.md` ends with `## Next step`.
- `grep -rIil` each token of `design/denylist.txt` over shipped files → no hits.
- `README.md` references every file under `docs/`.
- `claude plugin validate .` passes.
