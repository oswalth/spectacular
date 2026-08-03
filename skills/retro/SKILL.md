---
name: retro
description: With an argument, append one process observation to the workspace log in seconds, zero questions. Without one, review accumulated observations, root-cause them, and propose fixes.
argument-hint: ["observation"]
---

# /spectacular:retro — capture and review process friction

Two modes. The cheap one must stay cheap — friction that costs more than a
sentence to record never gets recorded.

## Append mode (an observation was passed)

Append one line to `.spectacular/observations.md` (create the file with just the
heading `# Observations` on first use):

```markdown
- <YYYY-MM-DD>: <the observation, verbatim>
```

Ask **zero** questions. Confirm in one line and stop.

## Review mode (no argument)

1. Read `.spectacular/observations.md`. Empty or missing → say so and stop;
   nothing to review is a fine state.
2. Group the observations and root-cause each group against evidence in the
   artifacts (which skill, which artifact, what actually happened) — not against
   memory.
3. Split the causes:
   - **Workspace-level** (this project's process, conventions, artifacts):
     propose concrete fixes, gate them with the owner, apply the approved ones,
     and mark the covered observations `(addressed <date>)`.
   - **Plugin-level** (spectacular itself should change): write a handoff brief
     under `## Plugin handoff briefs` in the observations file — what hurt,
     evidence, proposed change. Briefs accumulate; the plugin-evolution loop is
     deliberately not built until accumulated briefs demand it. Do not attempt
     to modify the plugin from here.

## Next step

- Append mode: recommend returning to whatever was interrupted — the
  observation is saved; that is the entire point of the cheap mode.
- Review mode: recommend `/spectacular:next` to re-derive state, since applied
  fixes may have changed what is ready.
