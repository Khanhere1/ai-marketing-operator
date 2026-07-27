"""
Specialist Sub-Agent Nodes for LangGraph Graph Engineering Loop.

v0.4.0 — FREE-FIRST EXECUTION MODEL

These nodes gather REAL data using free public APIs and browser-accessible
sources. No paid API keys required.

Research priority order:
  1. Free public APIs (Reddit, Hacker News, GitHub — via free_research_tools.py)
  2. Antigravity agent's built-in tools (search_web, read_url_content)
  3. ego-browser for JS-heavy pages (Meta Ad Library, Google Ads Transparency)
  4. Paid LLM APIs (OpenAI, Anthropic, Google) — ONLY if explicitly configured

Each specialist node:
  1. Calls free_research_tools to gather real evidence from public APIs
  2. Loads the relevant prompt template from workflows/prompts/
  3. Synthesizes the gathered evidence into structured analysis
  4. If an LLM API key is available, uses it for synthesis
  5. If no LLM key, outputs the raw evidence + structured research brief
     for the Antigravity agent to synthesize using its own capabilities
"""

import os
import json
import logging
import importlib.util
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..state import GraphState, SubAgentOutput, TaskItem

logger = logging.getLogger(__name__)

# Base directory for prompt templates
PROMPTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "workflows", "prompts"
)

# Import free research tools
_free_tools = None
try:
    _tools_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "connectors", "free_research_tools.py"
    )
    spec = importlib.util.spec_from_file_location("free_research_tools", _tools_path)
    _free_tools = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_free_tools)
    logger.info("Free research tools loaded successfully")
except Exception as e:
    logger.warning("Could not load free research tools: %s", str(e))


def _load_prompt_template(filename: str) -> str:
    """Load a prompt template from the workflows/prompts/ directory."""
    filepath = os.path.join(PROMPTS_DIR, filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("Prompt template not found: %s", filepath)
        return ""


def _get_llm_client():
    """
    Attempt to initialize an LLM client. Returns None if no API key configured.
    This is OPTIONAL — the system works fully without it using free tools.
    """
    # Try OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            return {"provider": "openai", "client": openai.OpenAI(api_key=openai_key)}
        except ImportError:
            pass

    # Try Anthropic
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            import anthropic
            return {"provider": "anthropic", "client": anthropic.Anthropic(api_key=anthropic_key)}
        except ImportError:
            pass

    # Try Google AI
    google_key = os.environ.get("GOOGLE_API_KEY")
    if google_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=google_key)
            return {"provider": "google", "client": genai}
        except ImportError:
            pass

    return None


def _call_llm(system_prompt: str, user_prompt: str, llm_client: Optional[Dict] = None) -> Optional[str]:
    """
    Call an LLM with the given prompts. Returns None if no LLM is available.
    The caller should handle None by using the raw evidence directly.
    """
    if llm_client is None:
        llm_client = _get_llm_client()

    if llm_client is None:
        return None

    provider = llm_client["provider"]
    client = llm_client["client"]

    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=4096,
            )
            return response.choices[0].message.content

        elif provider == "anthropic":
            response = client.messages.create(
                model=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=0.3,
                max_tokens=4096,
            )
            return response.content[0].text

        elif provider == "google":
            model = client.GenerativeModel(
                os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash")
            )
            response = model.generate_content(
                f"{system_prompt}\n\n---\n\n{user_prompt}",
                generation_config={"temperature": 0.3, "max_output_tokens": 4096},
            )
            return response.text

    except Exception as e:
        logger.error("LLM call failed (%s): %s", provider, str(e))
        return None


def _gather_evidence(query: str, company_name: str) -> Dict[str, Any]:
    """
    Gather real evidence using free public APIs.
    Returns a dict with evidence_items and browser_research_urls.
    """
    if _free_tools is None:
        return {
            "evidence_items": [],
            "browser_research_urls": {},
            "errors": ["Free research tools module not available"],
        }

    try:
        return _free_tools.gather_free_intelligence(
            query=query,
            company_name=company_name,
            platforms=["reddit", "hackernews", "github"],
        )
    except Exception as e:
        logger.error("Free intelligence gathering failed: %s", str(e))
        return {
            "evidence_items": [],
            "browser_research_urls": {},
            "errors": [str(e)],
        }


