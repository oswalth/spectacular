---
name: upgrade
description: Align a workspace with the installed plugin version — walk the shipped per-version upgrade notes, scan the workspace and its registered repos' contracts for structural drift against current templates, apply gated fixes, and bump the version pin. Equal versions run the drift scan as a verification pass. Approved truth is only ever amended via changes/.
---

# /spectacular:upgrade — align a workspace with the plugin

Workspaces pin the plugin version they were built with
(`.spectacular/profile.md`). When the plugin moves on, this skill carries the
workspace forward — without re-running any lifecycle stage and without ever
rewriting approved truth.

Runs **in a workspace** (profile.md present); otherwise refuse.

## Steps

1. **Compare versions.** Read the pin from `.spectacular/profile.md` and the
   installed version from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`.
   Equal → **verification mode**: skip step 2 (no migration items) and run
   the drift scan anyway — a workspace migrated by hand can claim the right
   pin while missing pieces; this is how that gets caught. Report a clean
   scan in one line and stop; findings follow the normal gated flow (steps
   4–6, no pin change). Pin *newer* than installed → the plugin itself is
   behind: recommend updating the plugin, stop.
2. **Collect migration items** from
   `${CLAUDE_PLUGIN_ROOT}/docs/upgrades.md`: every version section after the
   pin, up to the installed version, in order.
3. **Drift scan** regardless of the notes — report anything they don't
   explain:
   - workspace `CLAUDE.md` vs `templates/workspace-claude.md`: missing or
     outdated sections (Language included — an existing workspace names the
     language its artifacts already use);
   - `conventions.md` (if present) vs `templates/naming-families.md`: letters
     must carry their frozen family meaning;
   - `.spectacular/` files present and well-formed; the registry carries the
     `remote` column — an empty `remote` is proposed from the local clone's
     `git remote get-url origin` (derived, never invented);
   - each repo in `.spectacular/registry.md`, **read fresh** (fetch; default
     branch — workspace CLAUDE.md, Ways of working §5): a repo absent
     locally is reported as *unreachable — clone it (`/spectacular:onboard`)
     and re-run*, never silently skipped; its `.spectacular/contract.md`
     present and structured per `templates/contract.md` — front-matter
     fields complete, Conventions as the dimension list, a Toolchain notes
     section (an empty heading is fine — implement fills it); its
     `CLAUDE.md` present and aligned with `templates/code-claude.md`; its
     `README.md` carrying a Prerequisites section (structure — the content
     is *proposed* from manifests and the contract's Stack, marked inferred,
     for the owner to confirm). Code repos carry no version pin of their own
     (D-40): the workspace pin covers the constellation, and this pass is
     how their drift gets caught.
4. **Propose the migration set**, split by ownership:
   - **Plugin-owned scaffolding** (CLAUDE.md sections, conventions structure,
     profile, registry columns) → direct edits, applied under this gate.
   - **Approved truth artifacts** (brief, PRDs, ADRs, designs) → a `changes/`
     proposal, and only where the new standard exposes a concrete defect.
     Template conformance alone never rewrites approved truth — approved is
     approved.
   - **Code-repo files** (contract, `CLAUDE.md`, `README.md`) → gated edits
     in that repo, one change set per repo, landed per the repo's contract
     `merge_flow`: `pr` → branch `chore/spectacular-X.Y.Z`, push and
     `gh pr create` inside this gate's approval (the PR is merged by the
     repo's normal review); `local-rebase` → one commit on the mainline
     (`chore(spectacular): align with plugin vX.Y.Z`; a contract-only fix
     keeps `chore(contract): …`). Code-repo files are code-repo-local, not
     workspace truth. Structure only — never fill Conventions content the
     owner hasn't decided; a missing decision is a finding to report, not a
     blank to complete.
5. **Apply** the approved items — approval is explicit and names which
   items, PRs included; a vague go-ahead re-asks (gate protocol,
   CLAUDE.md). Set the pin to the installed version. A PR still open shows
   up as drift on the next equal-version run — that is the verification
   mode doing its job, not an error.
6. **Propose one commit** — `chore(spectacular): upgrade workspace to
   vX.Y.Z`; commit only on explicit approval (workspace commit protocol,
   CLAUDE.md).

Validating that the *upgraded skills* work here is not this skill's job — and
not re-running completed stages' either: the next real lifecycle stage
exercises the new behavior on real work.

## Next step

Recommend `/spectacular:next` — the upgrade may have changed what is ready,
and any `changes/` proposal it opened is now a pending approval.
