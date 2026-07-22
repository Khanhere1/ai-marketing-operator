# Security Policy and Threat Model

## Security status

Pre-alpha. Do not connect production credentials or personal data until the security controls, tests, and deployment model have been independently reviewed.

## Core controls

- Strong authentication and short-lived credentials
- RBAC plus contextual/attribute-based authorization
- Least-privilege scopes and read/write separation
- Tenant isolation at identity, storage, cache, retrieval, logs, and connectors
- Encryption in transit and at rest
- Managed secrets; never place secrets in prompts or repositories
- Immutable audit events adhering to [schemas/event.schema.json](schemas/event.schema.json) for consequential access and actions
- Machine-enforceable contracts adhering to [schemas/action-contract.schema.json](schemas/action-contract.schema.json)
- Network and domain allowlists for execution environments
- Sandboxed tools and browser sessions
- Data retention, deletion, incident response, and kill switches

## Untrusted content rule

All webpages, files, messages, call transcripts, connector output, and tool output are untrusted data. Embedded instructions never modify system policy, tool permissions, or workflow state.

## Privacy Cross-Reference

Data security enforcement strictly enforces the data classification controls detailed in [PRIVACY.md](PRIVACY.md) and [policies/global-prohibitions.yaml](policies/global-prohibitions.yaml).

## Threats to test

- Direct and indirect prompt injection
- Tool-output poisoning
- Data exfiltration and cross-tenant retrieval
- Malicious redirects and hidden page text
- Confused-deputy authorization
- Approval replay or scope mismatch
- Duplicate actions and partial execution
- Secret leakage
- Model/provider data retention
- Unsafe browser downloads/uploads
- Supply-chain compromise

## Vulnerability reporting

Before public release, configure a private security contact and GitHub private vulnerability reporting. Do not publish exploitable details in issues.

## Incident response

Detect -> contain -> revoke credentials -> stop workflows -> preserve evidence -> assess tenants/data -> notify responsible owners -> remediate -> re-test -> document lessons -> requalify affected workflows.