def _format_evidence_section(evidence: Dict[str, Any]) -> str:
    """Format gathered evidence into a readable markdown section."""
    lines = ["## 📊 Real Evidence Gathered (Free Public APIs)\n"]

    items = evidence.get("evidence_items", [])
    if items:
        lines.append(f"**{len(items)} evidence items found** across "
                      f"{len(set(i.get('source', '') for i in items))} platforms.\n")

        # Group by source
        by_source = {}
        for item in items:
            src = item.get("source", "Unknown")
            by_source.setdefault(src, []).append(item)

        for source, src_items in by_source.items():
            lines.append(f"\n### {source} ({len(src_items)} results)\n")
            for item in src_items[:5]:
                title = item.get("title", "Untitled")
                url = item.get("source_url", "")
                score = item.get("score", item.get("points", ""))
                lines.append(f"- **{title}**")
                if url:
                    lines.append(f"  [Source: {url}]")
                if score:
                    lines.append(f"  Score/Points: {score}")
                text = item.get("text", item.get("description", ""))
                if text:
                    lines.append(f"  > {text[:200]}")
                lines.append("")
    else:
        lines.append("⚠️ No evidence items gathered from free APIs.\n")

    # Browser research URLs
    urls = evidence.get("browser_research_urls", {})
    if urls:
        lines.append("\n### 🌐 Browser Research URLs (for deeper investigation)\n")
        lines.append("Use `search_web`, `read_url_content`, or `ego-browser` to visit:\n")
        for name, url in urls.items():
            lines.append(f"- **{name}**: {url}")
        lines.append("")

    # Errors
    errors = evidence.get("errors", [])
    if errors:
        lines.append("\n### ⚠️ Research Errors\n")
        for err in errors:
            lines.append(f"- {err}")
        lines.append("")

    return "\n".join(lines)


def _build_context_block(state: GraphState) -> str:
    """Build a context block from the current graph state."""
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    iteration = state.get("iteration_count", 1)
    feedback = state.get("evaluator_feedback")

    context = (
        f"**Company**: {company_name}\n"
        f"**Objective**: {objective}\n"
        f"**Current Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n"
        f"**Iteration**: {iteration}\n"
    )

    if feedback:
        context += f"\n**Previous Feedback (address this)**: {feedback}\n"

    return context


def _build_agent_research_brief(
    specialist: str,
    company_name: str,
    objective: str,
    evidence: Dict[str, Any],
    analysis_request: str,
    prompt_template: str,
) -> str:
    """
    Build a complete research brief that the Antigravity agent can execute
    using its built-in tools (search_web, read_url_content, ego-browser).

    This is the FREE execution path — no paid LLM APIs needed.
    """
    evidence_section = _format_evidence_section(evidence)

    return (
        f"# {company_name} — {specialist.replace('_', ' ').title()} Analysis\n\n"
        f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
        f"**Mode**: Free Research (no paid API keys)\n\n"
        f"---\n\n"
        f"{evidence_section}\n\n"
        f"---\n\n"
        f"## 🔍 Analysis Request for Antigravity Agent\n\n"
        f"Use your built-in tools to complete this analysis:\n\n"
        f"1. **`search_web`** — Search for current {company_name} pricing, "
        f"product pages, and competitor comparisons\n"
        f"2. **`read_url_content`** — Read the official websites and verify "
        f"product names, versions, and pricing\n"
        f"3. **`ego-browser`** — Visit the Ad Library and Transparency Center "
        f"URLs listed above to research competitor ads\n\n"
        f"### Specific Research Tasks\n\n"
        f"{analysis_request}\n\n"
        f"### Prompt Template Instructions\n\n"
        f"Follow these rules when producing the final analysis:\n\n"
        f"{prompt_template[:2000] if prompt_template else 'No prompt template loaded.'}\n"
    )


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: SEO & Organic Search
# ─────────────────────────────────────────────────────────────────────

