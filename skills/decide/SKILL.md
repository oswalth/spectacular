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
   ADR's `prd:` field when it applies).
2. **Drivers.** List what actually constrains the choice, each traced to the
   brief, a PRD, or a stated constraint — not generic virtues.
3. **Options.** 2–4 realistic candidates. If the owner named a favorite, it is
   one option among the others, not the conclusion.
4. **Trade-off table.** Options × drivers, filled with specifics. Below it, give
   your recommendation with reasoning — clearly marked as a recommendation.
5. **Owner picks.** Never auto-pick, never treat silence as consent.
6. **Write the ADR** — `architecture/decisions/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/adr.md` (MADR 4.0 structure). The `prd:`
   field is optional — drop it when no PRD forced the decision. Pros and Cons
   of the Options records every rejected option and why it lost — that section
   is the ADR's value; Confirmation states how compliance will be verified.

7. **Gate.** Present; on approval set `status: approved`.
8. **Update `architecture/overview.md`** — the living overview (create it on
   first use from `${CLAUDE_PLUGIN_ROOT}/templates/overview.md`). Reflect the
   decision; link the ADR. The overview states what IS; the ADR records why.

To revisit an approved ADR, do not edit it — either write a superseding ADR, or
amend it via a `changes/NNN-<slug>/proposal.md` (status draft → approved →
applied), whichever the owner prefers.

## Next step

Recommend returning to the work that raised the decision — the specific
`/spectacular:prd` or `/spectacular:plan` invocation that was blocked, now
unblocked by the approved ADR. If nothing was blocked, recommend
`/spectacular:next` to re-derive where things stand.
