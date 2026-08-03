# Naming families — the frozen letter taxonomy

The first letter of a codename identifies the thing's **family**. The taxonomy
below is FROZEN and product-independent: a letter keeps its meaning even if the
product never activates it, so letters can never be spent greedily on whatever
need showed up first (the classic mistake: M given to "mobile apps", colliding
with machine intelligence a year later — mobile is C, machine intelligence
is M, always).

Per product, only two things vary: which families are **activated** and which
**theme** supplies the codenames. Both live in the workspace's
`conventions.md`; this file never changes per product.

## Naming format

`<product-prefix>-<codename>` — prefix short, brandable, lowercase, identical
across all repos. The codename's first letter is the family; the rest uniquely
identifies the repo within it.

Never encode in a name: environment, region, language, framework, version,
lifecycle state, or deployment model. Those are metadata and belong in the
registry (`.spectacular/registry.md`).

## The families

| Letter | Family | Typical contents |
|--------|--------|------------------|
| A | Application services | domain APIs, backend services, transactional services |
| B | Browser applications | web portals, admin UIs, customer portals, microfrontends |
| C | Client applications | mobile, tablet, desktop, scanner and offline clients |
| D | Data & analytics | ETL/ELT, warehouse, BI, reporting, analytical models |
| E | Enterprise integrations | ERP, banking, EDI, market data, partner connectors |
| F | Foundations | shared libraries, internal frameworks, reusable packages |
| G | Governance | the workspace repo itself; standards, compliance, documentation |
| H | Hosting & infrastructure | Terraform/OpenTofu, cloud foundations, networking, DR |
| I | Identity & security | IAM, authorization, PKI, secrets, security platforms |
| J | Jobs & automation | batch jobs, schedulers, workers, reconciliation |
| M | Machine intelligence | AI/ML, LLM gateways, OCR, forecasting, recommendations |
| O | Observability | logging, metrics, tracing, alerting, SLO configuration |
| P | Platform engineering | Kubernetes platform, GitOps, developer portal, golden paths |
| Q | Quality engineering | E2E, integration, performance, resilience, security tests |
| S | Schemas & contracts | OpenAPI, AsyncAPI, protobuf, event schemas, canonical models |
| T | Tooling | CLIs, generators, templates, release and local-dev tools |

Reserved for the future — never repurposed, activated only when several repos
clearly require it: **K** knowledge systems / search / RAG · **L** localization
· **N** network, edge, IoT · **R** reliability, DR, incident engineering ·
**U** UI and design systems · **V** versioning and cross-system migrations ·
**W** workflow orchestration / BPM · **X** experimental (prefer metadata) ·
**Y**, **Z** unassigned.

## Family decision rules

- **A vs E**: implementing a business capability → A; most complexity is
  adapting an external system, protocol, or data model → E.
- **B vs C**: delivered through a browser → B; installed or device-specific
  → C.
- **C vs M**: mobile and desktop clients are C; AI/ML is M — never trade one
  letter for the other.
- **D vs M**: the product is analytical data → D; production ML/AI systems
  → M.
- **F vs S**: reusable executable code → F; language-neutral contract
  definitions → S.
- **H vs P**: H provisions raw infrastructure; P turns it into a
  developer-facing platform. Neither is a synonym for "all DevOps".
- **I**: dedicated shared security capabilities only; security logic specific
  to one application stays in that application's repo.
- **J**: only workers with an independent lifecycle, owner, or scaling model;
  otherwise the worker stays in its owning application's repo.
- **Q**: cross-system validation suites; unit tests stay with their source.
- **G**: non-runtime assets governing how the system is built and run — the
  spectacular workspace repo is always G.
- Several responsibilities → classify by the primary independently owned
  product or lifecycle, not by every technology inside.

**Not families** (implementation details, styles, lifecycle states — express
as registry metadata, never as a letter): API, microservice, monolith, worker,
database, SDK, DevOps, proof of concept, demo, experiment, migration.

## Codename rules

- Maintain a pool of 5–10 candidates per **activated** family.
- A valid codename: starts with the family letter; recognizable and
  pronounceable; lowercase ASCII, no spaces/punctuation/diacritics
  (normalize: `hong-kong` → `hongkong`); unique within the product;
  preferably 4–14 characters; avoids names tied to competitors, major
  software products, or politically disputed naming.
- **Theme viability check**: before the owner commits to a theme, verify every
  activated family genuinely has 5–10 candidates under its letter. A theme
  that starves an activated letter is disqualified — pick another theme, not
  another letter.
- Never silently reuse a retired codename for a different capability.

## Worked example

Product **acme**, theme *constellations*, activated families G, A, B, C, H:

- **acme-gemini** — G, the workspace repo
- **acme-andromeda** — A, core domain API
- **acme-bootes** — B, web portal
- **acme-cassiopeia** — C, mobile app
- **acme-hydra** — H, infrastructure

M stays frozen as machine intelligence even though acme has no AI yet — when
it arrives, the pool is musca / mensa / monoceros, and no renaming happens.
