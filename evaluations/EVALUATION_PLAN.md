# Evaluation Plan

## Offline
Golden datasets, historical replay, claim verification, retrieval relevance, marketing reasoning, analytical correctness, tool selection, structured output, security adversarial tests.

## Simulation
Connector failures, stale/conflicting data, prompt injection, approval rejection, budget violation, performance anomaly, interrupted workflow, provider outage, partial writes.

## Shadow mode
Run beside marketers without external actions. Compare quality, speed, cost, errors, evidence, forecasts, decisions, and human revision.

## Controlled production
Limited tenants, workflows, scopes, objects, budgets, and time windows. Use holdouts where appropriate.

## Human benchmark
Same inputs, time horizon, tools, budget, approval constraints, and market conditions for junior, specialist, senior, and system participants. Do not optimize cases to favor AI.

## Release blockers
- Unauthorized-action path
- Cross-tenant data exposure
- Critical policy bypass
- Unsupported consequential claim
- Silent partial failure
- Duplicate external action
- Missing verification for a write
- Regression beyond approved critical threshold
