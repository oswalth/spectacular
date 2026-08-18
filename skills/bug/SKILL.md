---
name: bug
description: File a bug report as a workspace artifact — map what the reporter says onto the bug Definition of Ready, elicit the missing evidence in at most two short rounds, then write bug-NNN (open) for triage by plan.
argument-hint: ["<what happened>"]
---

# /spectacular:bug — file a bug report

Cheap intake for anyone who sees something break — QA, product, a developer.
Zero investigation here: this skill records evidence while it is fresh; the
investigation belongs to `/spectacular:plan bug-NNN`. Runs in the workspace,
or in a registered code repo (found via `.spectacular/contract.md`).

## Steps

1. **Read the argument** — a sentence or a long paste — and map it onto the
   **bug Definition of Ready** (workspace CLAUDE.md): summary · where (page,
   screen or URL, component, the flow) · steps to reproduce with the input
   used · actual vs expected · environment (platform, build or environment,
   account/role) · reproducibility · evidence · regression (worked before?)
   · related story/AC if known. No argument → treat every field as missing.
2. **Elicit the gaps, bounded.** At most **two** propose-then-ask rounds
   (workspace CLAUDE.md, gate protocol style: frame first). Each round
   states what you already inferred and asks only for what is missing —
   "I read this as the Submit on the checkout form at /cart, always
   reproducible. Missing: the URL you were on, what you expected to happen,
   a screenshot or console error if you have one." Never ask what the
   report already answers; never run a third round. Evidence files the
   reporter offers (screenshots, log extracts) go under
   `delivery/bugs/NNN-<slug>/`; text evidence is pasted into the body.
3. **Structure and file.** Write `delivery/bugs/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/bug.md` — next free number, `status:
   open`, `routed_to: []`, every DoR field filled or explicitly marked
   *unknown*. Filing is never blocked by gaps: an incomplete report is still
   a report, and its unknowns become triage's first questions. Say in one
   line which fields stayed unknown.
4. **Propose a commit** — `docs(bug-NNN): report — <slug>` — committed only
   on explicit approval (workspace commit protocol, CLAUDE.md).

## Next step

Recommend `/spectacular:plan bug-NNN` to triage and route the report — it
finds the story, task, or repo the cause lives in and plans the fix; the bug
itself is never implemented directly. If the reporter already knows the
story whose acceptance criterion broke, `/spectacular:plan story-NNN
"<defect>"` skips the search.
