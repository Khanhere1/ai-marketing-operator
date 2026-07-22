# Contributing

## Before proposing a feature

Describe the business objective, user, evidence, workflow state changes, data required, privacy implications, risk class (per [GOVERNANCE.md](GOVERNANCE.md)), permissions, approval behavior, failure modes, rollback, metrics, tests, and non-goals.

## Pull-request requirements

- Versioned schemas and migrations where applicable
- Local schema validation using `ajv-cli` or `python-jsonschema` (see [examples/README.md](examples/README.md))
- Tests for valid/invalid inputs
- Policy and permission tests
- Tenant-isolation tests for data-bearing changes
- Prompt-injection tests for retrieval/tool changes
- Cost/latency impact
- Documentation and changelog
- No secrets, production data, or unlicensed assets

## New write capability checklist

A write capability must include:

- Formal action contract adhering to [schemas/action-contract.schema.json](schemas/action-contract.schema.json)
- Least-privilege permission list
- Preflight and dry-run behavior
- Approval policy
- Idempotency protection
- Read-back verification
- Partial-failure handling
- Rollback or compensation action
- Audit events adhering to [schemas/event.schema.json](schemas/event.schema.json)
- Rate-limit behavior
- Sandbox fixture
- Security and adversarial tests

## Schema Validation Command

Before submitting a PR containing schema or fixture changes:

```bash
npx -y ajv-cli validate -s schemas/recommendation.schema.json -r "schemas/*.schema.json" -d examples/sample-recommendation.json
npx -y ajv-cli validate -s schemas/action-contract.schema.json -r "schemas/*.schema.json" -d examples/sample-action-contract.json
npx -y ajv-cli validate -s schemas/event.schema.json -r "schemas/*.schema.json" -d examples/sample-event-sequence.json
npx -y ajv-cli validate -s schemas/organization-context.schema.json -r "schemas/*.schema.json" -d examples/sample-organization-context.json
```

## Development workflow

1. Open or select an issue.
2. Write an architecture decision record for consequential changes.
3. Implement the smallest testable slice.
4. Run tests and evaluation suites.
5. Submit a PR with risk and migration notes.
6. Obtain code, domain, and security review as applicable.