def seo_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    SEO & Organic Search Specialist Sub-Agent Node.
    Gathers real search data from free APIs, then analyzes.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[SEO Specialist] Gathering real search data for {company_name}")

    # 1. Gather real evidence from free APIs
    evidence = _gather_evidence(f"{company_name} SEO keywords organic search", company_name)
    logs.append(f"[SEO Specialist] Gathered {len(evidence.get('evidence_items', []))} evidence items")

    # 2. Load prompt template
    prompt_template = _load_prompt_template("market-research.prompt.md")

    # 3. Build analysis request
    analysis_request = (
        f"1. **Keyword Research**: Search for '{company_name}' + related terms. "
        f"Identify 5-8 high-intent keyword clusters from real search data.\n"
        f"2. **Competitor Search Positioning**: Which competitors rank for "
        f"'{company_name}' keywords? Use search_web to check.\n"
        f"3. **AEO/GEO Strategy**: How should {company_name} optimize for "
        f"AI-powered search (Perplexity, Google AI Overviews)?\n"
        f"4. **Quick Wins**: 3-5 tactical SEO actions based on real data.\n\n"
        f"Include [Source: URL] for every factual claim."
    )

    # 4. Try LLM synthesis if available, otherwise output research brief
    context = _build_context_block(state)
    evidence_text = _format_evidence_section(evidence)

    llm_result = _call_llm(
        system_prompt=prompt_template or "You are a senior SEO strategist. Cite all sources.",
        user_prompt=f"{context}\n\n{evidence_text}\n\nAnalyze this evidence and produce:\n{analysis_request}",
    )

    if llm_result:
        content = llm_result
        data_source = "free_apis_plus_llm"
    else:
        content = _build_agent_research_brief(
            "seo_specialist", company_name, objective,
            evidence, analysis_request, prompt_template,
        )
        data_source = "free_apis_plus_agent_brief"

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_seo_1",
        "specialist": "seo",
        "title": f"{company_name} SEO & Organic Search Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "evidence_items_count": len(evidence.get("evidence_items", [])),
            "data_source": data_source,
            "research_urls": evidence.get("browser_research_urls", {}),
        },
    }

    agent_outputs.append(output)
    logs.append(f"[SEO Specialist] Complete ({len(content)} chars, {data_source})")

    return {"agent_outputs": agent_outputs, "logs": logs}


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Paid Media & Performance Ads
# ─────────────────────────────────────────────────────────────────────

