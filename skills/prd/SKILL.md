---
name: prd
description: Propose the PRD map on first run, or develop one PRD from stub to approved — bounded clarify pass, checkable acceptance criteria, explicit out-of-scope. Requires an approved product brief.
argument-hint: [prd-NNN]
---

# /spectacular:prd — product requirements

A PRD is the durable spec of one capability. It is never "done" — once approved it
can only be amended through `changes/`. The set of PRDs and their `depends_on`
edges IS the product roadmap; no other roadmap artifact exists.

## Precondition

`product/brief.md` exists with `status: approved`. Otherwise refuse: point at
`/spectacular:init` (no brief) or at approving the brief (still draft).

## Mode A — no PRDs yet: propose the map

1. Read the brief. Derive the product's capabilities — one PRD each. Aim for the
   smallest set that covers the goals; challenge any capability that serves no
   stated goal.
2. Present the map for approval: per capability a proposed reference
   (`prd-001`, …), a one-line scope, and `depends_on` edges (must be acyclic).
   Number so that low numbers are upstream where possible.
3. **Gate.** On approval, write one **stub** PRD per capability — the map is
   persisted only as stub PRDs, nowhere else. File:
   `product/prds/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/prd.md`, reduced to the stub form:
   `status: stub`, `depends_on` filled, the title, and a one-line Scope —
   drop the remaining sections until the PRD is developed.

## Mode B — stubs exist: develop one PRD

1. Pick the target: the `prd-NNN` argument if given; otherwise suggest the stub
   whose `depends_on` are all approved and which unblocks the most other stubs.
2. **Clarify pass.** Ask at most 5 structured questions — only where the brief
   and stub genuinely underdetermine the capability (scope edges, must-vs-nice,
   failure behavior, integration boundaries). Write the answers into the PRD's
   Clarifications section; they must not live only in chat.
3. Draft the full PRD (`status: draft`) with every section of
   `${CLAUDE_PLUGIN_ROOT}/templates/prd.md`. Requirements are numbered
   `FR-NNN` with a `must | should | could` priority (an unmet "must" means
   the capability does not ship). ACs use the EARS form — `WHEN <trigger>,
   THE SYSTEM SHALL <observable behavior>` — and name the FRs they verify;
   every AC must be binary, a human tester can answer pass/fail. Every known
   exclusion goes under Out of scope explicitly.
4. **Gate.** Present, revise until the owner approves, then set
   `status: approved`.

## Amending an approved PRD

Never edit an approved PRD directly. Write
`changes/NNN-<slug>/proposal.md` from
`${CLAUDE_PLUGIN_ROOT}/templates/change-proposal.md`. Gate the proposal; on
approval merge the deltas into the PRD and set the change `status: applied` in
the same session.

## Next step

End with exactly one recommendation:

- Stubs remain → name the next stub to develop with this skill, and why it is
  next (dependencies approved, unblocks the most).
- The PRD just approved forces a technology or architecture choice → recommend
  `/spectacular:decide` and name the decision.
- A PRD is approved and no decision blocks it → recommend `/spectacular:plan`
  for it — breakdown is the next lifecycle stage.
