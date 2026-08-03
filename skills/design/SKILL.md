---
name: design
description: Record the product's UX design as a truth artifact — flows, screens, states, and design-tool sources mapped to the PRD's requirements — and import ready design code (e.g. a Claude Design project) into the workspace, git-canonical. Gated like every truth artifact; consumed by plan and implement.
argument-hint: [prd-NNN]
---

# /spectacular:design — record the UX design as truth

The plugin never generates UX. The owner (or their designer) designs in the
design tool — Figma, Claude Design (claude.ai/design), or equivalent; this
skill turns that work into reviewable, linkable truth: a **design spec** per
PRD (which flows and screens exist, what states they have, where the sources
live, which requirements the visuals constrain) and, when ready design code
exists, an **imported copy** of it in the workspace. plan routes
stories/tasks against the specs; implement pulls the referenced frames and
code into the task capsule.

## Design-code convention

Imported design code is **git-canonical**: after import, the files in the
workspace are the design truth and the external tool remains the authoring
surface. Two placement levels:

- `product/designs/system/` — product-wide design code (visual direction,
  foundations, component systems, themes), one per workspace;
- `product/designs/NNN-<slug>/` — screen prototypes belonging to one design
  spec, next to its `NNN-<slug>.md`.

Every import directory carries a `provenance.md`: source project (id + URL),
a remote→local file map, the import date, viewing notes, and the refresh
procedure. Import source-only — no dependency installs, no build outputs.
**Refresh is explicit and gated**: diff the source's file list against the
provenance map, fetch only what changed, show the owner the diff, overwrite
on approval, update provenance — never silently.

## Precondition

The target PRD has `status: approved` — design specs refine an agreed
capability, not a moving one. Otherwise refuse and point at `/spectacular:prd`.

## Steps

1. **Pick the target.** The `prd-NNN` argument if given; otherwise suggest the
   approved PRD with user-facing surface and no design spec yet.
2. **Context.** Read the PRD and the brief. If a Figma MCP (or equivalent
   design-tool MCP) is connected, read the named file or pages to inventory
   frames and screens; otherwise work from links, exports, or descriptions the
   owner provides. Never invent screens — everything in the spec must trace to
   a real design source or be listed as an open design question.
3. **Import ready design code** (when the owner has it — a Claude Design
   project, an exported prototype, design-code files). Fetch or copy it into
   the workspace per the design-code convention above (`system/` for
   product-wide code, the spec's own folder for its screens), write
   `provenance.md`, and record the source in the spec's `sources:`. Use the
   available integration to read the source (Claude Design via the design
   tool access in Claude Code; plain files otherwise). If an import already
   exists, this step is the gated **refresh** instead.
4. **Clarify pass.** At most 5 questions, propose-then-ask: which flows are in
   scope, platform conventions (iOS/Android/web divergence), which states are
   worth specifying per screen, and what is deliberately left undesigned.
5. **Draft the design spec** — `product/designs/NNN-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/design.md` (`status: draft`): flows with
   their screens (each screen carrying its source link and states),
   cross-cutting patterns, a Requirement mapping ONLY where the design
   constrains acceptance, and open design questions. If the design work
   exposes a gap or contradiction in the approved PRD, open a
   `changes/NNN-<slug>/proposal.md` — never bend the spec to paper over it.
   Screens may source from Figma frames, imported design code, or both; the
   Cross-cutting section points into `product/designs/system/` where a
   product-wide design system exists.
6. **Gate.** Present; on approval set `status: approved`.
7. **Propose a commit** for the design spec — plus any imported design code
   and its provenance — as one unit (e.g. `design-001: <what it covers>`);
   commit only on explicit approval (workspace commit protocol, CLAUDE.md).

## Next step

Recommend `/spectacular:plan` for the PRD if nothing else blocks it — the
design spec is exactly what its UI stories and tasks will reference. If step 5
opened a change proposal, that approval comes first.
