# Product Requirements

## Vision

Create an evidence-driven AI Marketing Operator that helps organizations understand performance, decide what to do, coordinate implementation, execute approved bounded actions, and learn from observed outcomes.

## Non-goals

- Guaranteed ROI, profitability, rankings, citations, or competitive superiority
- Universal replacement of marketers, legal counsel, privacy experts, security specialists, statisticians, or finance owners
- Unrestricted account access or browser control
- Autonomous material spend, public claims, customer-data exports, regulated communications, or irreversible changes
- “One prompt” marketing automation

## Core jobs to be done

1. Establish reliable organizational context and metric definitions.
2. Diagnose marketing and revenue constraints.
3. Link recommendations to evidence and a plausible mechanism.
4. Produce short and long execution sequences with owners and completion criteria.
5. Prepare and, where qualified, perform authorized actions.
6. Verify results and preserve only qualified learning.

## Output contract

Every major recommendation (see [schemas/recommendation.schema.json](schemas/recommendation.schema.json)) includes:

- Business objective and baseline
- Evidence and data-quality assessment
- Assumptions and unresolved questions
- Diagnosis and alternatives considered
- Proposed action and expected mechanism
- Expected outcome range and confidence
- Cost, opportunity cost, dependencies, and risks
- Guardrail metrics and measurement plan
- Approval requirement and rollback guidance
- Immediate task sequence and long-term sequence
- Next review point

## Capability packs

### Core control plane
Context, identity, permissions, policy, approvals, workflow state, evidence, audit, observability, cost controls, model routing, memory qualification.

### Intelligence
Market/competitor research, customer and VoC, strategy, analytics, attribution limitations, incrementality planning, forecasting, anomaly detection.

### Execution planning
Paid media, SEO/AEO/GEO, content, social, lifecycle/CRM, CRO, experimentation, reporting.

### Assurance
Evidence/fact checking, brand review, privacy/policy review, accessibility, security, red-team review.

## Deployment modes

- **Advisory:** read-only analysis and recommendations (maps to *Shadow qualified* stage in [GOVERNANCE.md](GOVERNANCE.md)).
- **Copilot:** prepares drafts/change sets; human approves every mutation (*Copilot qualified*).
- **Bounded autonomy:** executes reversible actions inside standing authorization (*Bounded-autonomy qualified*).
- **Advanced autonomy:** only for individually qualified workflows with monitoring, expiry, rollback, and emergency controls (*Bounded-autonomy qualified* with elevated thresholds).

## Initial ICP

Prioritize organizations with multiple active channels, a CRM or transaction system, recurring performance reviews, material marketing spend, fragmented reporting, and the ability to implement recommendations. Agencies are a strong secondary ICP because workflows repeat across accounts, but tenant and client isolation are mandatory.

## Success model

Measure four layers:

1. Business: incremental contribution, qualified pipeline, CAC, payback, retention.
2. Execution: insight-to-launch time, valid experiment rate, rework, cycle time, usable-asset cost.
3. Quality: factual accuracy, evidence coverage, brand adherence, compliance, rejection rate.
4. System: task success, tool success, recovery, unauthorized attempts, cost and latency.

Every metric requires definition via [schemas/metric-registry.schema.json](schemas/metric-registry.schema.json).
