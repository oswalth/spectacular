---
workspace: ../<workspace-dir>
name: <registry-name>
merge_flow: pr
versioning: semver # semver | none — bump derived from CC types at release; see the plugin's docs/release.md (D-37)
release_flow: manual # manual | ci — who performs the release act; commits never bump versions or tag
---

## Stack

## Commands

- build: …
- test: …
- run: …

## Conventions

<!-- Elicited by plan's repo-bootstrap interview when the repo is created;
amended here — gated, owner-approved — as the repo evolves (see implement).
Never contradicts an approved ADR: a conflicting change needs a superseding
ADR first (/spectacular:decide). The dimensions below are the common core;
the interview adds stack-specific ones the forcing ADRs imply (e.g.
sync/async posture for an API, state management for a SPA, dataset
versioning for ML). Every implement capsule carries this section. -->

- Architecture style: … <!-- layering / DDD / hexagonal / plain modules -->
- Testing: … <!-- framework, coverage bar, fixture strategy, test data (factories/fakes) -->
- Tooling: … <!-- package manager, lint/format, type checking -->
- Build & packaging: … <!-- container strategy, artifact format -->
- Quality gates: … <!-- what must pass before a task lands -->
