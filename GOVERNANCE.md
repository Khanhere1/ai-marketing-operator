# Governance

## Decision classes

### Low risk
Internal summaries, research synthesis, draft briefs, draft content, non-sensitive reporting.

- Owner approval optional according to organization policy
- Evidence references required for material statements
- Normal audit record

### Medium risk
Approved-content scheduling, CRM segment preparation, landing-page drafts, metadata updates, low-budget reversible tests.

- Functional owner approval
- Before/after preview
- Bounded scope and monitoring
- Rollback or compensation guidance

### High risk
Material spending, public claims, pricing statements, customer-data exports, tracking changes, major site changes, sensitive audiences, brand repositioning.

- Authenticated authorized approver
- Evidence and policy review
- Specific time-limited approval
- Detailed audit and monitoring
- Tested rollback or incident procedure

### Prohibited
Fabricated evidence, deceptive personalization, discriminatory targeting, unauthorized data use, impersonation, fake engagement/reviews, competitor-ad clicking, consent circumvention, platform-rule evasion, unreviewed regulated claims.

A human instruction cannot override a prohibition. See [policies/global-prohibitions.yaml](policies/global-prohibitions.yaml) for machine-readable rules.

## Approval principles

- Approval is for an immutable action package defined by [schemas/action-contract.schema.json](schemas/action-contract.schema.json), not a conversation.
- Any material plan change invalidates approval.
- Approvals contain scope, target systems, object identifiers, financial limit, permitted window, expiry, monitoring, and rollback.
- Separation of duties applies: proposer, approver, executor, and verifier are distinct roles for high-risk actions.

## Deployment Modes & Autonomy Qualification

System deployment modes ([PRODUCT.md](PRODUCT.md)) map directly to qualification stages:

```text
Experimental -> Offline qualified -> Shadow qualified (Advisory Mode)
-> Copilot qualified (Human Approval per Mutation)
-> Bounded-autonomy qualified (Standing Authorization within Expiry & Limit)
-> Suspended/Requalified
```

Requalification is required after material model, prompt, connector, schema, policy, metric, or business-context changes.

## Claim governance

Public claims require a registry entry with claim type, text, evidence, permitted channels/audiences/jurisdictions, owner, approval, disclaimer, and expiry.

## Organizational maturity

Assess separately across strategy, data, customer intelligence, content, search, paid media, experimentation, lifecycle, sales alignment, integrations, governance, finance, reliability, and learning. See [docs/MATURITY_MODEL.md](docs/MATURITY_MODEL.md). Do not assign a single maturity label without dimension-level evidence.
