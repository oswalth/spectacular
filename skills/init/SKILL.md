---
name: init
description: Bootstrap a new spectacular workspace in an empty directory — scaffold, git init, a business-analyst interview producing the product brief, and an optional naming-conventions step. Start here for a new product.
---

# /spectacular:init — bootstrap a workspace

Creates the workspace repo of a multi-repo product: the single home for the brief,
PRDs, architecture decisions, and delivery breakdown. Code repos come later —
`/spectacular:plan` creates them as sibling directories. This skill needs no prior
context; everything it produces lives in files.

## Precondition

The current directory must be empty (ignore `.DS_Store` and similar). If it is not
empty, refuse and stop: spectacular v0.1 is greenfield-only — onboarding an existing
product is deliberately deferred until a real need appears. Do not scaffold into a
non-empty directory.

## Steps

1. **Ask for the product name.** One question, nothing else yet.

2. **Scaffold.** Create:
   - `CLAUDE.md` — copy the template at
     `${CLAUDE_PLUGIN_ROOT}/templates/workspace-claude.md`, replacing
     `<product-name>`.
   - `README.md` — 3–5 lines: product name, "documentation workspace of a
     multi-repo product", pointers to `CLAUDE.md` and `/spectacular:next`.
     Fill the product one-liner in after the interview (step 4).
   - `.spectacular/profile.md` — read the installed plugin version from
     `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`, then write:

     ```markdown
     ---
     plugin: spectacular
     plugin_version: <installed version>
     layout: sibling
     ---

     Code repos live as sibling directories of this workspace
     (`../<repo-name>`), each pointing back here via its
     `.spectacular/contract.md`. The registry is the authoritative list.
     ```
   - `.spectacular/registry.md` — the empty code-repo registry:

     ```markdown
     # Code-repo registry

     | name | path | role | one-liner |
     |------|------|------|-----------|
     ```

   Other directories (`product/`, `architecture/`, `delivery/`, `changes/`) are
   created lazily by whichever skill first writes into them — do not create them
   empty.

3. **git init + scaffold commit.** Run `git init`, then propose the commit
   message `scaffold <product-name> workspace` and commit only on the owner's
   approval — the workspace commit protocol (recorded in CLAUDE.md) applies
   from the very first commit: never commit or push unprompted.

4. **BA interview.** Act as a business analyst working propose-then-ask, never
   interrogation. Cover, in order: problem, users, goals, non-goals,
   constraints. For each topic:
   1. **Frame first** — a short paragraph of what is already known or assumed
      from the conversation so far, plus a strawman position where you have
      one, so the owner has something to react to instead of a blank page.
   2. **Then ask** 2–3 focused questions that reference the frame.
   3. **Close with a mini-summary** the owner confirms or corrects before the
      next topic.

   Weave in three opportunity-assessment questions: what alternatives
   exist today, why build this now, and how success will be measured — the
   answers sharpen Goals and Constraints. Never invent answers — if the owner
   is unsure, record the point as open. Push back once when a stated goal looks
   like a solution in disguise; accept the owner's call.

5. **Write `product/brief.md`** from
   `${CLAUDE_PLUGIN_ROOT}/templates/brief.md` (`status: draft`). It is the one
   product document — no other product-level doc exists. Fill the Positioning
   two-liner from the interview answers; if it cannot be filled sharply, that
   is a finding — say so and record the gap under Open points. The Product
   shape section is a capability sketch: 2–4 lines per capability plus its
   sharpest open question — enough to see the product's shape, never a feature
   spec; full treatment lives in the PRDs.

6. **Optional naming conventions.** Offer in one sentence; skipping is the normal
   path (descriptive names like `<product>-api` work fine). If taken, the
   letter→family taxonomy is FROZEN — never invent product-specific families:
   1. Read `${CLAUDE_PLUGIN_ROOT}/templates/naming-families.md`: the canonical
      letter table, its decision rules, and the codename rules.
   2. With the owner, **activate** the families this product foreseeably needs
      (G almost always — the workspace repo itself is governance). Letters keep
      their frozen meaning even when inactive: M is machine intelligence even
      if the product has no AI today.
   3. Suggest 2–3 **themes derived from the product idea**, checking theme
      viability: every activated family must have 5–10 pronounceable
      candidates under its letter, or the theme is disqualified. The owner
      picks one.
   4. Write `conventions.md`: the family table with activated rows marked, the
      chosen theme, and a candidate pool per activated family following the
      template's codename rules.

   Worked example: product **acme**, theme *constellations*, activated
   G / A / B / C / H; later `/spectacular:plan` names the workspace-adjacent
   repos **acme-andromeda** (A, API), **acme-bootes** (B, web portal),
   **acme-cassiopeia** (C, mobile app), **acme-hydra** (H, infra).

7. **Approval gate.** Present the brief together with the depth ladder, so its
   deliberate thinness reads as intentional: brief (problem, users, goals,
   constraints, one capability sketch) → PRD map → developed PRDs (full
   feature treatment) → stories and tasks. Then ask for approval. On explicit
   approval, set `status: approved` yourself. If the owner wants changes, revise
   and re-present. Manual edits to any artifact, including statuses, are always
   legitimate — files are the interface.

8. **Propose the closing commit** for whatever state the session ends in
   (e.g. `add approved product brief and naming conventions`); commit only on
   the owner's explicit approval.

## Next step

End with exactly one recommendation:

- Brief approved → recommend `/spectacular:prd`, because the PRD map is the next
  artifact in the lifecycle and nothing downstream (plan, implement) can start
  without an approved PRD.
- Brief still draft → the next action is the owner reviewing `product/brief.md`;
  they can re-run this gate or flip `status:` manually.
