# <product-name> — workspace

This is a **spectacular** workspace: the documentation home of a multi-repo
product. Code lives in sibling repositories; `.spectacular/registry.md` lists
them, and each code repo points back here via its `.spectacular/contract.md`.

## How this workspace works

- **State is derived, never stored.** Where things stand is always computed from
  artifact files and their front matter. There is no status file; if any summary
  disagrees with the files, the files win.
- **Files are the interface.** Manually editing any artifact — including
  front-matter statuses — is always legitimate.
- **Orientation:** run `/spectacular:next` to derive current state and get one
  recommended action.

## Commit protocol

Nothing is committed unprompted — by a skill or by any session working here.
Each **unit of work** ends with a proposed commit message; the owner reviews
the diff and approves, and only then does the commit happen. Pushing likewise
happens only on explicit ask.

One commit per unit of work: the scaffold; the approved brief; the PRD-map
stubs; each developed PRD (plus any change proposal it opened); each ADR with
its overview update; each plan batch; each retro review's applied fixes.
The one exception is `/spectacular:implement`'s **code-repo** commit — one
task = exactly one squashed mainline commit is itself the unit of work; the
workspace edits it makes (statuses, Learnings) still get a proposed workspace
commit at close-out.

## Layout

| Path | Contents |
|------|----------|
| `product/brief.md` | the product brief |
| `product/prds/` | one PRD per capability, `NNN-<slug>.md` |
| `product/designs/` | design specs (`NNN-<slug>.md`); `system/` holds imported design code + distilled `tokens.json` / `design-language.md` (git-canonical, with `provenance.md`) |
| `architecture/overview.md` | living architecture overview |
| `architecture/decisions/` | ADRs, `NNN-<slug>.md` |
| `delivery/stories/` | user-visible slices of a PRD |
| `delivery/tasks/` | one repo's share of a story |
| `changes/` | amendment proposals to approved artifacts |
| `.spectacular/` | profile, code-repo registry, retro observations |
| `conventions.md` | naming conventions (optional) |

References are `<type>-<NNN>` and resolve by filename: `prd-001` →
`product/prds/001-*.md`, `design-002`, `adr-003`, `story-004`, `task-012`
likewise. Numbering is per type, zero-padded to 3. The filename is the
identity.

## Definitions of Ready and Done

Uniform for every item — defined once here, enforced by the skills
(`/spectacular:plan` only writes items that are ready; `/spectacular:implement`
checks ready before starting and walks done before closing). The item-specific
part of "done" lives in each story's Acceptance criteria and each task's
Verification; these definitions are the invariant rest.

**Story ready:** its PRD is approved; ACs are Given/When/Then test scripts
mapped from the PRD's ACs; every AC is covered by at least one task; a story
covering designed UI references the approved design spec sections it
implements (when its PRD has a design spec); its `depends_on` stories are
done.

**Story done:** all its tasks are done; a human tested every AC and logged
PASS in the Acceptance log; the human sign-off (never the plugin) flips
`status: done`.

**Task ready:** its story is ready; its `repo:` is in the registry with a
contract; Verification (preconditions, steps, expected) is written; its
`depends_on` tasks are done.

**Task done:** Verification passes; exactly one squashed mainline commit
(`task-NNN: …`); Learnings appended; `status: done`.

## Ways of working (Karpathy guidelines)

### 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

- State assumptions explicitly — if uncertain, ask rather than guess.
- Present multiple interpretations — don't pick silently when ambiguity exists.
- Push back when warranted — if a simpler approach exists, say so.
- Stop when confused — name what's unclear and ask for clarification.

### 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If 200 lines could be 50, rewrite it.

The test: would a senior engineer say this is overcomplicated? If yes, simplify.

### 3. Surgical changes

Touch only what you must. Clean up only your own mess.

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused; leave
  pre-existing dead code alone unless asked.

The test: every changed line should trace directly to the request.

### 4. Goal-driven execution

Define success criteria. Loop until verified.

| Instead of… | Transform to… |
|---|---|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

For multi-step tasks, state a brief plan: each step paired with its verification.