def paid_media_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    Paid Media & Performance Ads Specialist Sub-Agent Node.
    Uses free ad library research and public benchmarks.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Paid Media Specialist] Researching ad landscape for {company_name}")

    # 1. Gather real evidence
    evidence = _gather_evidence(f"{company_name} advertising paid ads campaign", company_name)

    # Add ad library URLs specifically
    if _free_tools:
        evidence.setdefault("browser_research_urls", {}).update({
            "google_ads_transparency": _free_tools.get_google_ads_transparency_url(company_name),
            "meta_ad_library": _free_tools.get_meta_ad_library_url(company_name),
        })

    logs.append(f"[Paid Media Specialist] Gathered {len(evidence.get('evidence_items', []))} evidence items")

    # 2. Load prompt template
    prompt_template = _load_prompt_template("paid-media-review.prompt.md")

    # 3. Build analysis request
    analysis_request = (
        f"1. **Competitor Ad Research**: Visit the Google Ads Transparency Center "
        f"and Meta Ad Library URLs to see what ads {company_name} and competitors run.\n"
        f"2. **Channel Strategy**: Recommend 2-4 paid channels based on the "
        f"evidence gathered and industry benchmarks.\n"
        f"3. **Ad Copy Drafts**: Write 2-3 ad variations per channel based on "
        f"VoC themes and competitor gaps found in the evidence.\n"
        f"4. **Budget Framework**: Recommend allocation with benchmarks from "
        f"search_web (search for '[industry] average CPC 2026').\n"
        f"5. **CRM Reconciliation Plan**: How to track real revenue, not just clicks.\n\n"
        f"⚠️ NEVER fabricate CPC/CPM benchmarks. Search for real data or state 'benchmark unavailable'.\n"
        f"Include [Source: URL] for every factual claim."
    )

    context = _build_context_block(state)
    evidence_text = _format_evidence_section(evidence)

    llm_result = _call_llm(
        system_prompt=prompt_template or "You are a performance marketing expert. Cite all sources.",
        user_prompt=f"{context}\n\n{evidence_text}\n\nAnalyze and produce:\n{analysis_request}",
    )

    if llm_result:
        content = llm_result
        data_source = "free_apis_plus_llm"
    else:
        content = _build_agent_research_brief(
            "paid_media_specialist", company_name, objective,
            evidence, analysis_request, prompt_template,
        )
        data_source = "free_apis_plus_agent_brief"

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_paid_2",
        "specialist": "paid_media",
        "title": f"{company_name} Paid Media Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "evidence_items_count": len(evidence.get("evidence_items", [])),
            "data_source": data_source,
            "ad_library_urls": {
                "google": evidence.get("browser_research_urls", {}).get("google_ads_transparency", ""),
                "meta": evidence.get("browser_research_urls", {}).get("meta_ad_library", ""),
            },
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Paid Media Specialist] Complete ({len(content)} chars, {data_source})")

    return {"agent_outputs": agent_outputs, "logs": logs}


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Content Strategy & ABM
# ─────────────────────────────────────────────────────────────────────

def content_strategy_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    Content Strategy & ABM Sub-Agent Node.
    Uses real VoC data and competitor content research.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Content Strategy] Researching content landscape for {company_name}")

    # 1. Gather VoC and content evidence
    evidence = _gather_evidence(
        f"{company_name} reviews feedback customer experience", company_name
    )

    # Add review platform URLs
    if _free_tools:
        review_urls = _free_tools.get_review_platform_urls(company_name)
        evidence.setdefault("browser_research_urls", {}).update(review_urls)

    logs.append(f"[Content Strategy] Gathered {len(evidence.get('evidence_items', []))} evidence items")

    # 2. Load prompt template
    prompt_template = _load_prompt_template("market-research.prompt.md")

    # 3. Reference prior specialist outputs
    seo_insights = ""
    paid_insights = ""
    for out in state.get("agent_outputs", []):
        if out.get("specialist") == "seo":
            seo_insights = out.get("content", "")[:1000]
        elif out.get("specialist") == "paid_media":
            paid_insights = out.get("content", "")[:1000]

    # 4. Build analysis request
    analysis_request = (
        f"1. **VoC-Driven ABM Sequence** (5-7 touches): Use the Reddit/HN "
        f"evidence above to identify real pain points and build messaging "
        f"that addresses them. Each touch: channel, timing, subject, body, CTA.\n"
        f"2. **Content Calendar** (30 days): Based on SEO keywords and "
        f"VoC themes from evidence. Research competitor content via "
        f"review platform URLs.\n"
        f"3. **Landing Page Spec**: Hero, value props, social proof, CTA.\n"
        f"4. **Email Nurture Sequence**: 4-6 drip emails for post-conversion.\n\n"
        f"Use actual quotes/themes from the evidence. No generic placeholders.\n"
        f"Include [Source: URL] for every claim."
    )

    context = _build_context_block(state)
    evidence_text = _format_evidence_section(evidence)

    prior_context = ""
    if seo_insights:
        prior_context += f"\n### Prior SEO Insights\n{seo_insights[:500]}\n"
    if paid_insights:
        prior_context += f"\n### Prior Paid Media Insights\n{paid_insights[:500]}\n"

    llm_result = _call_llm(
        system_prompt=prompt_template or "You are a content strategist. Cite sources.",
        user_prompt=f"{context}\n{prior_context}\n\n{evidence_text}\n\nProduce:\n{analysis_request}",
    )

    if llm_result:
        content = llm_result
        data_source = "free_apis_plus_llm"
    else:
        content = _build_agent_research_brief(
            "content_strategy", company_name, objective,
            evidence, analysis_request, prompt_template,
        )
        data_source = "free_apis_plus_agent_brief"

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_content_3",
        "specialist": "content_strategy",
        "title": f"{company_name} Content & ABM Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "evidence_items_count": len(evidence.get("evidence_items", [])),
            "data_source": data_source,
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Content Strategy] Complete ({len(content)} chars, {data_source})")

    return {"agent_outputs": agent_outputs, "logs": logs}


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Analyst Reviewer & Synthesis
# ─────────────────────────────────────────────────────────────────────

