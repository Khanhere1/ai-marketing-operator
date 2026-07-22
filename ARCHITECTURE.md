# Architecture

## Architectural rule

**Agents propose and perform bounded tasks. Workflows own state. Policies own permissions. Humans own consequential decisions.**

## Logical architecture

```text
User / API / Event / Schedule
            |
            v
Identity, Intent and Permission Gateway
            |
            v
Objective Router and Workflow Registry
            |
            v
Deterministic Workflow State Machine
   |              |              |
Planning      Specialists      Retrieval
   \______________|______________/
                  v
       Evidence and Artifact Store
                  v
      Assurance and Policy Gates
                  v
        Human Approval Service
                  v
       Sandboxed Execution Gateway
                  v
       Verification and Monitoring
                  v
      Decision Ledger and Learning
```

## Planes

### Control plane
Orchestrator, workflow engine, policy engine, approval service, identity/authorization, budget limits, action registry, reliability manager.

### Intelligence plane
Context/data-quality, market and customer intelligence, strategy, measurement/analytics, experimentation.

### Domain plane
Paid media, SEO/AEO/GEO, content/social, lifecycle/CRM, CRO, executive reporting.

### Assurance plane
Evidence, brand, policy/privacy, accessibility, statistical review, security critic.

### Memory plane
Active workflow state, organization profile, approved claims, source evidence, decisions, experiments, campaigns, performance, and qualified learning.

## Interfaces

Use stable internal capability contracts. Runtime adapters may use REST, GraphQL, database access, files, official SDKs, MCP, or constrained browser automation.

```text
Workflow -> Capability Contract -> Policy Gateway -> Adapter -> External System
```

### Tool priority

1. Official API
2. Approved native integration
3. Approved MCP adapter
4. Deterministic browser automation
5. Visual computer-use fallback
6. Human task when safe automation is unavailable

Browser automation must never circumvent access restrictions or platform controls.

## Agent protocol

Every invocation includes organization ID, workflow/version, agent role, requesting identity, permission context, input references, policy versions, cost/time limit, correlation ID, and idempotency key. Every output validates against a versioned schema.

## Action lifecycle

```text
Propose -> Preflight -> Policy check -> Permission check -> Dry run
-> Approval -> Execute -> Read back -> Compare -> Monitor
-> Roll back/escalate -> Audit -> Learning review
```

## Conflict resolution

1. Verified organization ground truth
2. Applicable mandatory policy
3. Approved organization policy
4. Higher-authority and fresher evidence
5. Data-quality and methodological review
6. Human decision owner

Agents cannot vote to override policy.

## Resumption and duplicate prevention

- Persist state after each material transition.
- Store immutable event history and current materialized state.
- Require idempotency keys for external actions.
- Check target state before retrying.
- Use compensation actions for reversible mutations.
- Escalate ambiguous partial failures.

## Repository target

```text
/core /agents /packs /workflows /schemas /connectors /memory
/prompts /policies /evaluations /tests /runtime /deployment
/security /observability /examples /docs
```
