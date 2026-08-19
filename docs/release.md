# Release procedure

Adopted by D-37. The universal rule, all repo kinds: **tags mark releases,
never commits.** Any commit's version is derived (`git describe --tags`),
never stamped per commit. Workspaces have no versions and no tags; code repos
release per their contract's `versioning`/`release_flow` fields.

Also universal: commit messages never carry AI-attribution trailers —
no `Co-Authored-By: Claude …`, no `Generated with …` — in any repo:
plugin, workspace, or code (D-37).

## Releasing the plugin

Owner-triggered. Steps 2–5 land in **one atomic release commit** — that is
what keeps CHANGELOG.md and docs/upgrades.md in sync by construction.

1. **Derive the bump** from Conventional Commit types since the last tag:
   `BREAKING CHANGE`/`!` → major (once past 1.0), `feat` → minor, everything
   else → patch. Any workspace-facing change — anything that needs an
   upgrades.md section — is at least minor.
2. **`.claude-plugin/plugin.json`**: set the new version. (marketplace.json
   carries no version field.)
3. **`CHANGELOG.md`**: add the version section — every release, no exceptions.
4. **`docs/upgrades.md`**: add a section iff the release changes
   workspace-facing behavior. Check the invariant now: every upgrades.md
   section has a matching CHANGELOG entry (upgrades ⊆ changelog).
5. **Manual checks** (lint and CI deferred — D-48): grep shipped files
   case-insensitively against `design/denylist.txt` (the design zone is
   shared with the team as the decision log but never ships publicly —
   D-12 as revised), regenerate `docs/commands.md` and confirm no diff,
   run `claude plugin validate .` — the full list is in CLAUDE.md
   "Manual checks".
6. Propose the release commit `chore(release): X.Y.Z` and stop — the owner
   reviews the diff (commit protocol, CLAUDE.md Ways of working #6).
7. On explicit approval: commit, then tag `vX.Y.Z` on that commit. Push
   (including `--tags`) only on explicit ask.

## Code repos

The release act belongs to the release manager (a human today; CI later, per
the D-24 trigger) — commits never bump versions. At release time the bump is
derived exactly as in step 1, from CC types since the repo's last tag, then
tagged `vX.Y.Z`. Whether a repo versions at all, and who releases it, is
recorded in its contract (`versioning`, `release_flow`).
