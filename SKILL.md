---
name: ai-marketing-operator
description: Free-first AI Marketing Operating System that uses built-in agent tools (search_web, read_url_content, ego-browser) and free public APIs (Reddit, Hacker News, GitHub, Google Trends, Meta Ad Library, Google Ads Transparency) for real-time competitive intelligence, market research, paid media analysis, VoC extraction, ABM sequences, and content strategy. No paid API keys required. Activate this skill for ALL marketing, growth, competitor analysis, ad research, or marketing operations tasks.
metadata:
  version: "0.4.0"
  author: "AI Marketing Operator Maintainers"
  license: "Apache-2.0"
---

# AI Marketing Operator Skill (v0.4.0 — Free-First)

Evidence-driven marketing intelligence using **FREE tools only**. No paid API keys required.

---

## 🎯 When to Use This Skill

Activate for ANY marketing task including:
- Market research & competitor intelligence
- Ad library research (Google Ads Transparency, Meta Ad Library)
- VoC extraction (Reddit, G2, Capterra, Hacker News, Product Hunt)
- Paid media diagnosis & campaign planning
- SEO/AEO/GEO keyword strategy
- ABM outbound sequences & email nurturing
- Content strategy & landing page briefs
- Weekly growth reviews & performance audits

---

## 🔧 How This Skill Works (Free-First)

This skill does NOT require paid APIs. It uses a tiered research approach:

### Tier 1: Built-in Agent Tools (Always Available)
Use these tools for every research task:

- **`search_web`** — Search Google for competitor data, pricing, product info, industry benchmarks, market trends
- **`read_url_content`** — Read official pricing pages, product pages, press releases, blog posts to verify claims
- **`ego-browser`** — Visit JavaScript-heavy pages like Meta Ad Library, Google Ads Transparency Center, Google Trends, review platforms

### Tier 2: Free Public API Connector (`connectors/free_research_tools.py`)
The graph engine automatically queries these free APIs:

| Source | API | What It Provides | Auth? |
|--------|-----|-------------------|-------|
| Reddit | `reddit.com/search.json` | VoC, competitor discussions, pain points | ❌ None |
| Hacker News | `hn.algolia.com/api` | Tech industry sentiment, product launches | ❌ None |
| GitHub | `api.github.com/search` | Open source landscape, developer tools | ❌ None |
| Google Trends | RSS feed | Trending search topics, keyword interest | ❌ None |

### Tier 3: Browser-Accessible Sources (via ego-browser or read_url_content)

| Source | URL Pattern | What It Provides |
|--------|------------|-------------------|
| **Google Ads Transparency** | `adstransparency.google.com/?query=COMPANY` | Active ad creatives, messaging |
| **Meta Ad Library** | `facebook.com/ads/library/?q=COMPANY` | Facebook/Instagram ad creatives |
| **Google Trends** | `trends.google.com/trends/explore?q=KEYWORD` | Keyword interest over time |
| **G2 Reviews** | `g2.com/search?query=PRODUCT` | Customer reviews, ratings, complaints |
| **Capterra** | `capterra.com/search/?query=PRODUCT` | Software comparisons, reviews |
| **TrustPilot** | `trustpilot.com/search?query=COMPANY` | Customer trust scores, feedback |
| **Product Hunt** | `producthunt.com/search?q=PRODUCT` | Product launches, upvotes |
| **AlternativeTo** | `alternativeto.net/browse/search/?q=PRODUCT` | Competitor alternatives |

### Tier 4: Paid LLM APIs (Optional Enhancement)
If API keys are set, sub-agents use them for synthesis. NOT required.

```bash
# OPTIONAL — system works fully without these
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
```

---

## 🏛️ Operating Principles

1. **Evidence-First, Always Cited**: Every claim MUST include `[Source: URL]`. Use `search_web` to find real URLs.
2. **Verify Before Stating**: Use `read_url_content` on official websites to verify product names, versions, pricing.
3. **Label Everything**: Mark claims as `[FACT]` (verified URL), `[INFERENCE]` (deduction), or `[ASSUMPTION]`.
4. **No Silent Fallbacks**: If a data source fails, say so. Never substitute fake data.
5. **CRM Over Platform Vanity**: Never present ad platform metrics as proven revenue.
6. **Browser for Ad Research**: Use `ego-browser` for Meta Ad Library and Google Ads Transparency.

---

## 📋 Standard Research Workflow

When the user asks for market research, competitor analysis, or any marketing task:

```
Step 1: SEARCH — Use search_web to find current data about the company/competitors
Step 2: VERIFY — Use read_url_content on official websites to confirm product details, pricing
Step 3: GATHER VOC — Search Reddit, G2, HN for customer sentiment (free_research_tools handles this)
Step 4: AD RESEARCH — Use ego-browser to visit Meta Ad Library and Google Ads Transparency
Step 5: ANALYZE — Synthesize evidence into structured output following prompt templates
Step 6: VALIDATE — Check citation density (>80%), flag stale data, policy compliance
Step 7: DELIVER — Present findings with clear [Source: URL] citations
```

---

## 📁 Key Files

### Prompt Templates (enforce citation rules)
- `workflows/prompts/market-research.prompt.md` — Market research & VoC
- `workflows/prompts/competitor-analysis.prompt.md` — Competitive intelligence
- `workflows/prompts/paid-media-review.prompt.md` — Paid media & CRM reconciliation

### Free Research Connector
- `connectors/free_research_tools.py` — Reddit, HN, GitHub, Google Trends, ad library URL generators

### Validation Layer
- `graph_engine/validators/output_validator.py` — Citation density, freshness, policy compliance

### Schema Contracts
- `schemas/recommendation.schema.json` — Marketing recommendation structure
- `schemas/organization-context.schema.json` — Company context
- `schemas/data-quality.schema.json` — Data quality assessment

### Workflows
- `workflows/paid-media-review.yaml` — Paid media audit workflow
- `workflows/weekly-growth-review.yaml` — Weekly growth review

### Policies
- `policies/global-prohibitions.yaml` — 11 prohibited actions (no fabrication, no deception, etc.)

---

## 🚀 Execution Pipeline

```text
1. Free API Research (Reddit, HN, GitHub → connectors/free_research_tools.py)
2. Browser Research (Ad Libraries, Review Sites → ego-browser / read_url_content)
3. Web Search Verification (search_web → official sources)
4. Specialist Analysis:
   a. SEO & Organic Search → Keywords, AEO/GEO, competitor rankings
   b. Paid Media → Ad library research, channel strategy, budget framework
   c. Content Strategy → VoC-driven ABM, content calendar, landing pages
   d. Analyst Review → Cross-specialist synthesis, quality audit
5. Output Validation (graph_engine/validators/output_validator.py)
6. Human Review Gate
```

---

## 💡 Example Usage

### Market Research
> "Research the competitive landscape for [Company] in [Industry]"
→ Agent uses search_web + free APIs + read_url_content to gather real data

### Ad Library Research
> "What ads are [Competitor] running on Google and Meta?"
→ Agent uses ego-browser to visit Google Ads Transparency + Meta Ad Library

### VoC Extraction
> "What are customers saying about [Product] on Reddit and G2?"
→ Agent uses free_research_tools.search_reddit() + ego-browser for G2

### Paid Media Audit
> "Audit our Google Ads performance and suggest optimizations"
→ Agent follows paid-media-review.prompt.md with CRM reconciliation rules

### ABM Sequence
> "Create a 5-touch outbound sequence for [Target Persona]"
→ Agent uses VoC evidence from free APIs to craft evidence-backed messaging
