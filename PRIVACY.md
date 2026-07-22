# Privacy and Responsible Marketing

## Principles

- Data minimization
- Purpose limitation
- Consent and preference enforcement
- Least privilege
- Aggregation before person-level processing
- Pseudonymization where appropriate
- Defined retention and deletion
- Tenant isolation
- Transparent model/provider handling
- No discriminatory or deceptive targeting
- Special care for children, sensitive audiences, and sensitive data

## Data classes

1. Public
2. Internal non-sensitive
3. Confidential business/financial
4. Personal data
5. Sensitive or specially restricted

Every model, tool, connector, workflow, and destination declares its permitted maximum class. See [schemas/organization-context.schema.json](schemas/organization-context.schema.json).

## Applicability review

Before person-level marketing activity, establish geography, audience, channel, industry, purpose, data classes, consent/preference status, cross-border processing, profiling, claim type, required notices, and responsible approver. Uncertainty is escalated.

## Technical Security & Prohibitions

For encryption, tenant isolation, and prompt injection protections, see [SECURITY.md](SECURITY.md) and [policies/global-prohibitions.yaml](policies/global-prohibitions.yaml).

## No compliance claims

Controls in this repository do not establish legal compliance. Qualified legal, privacy, security, accessibility, and industry specialists must validate deployments and jurisdiction-specific policy packs.
