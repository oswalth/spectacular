# spectacular

A Claude Code plugin for AI-assisted SDLC on **multi-repo products**: from idea
to merged code through seven commands — brief → PRDs → decisions → stories and
tasks → implementation → acceptance.

The model: one **workspace repo** holds all product documentation (brief, PRDs,
ADRs, stories, tasks); **code repos** live as its sibling directories, each
linked back via a small contract file. State is always **derived from artifact
files** — there is no status database, and manually editing any artifact is
always legitimate.

## Install and update from a local checkout (temporary)

> **Note:** this section covers running the plugin straight from a local clone,
> before the repo is published to GitHub. Remove it at publication.

For development and daily use from the checkout, load the plugin without
installing:

```bash
claude --plugin-dir ./spectacular
```

After editing plugin files, run `/reload-plugins` in the session to pick up the
changes — no restart needed. Sanity-check the manifests any time with
`claude plugin validate .` from the repo root.

Alternatively, install from the checkout as a local marketplace (the path must
start with `./`):

```
/plugin marketplace add ./spectacular
/plugin install spectacular@spectacular
```

Installed plugins are copied into `~/.claude/plugins/cache`, so local edits are
not picked up automatically — run `/plugin marketplace update spectacular`
after changes, and if they still don't appear, uninstall and reinstall. The
`--plugin-dir` flow avoids this entirely and is the recommended one while the
plugin lives only on this machine.

## Install

The plugin repo is its own marketplace. From any Claude Code session:

```
/plugin marketplace add <owner>/spectacular
/plugin install spectacular@spectacular
```

Works with a private GitHub repo — installation rides your existing GitHub
credentials (`gh` login or SSH key).

**Private-repo gotcha:** background auto-update needs git credentials without a
prompt. Run `gh auth setup-git` once, or keep your SSH key loaded in an agent.

## Update

```
/plugin marketplace update spectacular
```

## Use

Commands in lifecycle order — full reference in
[docs/commands.md](docs/commands.md), recommended model per command in
[docs/models.md](docs/models.md):

| Command | Does |
|---------|------|
| `/spectacular:init` | empty dir → workspace scaffold + product brief (interview) |
| `/spectacular:prd` | PRD map first, then one PRD at a time to approved |
| `/spectacular:decide` | just-in-time ADR when a choice blocks progress |
| `/spectacular:plan` | approved PRD → stories + per-repo tasks; creates missing code repos |
| `/spectacular:implement` | in a code repo: one task → one squashed mainline commit |
| `/spectacular:next` | derives state, renders the roadmap, recommends one action |
| `/spectacular:retro` | one-line friction capture; periodic review |

A typical first run: `mkdir acme-product && cd acme-product`, then
`/spectacular:init`. Approve the brief, let `/spectacular:prd` map the
capabilities, `/spectacular:plan` the first approved PRD (it will offer to
create `../acme-api` and friends), then `/spectacular:implement` inside the
code repo. `/spectacular:next` tells you where you are whenever you are lost.

Every command ends with a justified next action, and PRDs, ADRs, the brief, and
breakdowns all gate on your explicit approval. A read-only **repo-reader**
subagent inspects code repos on behalf of prd/decide/plan; it never writes.

## Notes

- v0.1 is greenfield-only: workspace and code repos are created by the plugin.
- Task branches are always squashed — one task = exactly one mainline commit
  (`task-NNN: …`), via PR or local rebase per each repo's contract.
- `docs/commands.md` is generated: `python3 scripts/generate-docs.py`.