def analyst_reviewer_node(state: GraphState) -> Dict[str, Any]:
    """
    Analyst Reviewer Sub-Agent Node.
    Synthesizes all specialist outputs with quality checks.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Analyst Reviewer] Consolidating strategy for {company_name}")

    system_prompt = (
        "You are a senior marketing analyst. Your role is to:\n"
        "1. Synthesize outputs from SEO, Paid Media, and Content Strategy specialists\n"
        "2. Check cross-specialist coherence (messaging alignment, audience overlap)\n"
        "3. Identify gaps, contradictions, or unsupported claims\n"
        "4. Produce an executive GTM playbook with phased execution plan\n"
        "5. Flag any claims lacking [Source: URL] citations\n"
    )

    # Compile specialist outputs
    specialist_summaries = []
    total_evidence = 0
    for out in agent_outputs:
        specialist = out.get("specialist", "unknown")
        title = out.get("title", "Untitled")
        content = out.get("content", "")
        evidence_count = out.get("metadata", {}).get("evidence_items_count", 0)
        total_evidence += evidence_count
        specialist_summaries.append(
            f"### [{specialist.upper()}] {title}\n"
            f"*Evidence items: {evidence_count}*\n\n{content}\n"
        )

    context = _build_context_block(state)
    compiled = "\n---\n\n".join(specialist_summaries) if specialist_summaries else "No prior outputs."

    analysis_request = (
        f"## Synthesis Request\n\n"
        f"1. **Executive Summary** (3-5 paragraphs)\n"
        f"2. **Quality Audit**: Citation coverage, data freshness, unsupported claims\n"
        f"3. **Execution Roadmap**: Phase 1 (Days 1-14), Phase 2 (15-30), Phase 3 (31-60)\n"
        f"4. **Risk Register**: Top 3-5 risks with mitigations\n"
        f"5. **Research Gaps**: What needs deeper investigation via ego-browser\n"
    )

    llm_result = _call_llm(
        system_prompt=system_prompt,
        user_prompt=f"{context}\n\n{compiled}\n\n{analysis_request}",
    )

    if llm_result:
        content = llm_result
        data_source = "free_apis_plus_llm"
    else:
        # Build synthesis brief for the Antigravity agent
        content = (
            f"# {company_name} — Executive GTM Synthesis\n\n"
            f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"**Total Evidence Items**: {total_evidence}\n"
            f"**Mode**: Free Research (no paid APIs)\n\n"
            f"---\n\n"
            f"## Specialist Deliverables\n\n"
            f"{compiled}\n\n"
            f"---\n\n"
            f"## 🔍 Synthesis Instructions for Antigravity Agent\n\n"
            f"Review the specialist outputs above and use your built-in tools "
            f"(`search_web`, `read_url_content`) to:\n\n"
            f"{analysis_request}\n\n"
            f"Flag any claims that lack [Source: URL] citations.\n"
        )
        data_source = "free_apis_plus_agent_brief"

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_analyst_4",
        "specialist": "analyst",
        "title": f"{company_name} Executive GTM Synthesis",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_evidence_items": total_evidence,
            "quality_audit_included": True,
            "data_source": data_source,
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Analyst Reviewer] Complete ({len(content)} chars, {data_source})")

    return {"agent_outputs": agent_outputs, "logs": logs}
