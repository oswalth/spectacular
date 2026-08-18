# Recommended models

Recommendations only — **nothing is pinned**. Every skill and the repo-reader
subagent inherit the session model; you always choose. The rule: cheapest model
that works, upgraded only where the quality gain is significant and failure
costs more than the token premium. Escalation is your call, evidenced by retro
observations — there is no automatic ladder.

Review this table at every retro; the model landscape moves.

| Command | Recommended | Escalate |
|---------|-------------|----------|
| `/spectacular:init` | opus | — (judgment-dense, low volume, everything downstream builds on the brief) |
| `/spectacular:prd` | opus | — (ACs steer all delivery work) |
| `/spectacular:design` | opus | — (design truth gates all UI delivery; mapping visuals to requirements is judgment-dense) |
| `/spectacular:decide` | opus | fable for foundational, hard-to-reverse ADRs |
| `/spectacular:plan` | sonnet | opus when cross-repo coupling is non-trivial, or a bug triage spans repos |
| `/spectacular:implement` | sonnet | opus after a task fails its goal-driven loop twice |
| `/spectacular:bug` | haiku | sonnet if the evidence elicitation misses obvious gaps |
| `/spectacular:next` | haiku | sonnet if ranking quality disappoints |
| `/spectacular:retro` | haiku (append) | sonnet for review mode |
| `/spectacular:upgrade` | sonnet | — (mechanical scan plus gated edits) |
| repo-reader (subagent) | sonnet | — |

## Retro evidence

Kept short, newest first — the observations that shaped a row.

- 2026-08 — `implement` on a frontier model at very high effort: pre-code
  deliberation ran as 24–32k-token thinking blocks (5–7 minutes each) before
  any visible plan. Plan-first (implement step 5) makes it legible; the token
  cost is the effort setting, not the skill. The sonnet recommendation for
  `implement` stands.
