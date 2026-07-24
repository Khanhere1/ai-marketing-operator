# AI Marketing Operator 🚀

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Pre--alpha-orange.svg)](#)
[![Schema Validation](https://img.shields.io/badge/Schemas-Draft_2020--12-green.svg)](schemas/)
[![Governance](https://img.shields.io/badge/Governance-Bounded_Autonomy-purple.svg)](GOVERNANCE.md)
[![Agent-Reach Integrated](https://img.shields.io/badge/Intelligence-Agent--Reach_Powered-brightgreen.svg)](connectors/agent_reach_adapter.py)

**An open, vendor-neutral framework and operating system for evidence-driven AI marketing agents.**

`ai-marketing-operator` transforms marketing operations from intuition-based manual execution into a schema-governed, auditable intelligence system. Integrated natively with **[Agent-Reach](connectors/agent-reach)**, it scrapes multi-platform social and market intelligence (Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu) with zero API fees, reconciles platform vanity metrics against true downstream CRM revenue, prepares operator-ready task packages, executes approved bounded workflows via APIs, and preserves qualified organizational learning.

---

## 🌟 Key Capabilities

* **🌐 Multi-Platform Market & Social Intelligence (Agent-Reach Integrated):** Scrapes competitor discussions, brand reactions, product reviews, and Voice of Customer (VoC) sentiment across Twitter/X, Reddit, YouTube, GitHub, Bilibili, and XiaoHongShu without API fees.
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
Planning      Specialists      Retrieval & Intelligence
   \______________|______________/ (Agent-Reach Multi-Platform Scraper)
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

### Integrated Connectors

* **`connectors/agent_reach_adapter.py`**: Python adapter interfacing embedded `connectors/agent-reach/` package into `schemas/definitions.schema.json#/$defs/evidence_item` JSON objects.

---

## ⚡ Quickstart & Usage

### 1. Market Research via Agent-Reach Adapter

```python
from connectors.agent_reach_adapter import AgentReachAdapter

adapter = AgentReachAdapter()
voc_data = adapter.extract_voc_sentiment("B2B SaaS Analytics", platforms=["reddit", "twitter", "youtube"])
print(f"Extracted {len(voc_data)} structured evidence items for intelligence plane.")
```

### 2. Schema Validation

Validate schemas and sample datasets using `ajv-cli` or Python's JSON Schema validator:

```bash
# Validate sample recommendation fixture
npx -y ajv-cli validate -s schemas/recommendation.schema.json -r "schemas/*.schema.json" -d examples/sample-recommendation.json

# Validate sample action contract fixture
npx -y ajv-cli validate -s schemas/action-contract.schema.json -r "schemas/*.schema.json" -d examples/sample-action-contract.json
```

---

## 🤝 Contributing

We welcome contributions! Please review [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md) before submitting pull requests.

---

## 📄 License

Distributed under the **Apache-2.0 License**. See [LICENSE](LICENSE) for details.
