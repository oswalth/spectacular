---
name: prd
description: Propose the PRD map on first run, or develop one PRD from stub to approved — bounded clarify pass, checkable acceptance criteria, explicit out-of-scope; a draft left for team review is revised from its review comments. Requires an approved product brief.
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
3. **Gate** (explicit approval only — gate protocol, CLAUDE.md). On
   approval, write one **stub** PRD per capability — the map is
   persisted only as stub PRDs, nowhere else. File:
   `product/prds/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/prd.md`, reduced to the stub form:
   `status: stub`, `depends_on` filled, the title, and a one-line Scope —
   drop the remaining sections until the PRD is developed. A stub may carry an
   optional `## Notes for development` section for ideas parked here by other
   sessions (e.g. another PRD's clarify pass); nothing else.
4. **Propose a commit** for the map (e.g. `add PRD map (prd-001…prd-006
   stubs)`); commit only on the owner's explicit approval — the workspace
   commit protocol (CLAUDE.md) applies to every unit of work.

## Mode B — stubs exist: develop one PRD

1. Pick the target: the `prd-NNN` argument if given; otherwise suggest the stub
   whose `depends_on` are all approved and which unblocks the most other stubs
   (name any drafts in review too — they belong to their authors, see
   Revise). Read the workspace fresh first — fetch and fast-forward when it
   has a remote. A target already at `status: draft` enters **Revise** below
   instead of steps 2–3.
2. **Clarify pass.** Ask at most 5 structured questions — only where the brief
   and stub genuinely underdetermine the capability (scope edges, must-vs-nice,
   failure behavior, integration boundaries). Work propose-then-ask: precede
   the questions with a short frame of what the brief and stub already settle
   and where you stand, so each question reads against a stated position.
   Write the answers into the PRD's Clarifications section; they must not
   live only in chat. If an answer amends the *approved brief* (a phrasing
   now wrong, a scope call the brief doesn't record), open
   `changes/NNN-<slug>/proposal.md` targeting the brief in the same session —
   clarifications must never strand brief deltas. Challenge answers that
   would weaken the capability — with your justification and a proposed
   alternative — and say explicitly when the owner's point stands as-is; the
   owner's call is final.
3. Draft the full PRD (`status: draft`) with every section of
   `${CLAUDE_PLUGIN_ROOT}/templates/prd.md`. Requirements are numbered
   `FR-NNN` with a `must | should | could` priority (an unmet "must" means
   the capability does not ship). ACs use the EARS form — `WHEN <trigger>,
   THE SYSTEM SHALL <observable behavior>` — and name the FRs they verify;
   every AC must be binary, a human tester can answer pass/fail. Every known
   exclusion goes under Out of scope explicitly.
4. **Gate.** Present, revise until the owner approves — approval is an
   explicit answer to an explicit question; a vague go-ahead re-asks (gate
   protocol, CLAUDE.md) — then set `status: approved` and drop the empty
   Review section. The owner may instead **leave it in review** for the
   team: the PRD stays `status: draft` with its Review section in place,
   teammates add comment lines there (workspace CLAUDE.md, Reviews), and a
   later run — by whoever carries the PRD — revises it.
5. **Propose a commit** — `docs(prd-NNN): approve — <slug>`, or
   `docs(prd-NNN): draft for review — <slug>` when left in review — with its
   push in a workspace with a remote (a draft nobody can fetch is not in
   review), plus any change proposal opened in step 2; commit only on
   explicit approval.

## Revise — a draft with review comments

Entered from Mode B when the target is `status: draft`: a PRD left in review
by an earlier session — the owner's or a teammate's. Review lines live in
the PRD's `## Review` section, one per comment, `- <date> — <name> —
<comment> (FR-003 / AC-2 / Scope …)`; a line is **open** until it carries a
` → ` resolution.

1. Read the draft and its Review section. No open line → the PRD is ready to
   approve: go to Mode B step 4.
2. Propose one resolution per open line, in one list: **apply** — the
   concrete delta (which FR, AC or section; old → new); **decline** — with
   the justification; **ask** — when the comment underdetermines the change,
   one question to its author (the name on the line), at most 5 questions in
   the run. Challenge a comment that would weaken the capability —
   justification plus a proposed alternative — and say explicitly when a
   comment stands as-is. A resolution that amends the approved brief opens
   a `changes/` proposal, as in Mode B step 2.
3. **Gate** — an explicit question, an explicit approval naming which
   resolutions (gate protocol, CLAUDE.md); partial approval is normal. Apply
   the approved deltas; mark every handled line in place (` → <date>
   applied` / ` → <date> declined: <why>`); move a declined point worth
   keeping into Clarifications. Unapproved lines stay open.
4. Then ask: **approve now, or leave in review?** Approval needs every line
   resolved and the team's agreement — the call of whoever carries the PRD,
   nothing is stored about who that is: `status: approved`, Review section
   dropped (git keeps it). Otherwise `status: draft` stays for the next
   round.
5. **Propose a commit** — `docs(prd-NNN): approve — <slug>`, or
   `docs(prd-NNN): revise draft — <what changed>` — with its push; commit
   only on explicit approval.

## Amending an approved PRD

Never edit an approved PRD directly. Write
`changes/NNN-<slug>/proposal.md` from
`${CLAUDE_PLUGIN_ROOT}/templates/change-proposal.md`. Gate the proposal; on
approval merge the deltas into the PRD and set the change `status: applied` in
the same session.

## Next step

End with exactly one recommendation:

- A PRD left in review → say who acts next: reviewers add their lines, then
  its author runs this skill on it again; a draft whose lines are all
  resolved → approve it with this skill.
- Stubs remain → name the next stub to develop with this skill, and why it is
  next (dependencies approved, unblocks the most).
- The PRD just approved forces a technology or architecture choice → recommend
  `/spectacular:decide` and name the decision.
- A PRD is approved and no decision blocks it → recommend `/spectacular:plan`
  for it — breakdown is the next lifecycle stage.
