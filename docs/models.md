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
| `/spectacular:decide` | opus | fable for foundational, hard-to-reverse ADRs |
| `/spectacular:plan` | sonnet | opus when cross-repo coupling is non-trivial |
| `/spectacular:implement` | sonnet | opus after a task fails its goal-driven loop twice |
| `/spectacular:next` | haiku | sonnet if ranking quality disappoints |
| `/spectacular:retro` | haiku (append) | sonnet for review mode |
| repo-reader (subagent) | sonnet | — |
