---
name: onboard
description: Set up a teammate or a new machine on an existing workspace — clone the registered code repos the person can reach (access is whatever GitHub grants, narrowed to the areas they work in), check every chosen repo's README prerequisites and install the missing ones only under a gate, verify the integrations the artifacts imply, and orient toward a scoped next. Idempotent — rerun it as a machine doctor.
argument-hint: [role]
---

# /spectacular:onboard — a person or a machine joins

Runs **in a workspace checkout** — the workspace repo is the entry point a
newcomer clones first; everything else is derived from it. Writes nothing
into the workspace; it changes the *machine* (clones, installs), and only
under gates. Access is never modelled in artifacts: GitHub decides what a
person can reach, and this skill derives from that.

## Steps

1. **Locate.** `.spectacular/profile.md` here → workspace; otherwise refuse
   and say what to do: clone the workspace repo, then run this inside it.
   Compare the installed plugin version with the pin: plugin older than the
   pin → update the plugin first (README, Update) and stop; pin older than
   the plugin → note it and carry on — `/spectacular:upgrade` is the owner's
   job, after onboarding, not this one's.
2. **Fresh workspace.** If the workspace has a remote, `git fetch` and
   fast-forward when behind (a checkout with local changes is left alone and
   reported).
3. **Reachability — derived access.** For every registry row
   (`name | path | remote | role | one-liner`): path present → already here
   (fetch; report branch and whether it is behind); path absent and
   `remote` empty → *no remote recorded — ask the owner to fill it in the
   registry*; otherwise `git ls-remote <remote>` (quiet, under a timeout):
   reachable → clonable; refused → *no access (the host refused) — ask the
   owner if your work needs this repo*. Report the table. Nothing is stored
   about the person; the next run derives it again.
4. **Area.** The `[role]` argument, or ask once: which of the reachable
   areas (distinct `role` values) does this person work in? Default: all
   reachable. Clone the chosen repos that are absent (`git clone <remote>
   <path>`, sibling layout per the profile); unchosen repos are not cloned
   and not checked further — a web developer never sees the infra
   toolchain.
5. **Prerequisites — from the READMEs.** For each chosen repo read the
   `## Prerequisites` section of its `README.md` (missing section → report
   it; `/spectacular:upgrade` adds the structure, the owner the content).
   Check each listed tool non-interactively under a timeout (`<tool>
   --version` or the README's own check), compare with the version
   constraint, and show a table: present / missing / version mismatch /
   unknown how to check. Then **gate**: propose the install commands for
   this platform — the platform's package manager or the version manager
   the README names, one command per tool, no silent privilege elevation —
   and run them **only on an explicit approval naming which tools** (gate
   protocol, workspace CLAUDE.md); a vague go-ahead re-asks. Re-check after
   installing. A tool you cannot install non-interactively is a manual step:
   say exactly what to run.
6. **Integrations — derived from the artifacts.** Check, never configure:
   - any chosen repo with `merge_flow: pr` → `gh auth status`; if it fails,
     point at the README's private-repo gotcha (`gh auth setup-git`);
   - a chosen UI repo plus design specs with Figma or Claude Design
     `sources:` → is a design-tool MCP connected? The plugin never ships or
     configures MCP servers — print that `/mcp` is where the person connects
     one, and that design/implement degrade to plain links without it;
   - a prerequisite line that names a login step (a cloud CLI, a registry)
     → run the status check it names, if any; otherwise list it as a manual
     step.
7. **Orientation**, short: the product one-liner from `product/brief.md`;
   the workspace `CLAUDE.md` as the rules that bind everywhere (gate and
   commit protocol, Language — artifacts stay in the workspace's artifact
   language, the conversation follows the person's own Claude Code
   `language` setting, `/config` → Language); each chosen repo's `CLAUDE.md`
   imports the workspace rules — Claude Code asks once per repo to allow
   that external import, approve it; `/spectacular:next <role>` shows their
   work and nothing else.

Rerunning on a machine already set up is the intended way to check it:
every step is a check before it is an action.

## Next step

Recommend `/spectacular:next <role>` for the area just chosen (bare
`/spectacular:next` when they took everything) — the first thing a newcomer
needs is what is ready for them, scoped to their repos. If the pin was older
than the plugin, also name `/spectacular:upgrade` for the owner.
