---
name: upgrade
description: Align a workspace with the installed plugin version — walk the shipped per-version upgrade notes, scan for structural drift against current templates, apply gated fixes, and bump the version pin. Equal versions run the drift scan as a verification pass. Approved truth is only ever amended via changes/.
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
     outdated sections;
   - `conventions.md` (if present) vs `templates/naming-families.md`: letters
     must carry their frozen family meaning;
   - `.spectacular/` files present and well-formed.
4. **Propose the migration set**, split by ownership:
   - **Plugin-owned scaffolding** (CLAUDE.md sections, conventions structure,
     profile) → direct edits, applied under this gate.
   - **Approved truth artifacts** (brief, PRDs, ADRs, designs) → a `changes/`
     proposal, and only where the new standard exposes a concrete defect.
     Template conformance alone never rewrites approved truth — approved is
     approved.
5. **Apply** the approved items; set the pin to the installed version.
6. **Propose one commit** — `upgrade workspace to spectacular vX.Y.Z`; commit
   only on explicit approval (workspace commit protocol, CLAUDE.md).

Validating that the *upgraded skills* work here is not this skill's job — and
not re-running completed stages' either: the next real lifecycle stage
exercises the new behavior on real work.

## Next step

Recommend `/spectacular:next` — the upgrade may have changed what is ready,
and any `changes/` proposal it opened is now a pending approval.
