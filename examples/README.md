# Synthetic Example Fixtures

This directory contains validated, synthetic sample datasets demonstrating machine-readable contracts.

## Contents

* `sample-organization-context.json` — Organization Context Pack for a fictional B2B SaaS company ("Acme Analytics").
* `sample-recommendation.json` — Validated Paid-Media recommendation resolving ROAS vs CRM lead quality discrepancy.
* `sample-action-contract.json` — Action capability contract for `pause_ad_groups` with preflight checks and rollback.
* `sample-event-sequence.json` — Complete sequence of audit events tracking recommendation and action lifecycle.

## Schema Validation

Validate all fixtures locally using `ajv-cli` or `python-jsonschema`:

```bash
npx -y ajv-cli validate -s ../schemas/recommendation.schema.json -r "../schemas/*.schema.json" -d sample-recommendation.json
npx -y ajv-cli validate -s ../schemas/action-contract.schema.json -r "../schemas/*.schema.json" -d sample-action-contract.json
npx -y ajv-cli validate -s ../schemas/event.schema.json -r "../schemas/*.schema.json" -d sample-event-sequence.json
npx -y ajv-cli validate -s ../schemas/organization-context.schema.json -r "../schemas/*.schema.json" -d sample-organization-context.json
```
