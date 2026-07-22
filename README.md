# AI Marketing Operator 🚀

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Pre--alpha-orange.svg)](#)
[![Schema Validation](https://img.shields.io/badge/Schemas-Draft_2020--12-green.svg)](schemas/)
[![Governance](https://img.shields.io/badge/Governance-Bounded_Autonomy-purple.svg)](GOVERNANCE.md)

**An open, vendor-neutral framework and operating system for evidence-driven AI marketing agents.**

`ai-marketing-operator` transforms marketing operations from intuition-based manual execution into a schema-governed, auditable intelligence system. It analyzes performance, reconciles platform vanity metrics against true downstream CRM revenue, prepares operator-ready task packages, executes approved bounded workflows via APIs, and preserves qualified organizational learning.

---

## 🌟 Key Capabilities

* **📊 Multi-Channel Paid Media Diagnosis:** Reconciles platform-attributed metrics (e.g. Google/Meta ROAS) against CRM deals, gross margin assumptions, and sales acceptance rates.
* **🛡️ Governed Human-in-the-Loop Autonomy:** Enforces 4 decision risk tiers (`Low`, `Medium`, `High`, `Prohibited`) with mandatory human transaction approvals for budget/spending changes.
* **📜 Immutable Action Contracts:** Guarantees idempotency, dry-run validation, read-back verification, preflight checks, and single-click rollbacks for all external mutations.
* **🛡️ Defense in Depth Security:** Treats all web pages, tool outputs, and CSV uploads as untrusted data, preventing prompt injection passthrough and cross-tenant data leakage.
* **🧠 Persistent Memory & Learning Layer:** Maintains ground-truth context packs, approved claim registries, decision ledgers, and experiment memory across all daily tasks.

---

## 🏛️ Architecture & Logical Planes

```text
User / API / Event / Schedule
            │
            ▼
Identity, Intent & Permission Gateway (RBAC / ABAC)
            │
            ▼
Deterministic Workflow State Machine
   │              │              │
Planning      Specialists      Retrieval
   \______________|______________/
                  │
                  ▼
       Evidence & Artifact Store
                  │
                  ▼
      Assurance & Policy Gates (Prohibitions / Claims)
                  │
                  ▼
        Human Approval Service (Action Contracts)
                  │
                  ▼
       Sandboxed Execution Gateway (APIs / MCP / Web)
                  │
                  ▼
      Decision Ledger & Memory Plane (Learning Loop)
```

### The 6 Logical Planes

1. **Control Plane:** Workflow engine, policy engine, approval gateway, budget management, action registry.
2. **Intelligence Plane:** Market research, VoC, competitive benchmarking, attribution reconciliation, anomaly detection.
3. **Domain Plane:** Paid Media, SEO/AEO/GEO, Content/Social, Lifecycle/CRM, CRO, Executive Reporting.
4. **Assurance Plane:** Fact-checking critic, brand adherence review, privacy auditor, security critic.
5. **Memory Plane:** Active state, organization context pack, claims registry, decision ledger, campaign learnings.
6. **Execution Gateway:** Official APIs, native integrations, MCP adapters, deterministic browser automation.

---

## 📦 Repository Structure

```text
ai-marketing-operator/
├── ARCHITECTURE.md                 # 5-plane system architecture & execution lifecycle
├── CHANGELOG.md                    # Release history & versioning
├── CODE_OF_CONDUCT.md              # Community code of conduct
├── CONTRIBUTING.md                 # Developer & schema contribution guidelines
├── GOVERNANCE.md                   # Risk classification matrix & approval principles
├── LICENSE                         # Apache 2.0 open-source license
├── PRIVACY.md                      # 5-tier data classification & privacy controls
├── PRODUCT.md                      # Core vision, non-goals, & 4-layer success model
├── README.md                       # Main repository overview & quickstart
├── ROADMAP.md                      # Phase 0 to Phase 5 implementation roadmap
├── SECURITY.md                     # Security policy, threat model, & untrusted data rules
├── .github/
│   ├── CODEOWNERS                  # Directory maintainer ownership mapping
│   ├── pull_request_template.md    # PR review & risk checklist
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md           # Schema & workflow bug reporting template
│       ├── config.yml              # Issue chooser configuration
│       └── feature_request.md      # Feature request proposal template
├── docs/
│   ├── GITHUB_LAUNCH_CHECKLIST.md  # Launch hygiene & security checklist
│   ├── MATURITY_MODEL.md           # 5-stage AI Marketing Maturity Model
│   ├── PAID_MEDIA_PLAYBOOK.md      # Paid media diagnostic & operator playbook
│   └── WORKFLOW_TEMPLATE.md        # Standardized workflow specification template
├── evaluations/
│   ├── EVALUATION_PLAN.md          # Offline, simulation, & shadow evaluation strategy
│   └── golden-cases/               # Ground-truth evaluation benchmarks
│       ├── README.md
│       └── 001-high-roas-poor-lead-quality.md
├── examples/                       # Machine-readable JSON fixtures & sample datasets
│   ├── README.md
│   ├── sample-action-contract.json
│   ├── sample-event-sequence.json
│   ├── sample-organization-context.json
│   └── sample-recommendation.json
├── policies/
│   └── global-prohibitions.yaml    # Machine-readable prohibition rules
├── schemas/                        # Machine-readable JSON Schema Draft 2020-12 contracts
│   ├── action-contract.schema.json
│   ├── data-quality.schema.json
│   ├── definitions.schema.json
│   ├── event.schema.json
│   ├── metric-registry.schema.json
│   ├── organization-context.schema.json
│   └── recommendation.schema.json
└── workflows/                      # Declarative YAML workflow state machine definitions
    ├── paid-media-review.yaml
    └── weekly-growth-review.yaml
```

---

## ⚡ Quickstart & Usage

### 1. Schema Validation

Validate schemas and sample datasets using `ajv-cli` or Python's JSON Schema validator:

```bash
# Validate sample recommendation fixture
npx -y ajv-cli validate -s schemas/recommendation.schema.json -r "schemas/*.schema.json" -d examples/sample-recommendation.json

# Validate sample action contract fixture
npx -y ajv-cli validate -s schemas/action-contract.schema.json -r "schemas/*.schema.json" -d examples/sample-action-contract.json
```

### 2. Standard Advisory Execution Lifecycle

```text
CSV Ingestion ──► Data Quality Gate ──► Diagnosis ──► Recommendation Assembly ──► Human Review ──► Execution Contract
```

1. **Ingest Data:** Upload CSV exports or connect read-only platform adapters (Google Ads, Meta, HubSpot).
2. **Data Quality Gate:** System checks completeness, staleness, and consistency against `data-quality.schema.json`.
3. **Diagnosis & Reconciliation:** System cross-checks platform-reported metrics against downstream CRM revenue.
4. **Recommendation Assembly:** Generates evidence-backed recommendations adhering to `recommendation.schema.json`.
5. **Human Approval:** High-risk actions output an immutable `action-contract.schema.json` package for human sign-off.
6. **Execution & Audit:** System executes approved actions, reads back state, and logs immutable audit events (`event.schema.json`).

---

## 🔒 Security & Governance Principles

* **Untrusted Content Rule:** All web pages, uploaded files, and external API responses are treated as untrusted data. Embedded instructions can never alter workflow state or system permissions.
* **Separation of Duties:** Proposer, Approver, Executor, and Verifier roles are strictly separated for medium and high-risk actions.
* **Fail-Closed Posture:** Any ambiguity in policy, authorization, or metric definitions causes the system to degrade safely and request human clarification.

---

## 🤝 Contributing

We welcome contributions! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md) before submitting pull requests.

1. Fork the repository and create your feature branch (`git checkout -b feature/amazing-feature`).
2. Run schema and validation checks locally.
3. Submit a Pull Request following the [PR Template](.github/pull_request_template.md).

---

## 📄 License

Distributed under the **Apache-2.0 License**. See [LICENSE](LICENSE) for details.
