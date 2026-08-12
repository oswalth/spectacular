---
name: retro
description: Capture process friction cheaply or review it — one-line append for a single observation, itemized capture for a multi-point argument, root-cause review with proposed fixes when called bare.
argument-hint: [observation]
---

# /spectacular:retro — capture and review process friction

Two modes, chosen by the **content** of the argument, not merely its presence.
The cheap path must stay cheap — friction that costs more than a sentence to
record never gets recorded.

## Append mode (argument is one short observation)

Append one line to `.spectacular/observations.md` (create the file with just
the heading `# Observations` on first use):

```markdown
- <YYYY-MM-DD>: <the observation, verbatim>
```

Ask **zero** questions. Confirm in one line and stop. No commit ceremony —
the observation rides along with the next unit-of-work commit.

## Multi-item argument

An argument carrying several observations, or a whole review request, is not
one line. Split it into individual dated entries, show the list for one quick
confirmation, append them all, then offer to run review mode on the spot.

## Review mode (no argument, or continuing from a multi-item capture)

1. Read `.spectacular/observations.md`. Empty or missing → offer interactive
   capture: ask what has hurt lately and append each answer as an observation
   line; if the owner has nothing, say that no recorded friction is a fine
   state and stop.
2. Group the observations and root-cause each group against evidence in the
   artifacts (which skill, which artifact, what actually happened) — not
   against memory. Observations are symptoms, not verdicts: root-causing may
   confirm, refine, or overturn them. Challenge an observation when the
   evidence disagrees, ask when it underdetermines the fix, propose the better
   option when you see one — and say explicitly when a point stands exactly
   as stated.
3. Split the causes:
   - **Workspace-level** (this project's process, conventions, artifacts):
     propose concrete fixes, gate them with the owner — explicit approval
     naming which fixes; a vague go-ahead re-asks (gate protocol,
     CLAUDE.md) — apply the approved ones,
     and mark the covered observations `(addressed <date>)`.
   - **Plugin-level** (spectacular itself should change): write a handoff brief
     under `## Plugin handoff briefs` in the observations file — what hurt,
     evidence, proposed change. Briefs accumulate until a session in the
     plugin repo consumes them. Do not modify the plugin from a workspace.
4. **Propose a commit** for the applied fixes and the updated observations
   file; commit only on the owner's explicit approval (workspace commit
   protocol, CLAUDE.md).

## Running inside the spectacular plugin repo

Run from the plugin repo itself rather than a workspace, review mode IS the
plugin-evolution loop: observations arrive in-chat or as handoff briefs
carried over from a workspace, root-causing runs against the skills and
templates, and the fixes are plugin changes — made under the plugin repo's
own ways of working. Plugin changes ship via the release procedure in
`docs/release.md`: derive the bump from CC types, update CHANGELOG.md (and
docs/upgrades.md iff workspace-facing), one atomic release commit, tag.

## Next step

- Append mode: recommend returning to whatever was interrupted — the
  observation is saved; that is the entire point of the cheap mode.
- Review mode: recommend `/spectacular:next` to re-derive state, since applied
  fixes may have changed what is ready.
