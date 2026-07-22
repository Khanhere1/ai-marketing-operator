# Implementation Roadmap

## Phase 0 — Discovery and design (Weeks 1–4)

- Interview marketers, media buyers, founders, analysts, sales leaders, and compliance owners.
- Observe weekly review, campaign planning, content, SEO, and experiment workflows.
- Freeze MVP/non-goals.
- Define canonical entities, metric registry, evidence model, decision ledger, action contract, and threat model.
- Create golden evaluation cases ([evaluations/EVALUATION_PLAN.md](evaluations/EVALUATION_PLAN.md)) before prompt optimization.

**Exit:** one repeated high-value workflow, identified buyer, available data, measurable baseline, and agreed risk envelope.

## Phase 1 — Core kernel (Weeks 5–12)

- Organization Context Pack ([schemas/organization-context.schema.json](schemas/organization-context.schema.json))
- Identity/tenant model
- Workflow state machine ([workflows/](workflows/))
- Structured artifact and event schemas ([schemas/](schemas/))
- Evidence store and decision ledger
- Policy/approval interface ([policies/global-prohibitions.yaml](policies/global-prohibitions.yaml))
- Audit/observability
- Provider/connector abstractions
- Evaluation harness ([evaluations/golden-cases/](evaluations/golden-cases/))

**Exit:** reproducible advisory workflows, validated schemas, safe recovery, no write access.

## Phase 2 — Marketing intelligence MVP (Weeks 13–20)

- Generic CSV/warehouse ingestion
- Initial analytics, CRM, search-performance, and ad-reporting adapters
- Data-quality report ([schemas/data-quality.schema.json](schemas/data-quality.schema.json))
- Weekly growth review ([workflows/weekly-growth-review.yaml](workflows/weekly-growth-review.yaml))
- Paid-media analysis and operator tasks ([workflows/paid-media-review.yaml](workflows/paid-media-review.yaml))
- Funnel/lead-quality diagnosis
- SEO/AEO/GEO review
- Executive report

**Exit:** useful shadow-mode outputs, measurable time saving, high evidence coverage, acceptable revision rate.

## Phase 3 — Content and experiment copilot (Weeks 21–28)

- Evidence-backed briefs and drafts
- Claim registry
- Experiment registry/design
- Publishing and campaign change-set preparation
- Human approval queue

**Exit:** reliable drafts/change sets; every external action still manually performed.

## Phase 4 — Approved actions (Weeks 29–40)

- Action capability registry ([schemas/action-contract.schema.json](schemas/action-contract.schema.json))
- Official-API adapters
- Dry run, transaction approval, verification, audit, rollback
- CMS drafts, social scheduling, metadata updates, internal ticketing
- Paid-media draft creation and narrowly scoped approved changes

**Exit:** selected workflows pass offline, security, shadow, and controlled-production qualification.

## Phase 5 — Bounded autonomy and packs

- Standing approvals with expiry and financial/object limits
- Industry/business-model packs
- Agency multi-account controls
- Private deployment options
- Continuous requalification and drift monitoring

## First 30 days

1. Name the project (`ai-marketing-operator`) and set Apache-2.0 license.
2. Recruit 3–5 design partners.
3. Finalize MVP workflow: weekly marketing review plus paid-media operator plan.
4. Publish schemas and sample artifacts ([examples/](examples/)).
5. Build 25–50 golden scenarios ([evaluations/golden-cases/](evaluations/golden-cases/)).
6. Define supported/non-supported data classes.
7. Implement read-only CSV fixture workflow.
8. Run first human benchmark.
9. Open public roadmap and contribution process.
10. Do not merge production write capabilities yet.
