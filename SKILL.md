---
name: ai-marketing-operator
description: Vendor-neutral, human-governed AI Marketing Operating System with LLM-powered specialist sub-agents, output validation, Agent-Reach integration for multi-platform social/market scraping (Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu), evidence-driven performance analysis, CRM revenue reconciliation, paid media diagnosis, market research, content drafting, and bounded action execution. Activate this skill for all marketing, growth review, competitor analysis, paid media audit, lead quality diagnosis, SEO/AEO/GEO, or marketing operations tasks.
metadata:
  version: "0.3.0"
  author: "AI Marketing Operator Maintainers"
  license: "Apache-2.0"
---

# AI Marketing Operator Skill (v0.3.0)

This skill provides an evidence-driven, schema-governed operating framework for executing marketing activities, campaign diagnoses, paid media optimizations, multi-platform market research, content planning, and executive reporting.

## 🎯 When to Use This Skill

Activate this skill whenever performing:
1. **Multi-Platform Market & Competitor Research:** Real-time competitive intelligence using web search, Agent-Reach scraping (Twitter/X, Reddit, YouTube, GitHub), and URL analysis with mandatory source citations.
2. **Weekly Marketing & Growth Reviews:** Performance audits, anomaly detection, metric trend analysis with CRM reconciliation.
3. **Paid Media Diagnosis:** Auditing Google Ads, Meta Ads, LinkedIn Ads against downstream CRM deals and true contribution margin.
4. **Funnel & Lead Quality Assessment:** Diagnosing form-fill vs sales-acceptance bottlenecks.
5. **Evidence-Backed Content & Creative Briefs:** Generating ad copy, email sequences, ABM playbooks, and landing page briefs with cited evidence.
6. **Action Capability Contracts:** Preparing human-governed transaction packages for campaign changes with preflight checks and single-click rollbacks.

---

## 🏛️ Permanent Operating Principles

* **Evidence-First, Always Cited:** Every factual claim in output MUST include a `[Source: URL]` citation. Outputs below 80% citation density are flagged by the validation layer.
* **Diagnose Before Acting:** Always establish baselines, data-quality scores, and cause-and-effect mechanisms before proposing campaign changes.
* **Separate Concerns:** Explicitly label `[FACT]`, `[INFERENCE]`, and `[ASSUMPTION]` in all analysis outputs.
* **CRM Reconciliation Over Platform Vanity:** Never represent platform-attributed conversions as proven incrementality without CRM cross-check.
* **Bounded Autonomy & Governance:** 4-tier risk classification (`Low`, `Medium`, `High`, `Prohibited`). High-risk actions require explicit human approval.
* **No Silent Fallbacks:** If a data source is unavailable, raise an error — never silently substitute mock data.

---

## 🔌 Integrated Connectors & Adapters

* **Agent-Reach Connector:** `connectors/agent_reach_adapter.py` — Multi-platform social & web scraper. Raises `AgentReachUnavailableError` if CLI is not installed (no silent mocks).
* **Google Ads Connector (Stub):** `connectors/google_ads_connector.py` — Requires API credentials (see docstring).
* **Meta Ads Connector (Stub):** `connectors/meta_ads_connector.py` — Requires API credentials (see docstring).
* **HubSpot Connector (Stub):** `connectors/hubspot_connector.py` — Requires API credentials (see docstring).

---

## ⚙️ Prompt Templates

* **Market Research:** `workflows/prompts/market-research.prompt.md` — Enforces source citations, fact/inference labeling, and ICE scoring methodology.
* **Competitor Analysis:** `workflows/prompts/competitor-analysis.prompt.md` — Enforces product version verification, pricing source validation, and 90-day freshness.
* **Paid Media Review:** `workflows/prompts/paid-media-review.prompt.md` — Enforces CRM reconciliation, causal mechanism requirements, and marginal return analysis.

---

## 📁 Repository & Schema Contracts

* **Shared Definitions:** `schemas/definitions.schema.json`
* **Marketing Recommendation Contract:** `schemas/recommendation.schema.json`
* **Action Capability Contract:** `schemas/action-contract.schema.json`
* **Audit Event Schema:** `schemas/event.schema.json`
* **Organization Context Pack:** `schemas/organization-context.schema.json`
* **Metric Registry:** `schemas/metric-registry.schema.json`
* **Data Quality Assessment:** `schemas/data-quality.schema.json`

## ⚙️ Workflows

* **Weekly Growth Review:** `workflows/weekly-growth-review.yaml`
* **Paid Media Review:** `workflows/paid-media-review.yaml`
* **Global Prohibitions Policy:** `policies/global-prohibitions.yaml`

---

## ✅ Output Validation Layer

All specialist outputs pass through `graph_engine/validators/output_validator.py` before delivery:

1. **Citation Density Check** — Rejects outputs where <80% of factual claims lack `[Source: URL]` citations
2. **Data Freshness Check** — Flags references to outdated product versions or stale data (>90 days)
3. **Policy Compliance Check** — Detects unverified causal claims, absolute guarantee language, and platform metric misrepresentation
4. **Content Substance Check** — Catches placeholder patterns, template variables, and insufficient output length

---

## 🚀 Standard Execution Pipeline

```text
1. Market Intelligence & VoC Extraction (Agent-Reach → connectors/agent_reach_adapter.py)
2. Data Ingestion & Quality Gate (schemas/data-quality.schema.json)
3. Specialist Analysis (LLM-powered sub-agents with prompt templates):
   a. SEO & Organic Search → workflows/prompts/market-research.prompt.md
   b. Paid Media & Performance → workflows/prompts/paid-media-review.prompt.md
   c. Content Strategy & ABM → workflows/prompts/market-research.prompt.md
   d. Analyst Reviewer & Synthesis → Cross-specialist coherence check
4. Output Validation Gate (graph_engine/validators/output_validator.py)
5. Assurance Review (policies/global-prohibitions.yaml & Brand Claims)
6. Action Contract Generation (schemas/action-contract.schema.json)
7. Human Approval Gate
8. Execution, Read-Back Verification & Audit Logging (schemas/event.schema.json)
```

## 🔑 LLM Configuration

Sub-agents support OpenAI, Anthropic, and Google AI. Set one of these environment variables:

```bash
# Option 1: OpenAI
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-4o"  # optional, defaults to gpt-4o

# Option 2: Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
export ANTHROPIC_MODEL="claude-sonnet-4-20250514"  # optional

# Option 3: Google AI
export GOOGLE_API_KEY="AIza..."
export GOOGLE_MODEL="gemini-2.0-flash"  # optional
```

If no API key is configured, sub-agents generate **prompt packages** for the Antigravity agent to execute using its built-in web search and URL reading capabilities.
