---
name: decide
description: Work a forced architecture or technology decision — drivers, options, trade-off table; the owner picks, the result becomes an ADR recording every rejected option, and the architecture overview is updated.
argument-hint: [topic]
---

# /spectacular:decide — just-in-time architecture decision

ADRs are written only when a PRD or a plan forces a choice — architecture is not
a phase. The owner always picks; this skill never decides.

## Steps

1. **Name the decision.** From the argument or the conversation: what must be
   chosen, and which PRD or plan forces it now (that reference goes into the
   ADR's `prd:` field when it applies). State its **reversal cost** — how
   expensive this choice is to unwind later — because it scales the depth of
   everything below: a foundational, hard-to-reverse decision earns the full
   treatment; a cheap-to-reverse one may be worked briefly, and you say so.
   Repo-internal engineering conventions (testing approach, tooling,
   packaging, …) are not one forced decision: they are elicited at repo
   creation by `/spectacular:plan`'s repo-bootstrap interview into the repo's
   contract, and amended there later — decide handles a single contested,
   hard-to-reverse choice among them, not the batch.
2. **Clarify pass.** At most 5 questions on what the artifacts do NOT record:
   unstated constraints and preferences, prior experience with the candidates,
   appetite for build and operational effort, accounts or subscriptions
   already owned, risk tolerance. Work propose-then-ask — frame what the
   brief and PRD already settle, then ask against that frame. Skip only when
   the artifacts truly determine the choice, and say that you are skipping.
   Answers land in the ADR's Context and Drivers, not only in chat.
3. **Investigate.** Never assemble options from memory alone when the decision
   is hard to reverse: research the candidates' current state (versions,
   pricing, constraints, platform requirements) with web search, and dispatch
   **repo-reader** where registered code informs the choice. For
   cheap-to-reverse decisions the artifacts may suffice — say so explicitly.
4. **Drivers.** List what actually constrains the choice, each traced to the
   brief, a PRD, a clarify answer, or a stated constraint — not generic
   virtues.
5. **Options.** 2–4 realistic candidates. If the owner named a favorite, it is
   one option among the others, not the conclusion.
6. **Trade-off table.** Options × drivers, filled with specifics. For
   hard-to-reverse decisions, add each option's failure mode: how does this
   choice hurt in a year, and what would migration off it cost? Below the
   table, give your recommendation with reasoning — clearly marked as a
   recommendation.
7. **Owner picks.** Never auto-pick, never treat silence as consent.
8. **Write the ADR** — `architecture/decisions/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/adr.md` (MADR 4.0 structure). The `prd:`
   field is optional — drop it when no PRD forced the decision. Pros and Cons
   of the Options records every rejected option and why it lost — that section
   is the ADR's value; Confirmation states how compliance will be verified.
   Any **new external dependency** the decision introduces (a vendor, a
   service, a subscription) must be named as either decided here or an
   explicit follow-up decision — consequences never smuggle undecided
   dependencies into the architecture.

9. **Gate.** Present; on approval set `status: approved`.
10. **Update `architecture/overview.md`** — the living overview (create it on
    first use from `${CLAUDE_PLUGIN_ROOT}/templates/overview.md`). Reflect the
    decision; link the ADR. The overview states what IS; the ADR records why.
11. **Propose a commit** covering the ADR and the overview update as one unit
    (e.g. `adr-001: <decision title>`); commit only on the owner's explicit
    approval (workspace commit protocol, CLAUDE.md).

To revisit an approved ADR, do not edit it — either write a superseding ADR, or
amend it via a `changes/NNN-<slug>/proposal.md` (status draft → approved →
applied), whichever the owner prefers.

## Next step

Recommend returning to the work that raised the decision — the specific
`/spectacular:prd` or `/spectacular:plan` invocation that was blocked, now
unblocked by the approved ADR. If nothing was blocked, recommend
`/spectacular:next` to re-derive where things stand.
