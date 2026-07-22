# Workflow Specification Template

## Identity
- Workflow ID/version
- Owner
- Risk class
- Eligible deployment modes

## Trigger and objective
- Trigger
- Business objective
- Primary metric
- Guardrails

## Preconditions
- Context
- Data freshness/quality
- Permissions
- Policy applicability

## Inputs and artifacts
- Required inputs
- Optional inputs
- Produced structured artifacts

## States
Describe deterministic states and permitted transitions.

## Agents and tools
List role, responsibility, access, and non-responsibility.

## Sequence
Identify parallel work, sequential work, review gates, approval gates, and checkpoints.

## Failures
Timeout, rate limit, partial results, invalid schema, stale data, low confidence, authorization failure, connector failure, policy conflict.

## External actions
Action contract, dry run, idempotency, approval, verification, monitoring, rollback.

## Completion
Completion criteria, metrics, audit events, review point, memory proposal.

## Examples
Provide testable example input and expected structured output.
