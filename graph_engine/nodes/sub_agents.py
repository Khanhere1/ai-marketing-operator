"""
Specialist Sub-Agent Nodes for LangGraph Graph Engineering Loop.

REWRITTEN: These nodes now generate dynamic, context-aware analysis using
structured prompt templates instead of returning static hardcoded text.

Each specialist:
1. Reads the objective, company name, and constraints from GraphState
2. Loads the relevant prompt template from workflows/prompts/
3. Constructs a role-specific analysis prompt
4. Returns structured output with evidence requirements and citation rules

When integrated with an LLM runtime (OpenAI, Anthropic, Google AI), 
these nodes invoke real model calls. Without an LLM key configured,
they generate structured prompt packages that the Antigravity agent
can execute via its own tools (web search, URL reading).
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..state import GraphState, SubAgentOutput, TaskItem

logger = logging.getLogger(__name__)

# Base directory for prompt templates
PROMPTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "workflows", "prompts"
)


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
    Attempt to initialize an LLM client. Returns None if no API key is configured.
    Supports OpenAI, Anthropic, and Google AI in priority order.
    """
    # Try OpenAI
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            return {"provider": "openai", "client": openai.OpenAI(api_key=openai_key)}
        except ImportError:
            logger.info("OpenAI key found but 'openai' package not installed.")

    # Try Anthropic
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            import anthropic
            return {"provider": "anthropic", "client": anthropic.Anthropic(api_key=anthropic_key)}
        except ImportError:
            logger.info("Anthropic key found but 'anthropic' package not installed.")

    # Try Google AI
    google_key = os.environ.get("GOOGLE_API_KEY")
    if google_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=google_key)
            return {"provider": "google", "client": genai}
        except ImportError:
            logger.info("Google key found but 'google-generativeai' package not installed.")

    return None


def _call_llm(system_prompt: str, user_prompt: str, llm_client: Optional[Dict] = None) -> str:
    """
    Call an LLM with the given prompts. If no LLM client is available,
    returns a structured prompt package for the Antigravity agent to execute.
    """
    if llm_client is None:
        llm_client = _get_llm_client()

    if llm_client is None:
        # No LLM configured — return the prompt package for the Antigravity
        # agent to execute via its own capabilities (web search, URL reading)
        return (
            f"## ⚠️ LLM API NOT CONFIGURED — PROMPT PACKAGE FOR AGENT EXECUTION\n\n"
            f"No LLM API key found (checked: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY). "
            f"The Antigravity agent should execute this analysis using its built-in web search "
            f"and URL reading tools.\n\n"
            f"### System Instructions\n\n{system_prompt}\n\n"
            f"### Analysis Request\n\n{user_prompt}\n\n"
            f"### Required Actions\n\n"
            f"1. Use web search to gather real, current data for each section\n"
            f"2. Verify all competitor names, product versions, and pricing via official sources\n"
            f"3. Include `[Source: URL]` citations for every factual claim\n"
            f"4. Follow the output structure defined in the system instructions above\n"
        )

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
        return (
            f"## ⚠️ LLM CALL FAILED\n\n"
            f"Provider: {provider}\n"
            f"Error: {str(e)}\n\n"
            f"### Fallback: Use Antigravity agent tools to complete this analysis.\n\n"
            f"### Analysis Request\n\n{user_prompt}\n"
        )


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

    # Include prior specialist outputs for downstream agents
    prior_outputs = state.get("agent_outputs", [])
    if prior_outputs:
        context += "\n**Prior Specialist Outputs Available**:\n"
        for out in prior_outputs:
            context += f"- [{out.get('specialist', 'unknown').upper()}] {out.get('title', 'Untitled')}\n"

    return context


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: SEO & Organic Search
# ─────────────────────────────────────────────────────────────────────

def seo_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    SEO & Organic Search Specialist Sub-Agent Node.

    Performs keyword research, competitive search analysis, and 
    AEO/GEO optimization strategy using real data.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[SEO Specialist Node] Executing search analysis for {company_name}")

    # Load prompt template
    system_prompt = _load_prompt_template("market-research.prompt.md")
    if not system_prompt:
        system_prompt = (
            "You are a senior SEO and organic search strategist. "
            "Every claim must include a [Source: URL] citation. "
            "Never fabricate keyword volumes, rankings, or competitor data."
        )

    # Build analysis request
    context = _build_context_block(state)
    user_prompt = (
        f"# SEO & Organic Search Analysis Request\n\n"
        f"{context}\n\n"
        f"## Required Analysis\n\n"
        f"1. **High-Intent Keyword Clusters**: Identify 5-8 keyword clusters relevant to "
        f"{company_name}'s positioning. For each cluster:\n"
        f"   - Primary keyword and estimated search intent category\n"
        f"   - Top 3 competing pages currently ranking (with URLs)\n"
        f"   - Content gap or opportunity\n\n"
        f"2. **AEO/GEO Optimization Strategy**: How should {company_name} structure content "
        f"for AI-powered search engines (Perplexity, Google AI Overviews, ChatGPT search)?\n"
        f"   - Recommended schema markup types\n"
        f"   - FAQ/answer targeting opportunities\n\n"
        f"3. **Competitive Search Positioning**: Which competitors dominate the target "
        f"keyword space? What messaging angles do they use?\n\n"
        f"4. **Quick Win Opportunities**: 3-5 tactical SEO actions that can be "
        f"implemented within 2 weeks.\n\n"
        f"**CRITICAL**: Use web search to verify all keyword data and competitor rankings. "
        f"Include [Source: URL] for every factual claim."
    )

    content = _call_llm(system_prompt, user_prompt)

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_seo_1",
        "specialist": "seo",
        "title": f"{company_name} SEO & Organic Search Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "prompt_template": "market-research.prompt.md",
            "data_source": "llm_generated" if _get_llm_client() else "prompt_package",
        },
    }

    agent_outputs.append(output)
    logs.append(f"[SEO Specialist Node] Completed analysis ({len(content)} chars)")

    return {
        "agent_outputs": agent_outputs,
        "logs": logs,
    }


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Paid Media & Performance Ads
# ─────────────────────────────────────────────────────────────────────

def paid_media_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    Paid Media & Performance Ads Specialist Sub-Agent Node.

    Designs campaign architectures, audits ad performance, and 
    recommends budget allocations with CRM reconciliation.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Paid Media Specialist Node] Designing campaigns for {company_name}")

    system_prompt = _load_prompt_template("paid-media-review.prompt.md")
    if not system_prompt:
        system_prompt = (
            "You are a senior performance marketing specialist. "
            "Never present platform-attributed metrics as proven revenue. "
            "CRM reconciliation is mandatory. Include [Source: URL] for all claims."
        )

    context = _build_context_block(state)
    user_prompt = (
        f"# Paid Media Campaign Architecture & Performance Analysis\n\n"
        f"{context}\n\n"
        f"## Required Analysis\n\n"
        f"1. **Channel Strategy**: Recommend 2-4 paid channels for {company_name} based on:\n"
        f"   - Target audience profile and where they consume content\n"
        f"   - Competitor ad activity (search Meta Ad Library, Google Ads Transparency)\n"
        f"   - Expected CPM/CPC benchmarks for the industry [Source: URL]\n\n"
        f"2. **Campaign Architecture**: For each recommended channel:\n"
        f"   - Campaign structure (campaigns, ad groups/sets, targeting)\n"
        f"   - Audience segments with rationale\n"
        f"   - Budget allocation recommendation with expected returns\n\n"
        f"3. **Ad Copy & Creative Direction**: Draft 2-3 ad variations per channel:\n"
        f"   - Headline, body, CTA\n"
        f"   - Messaging angle tied to VoC/competitor analysis\n\n"
        f"4. **Measurement Framework**:\n"
        f"   - Primary KPIs per channel\n"
        f"   - CRM reconciliation plan (platform conversions vs actual revenue)\n"
        f"   - Attribution model recommendation\n\n"
        f"**CRITICAL**: Research actual ad benchmarks for {company_name}'s industry. "
        f"Never fabricate CPM/CPC/ROAS numbers. "
        f"If data is unavailable, state: '⚠️ BENCHMARK DATA UNAVAILABLE'."
    )

    content = _call_llm(system_prompt, user_prompt)

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_paid_2",
        "specialist": "paid_media",
        "title": f"{company_name} Paid Media Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "prompt_template": "paid-media-review.prompt.md",
            "data_source": "llm_generated" if _get_llm_client() else "prompt_package",
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Paid Media Specialist Node] Completed analysis ({len(content)} chars)")

    return {
        "agent_outputs": agent_outputs,
        "logs": logs,
    }


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Content Strategy & ABM
# ─────────────────────────────────────────────────────────────────────

def content_strategy_specialist_node(state: GraphState) -> Dict[str, Any]:
    """
    Content Strategy & ABM Sub-Agent Node.

    Creates evidence-backed content plans, ABM sequences, and 
    landing page specifications.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Content Strategy Node] Drafting ABM sequences for {company_name}")

    system_prompt = _load_prompt_template("market-research.prompt.md")
    if not system_prompt:
        system_prompt = (
            "You are a senior content strategist and ABM specialist. "
            "All messaging must be evidence-backed. "
            "Include [Source: URL] citations for competitive claims."
        )

    context = _build_context_block(state)

    # Reference prior specialist outputs for coherent strategy
    seo_insights = ""
    paid_insights = ""
    for out in state.get("agent_outputs", []):
        if out.get("specialist") == "seo":
            seo_insights = out.get("content", "")[:1000]
        elif out.get("specialist") == "paid_media":
            paid_insights = out.get("content", "")[:1000]

    user_prompt = (
        f"# Content Strategy & ABM Playbook\n\n"
        f"{context}\n\n"
        f"## Prior Specialist Insights\n\n"
        f"### SEO Insights (Summary)\n{seo_insights[:500] if seo_insights else 'Not yet available'}\n\n"
        f"### Paid Media Insights (Summary)\n{paid_insights[:500] if paid_insights else 'Not yet available'}\n\n"
        f"## Required Analysis\n\n"
        f"1. **Multi-Touch ABM Outbound Sequence** (5-7 touches):\n"
        f"   - For each touch: Channel, timing, subject/headline, body draft, CTA\n"
        f"   - Personalization variables and segmentation logic\n"
        f"   - Message angles derived from VoC research (cite evidence)\n\n"
        f"2. **Content Calendar** (Next 30 Days):\n"
        f"   - Content type, topic, target keyword, distribution channel\n"
        f"   - Aligned with SEO keyword clusters and paid media messaging\n\n"
        f"3. **Landing Page Specification**:\n"
        f"   - Hero section: headline, subheadline, primary CTA\n"
        f"   - Value proposition blocks with evidence points\n"
        f"   - Social proof and trust elements\n"
        f"   - Conversion form fields and progressive profiling strategy\n\n"
        f"4. **Email Nurture Sequence** (Post-conversion):\n"
        f"   - 4-6 email drip sequence for marketing-qualified leads\n"
        f"   - Each email: subject, preview text, body outline, CTA\n\n"
        f"**CRITICAL**: All messaging angles must reference competitor weaknesses "
        f"or customer pain points discovered in prior analysis. "
        f"No generic placeholder content."
    )

    content = _call_llm(system_prompt, user_prompt)

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_content_3",
        "specialist": "content_strategy",
        "title": f"{company_name} ABM & Content Strategy",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "prompt_template": "market-research.prompt.md",
            "data_source": "llm_generated" if _get_llm_client() else "prompt_package",
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Content Strategy Node] Completed analysis ({len(content)} chars)")

    return {
        "agent_outputs": agent_outputs,
        "logs": logs,
    }


# ─────────────────────────────────────────────────────────────────────
# SPECIALIST NODE: Analyst Reviewer & Synthesis
# ─────────────────────────────────────────────────────────────────────

def analyst_reviewer_node(state: GraphState) -> Dict[str, Any]:
    """
    Analyst Reviewer Sub-Agent Node.
    
    Synthesizes all specialist deliverables into a unified executive 
    strategy with cross-specialist coherence checks and policy validation.
    """
    company_name = state.get("company_name", "Unknown")
    objective = state.get("objective", "")
    agent_outputs = list(state.get("agent_outputs", []))
    logs = list(state.get("logs", []))

    logs.append(f"[Analyst Reviewer Node] Consolidating GTM strategy for {company_name}")

    system_prompt = (
        "You are a senior marketing analyst and strategy reviewer. Your role is to:\n"
        "1. Synthesize outputs from SEO, Paid Media, and Content Strategy specialists\n"
        "2. Check for cross-specialist coherence (messaging alignment, audience overlap)\n"
        "3. Identify gaps, contradictions, or unsupported claims across deliverables\n"
        "4. Produce an executive-level GTM playbook with clear phased execution plan\n"
        "5. Flag any claims that lack [Source: URL] citations\n"
        "6. Validate compliance with global prohibitions policy\n\n"
        "## QUALITY CHECKS TO PERFORM:\n"
        "- [ ] All factual claims have source citations\n"
        "- [ ] No fabricated product names, versions, or pricing\n"
        "- [ ] Competitor data is current (within 90 days)\n"
        "- [ ] Platform metrics are not presented as proven revenue\n"
        "- [ ] Budget recommendations include marginal return analysis\n"
        "- [ ] Messaging angles are consistent across channels\n"
    )

    # Compile all specialist outputs
    specialist_summaries = []
    for out in agent_outputs:
        specialist = out.get("specialist", "unknown")
        title = out.get("title", "Untitled")
        content = out.get("content", "")
        specialist_summaries.append(
            f"### [{specialist.upper()}] {title}\n\n{content}\n"
        )

    context = _build_context_block(state)
    compiled_outputs = "\n---\n\n".join(specialist_summaries) if specialist_summaries else "No prior specialist outputs available."

    user_prompt = (
        f"# Executive GTM Strategy Synthesis & Quality Review\n\n"
        f"{context}\n\n"
        f"## Specialist Deliverables to Synthesize\n\n"
        f"{compiled_outputs}\n\n"
        f"## Required Output\n\n"
        f"1. **Executive Summary** (3-5 paragraphs):\n"
        f"   - Strategic situation assessment\n"
        f"   - Key opportunities identified across specialists\n"
        f"   - Primary recommendation with expected business impact\n\n"
        f"2. **Quality Audit Report**:\n"
        f"   - Citation coverage: % of claims with source URLs\n"
        f"   - Data freshness: any stale data flagged\n"
        f"   - Unsupported claims: list any claims lacking evidence\n"
        f"   - Policy compliance: any prohibited patterns detected\n\n"
        f"3. **Commercial Execution Roadmap**:\n"
        f"   - Phase 1 (Days 1-14): Quick wins and immediate actions\n"
        f"   - Phase 2 (Days 15-30): Campaign launches and content deployment\n"
        f"   - Phase 3 (Days 31-60): Optimization, measurement, iteration\n"
        f"   - Each phase: specific actions, owners, success metrics\n\n"
        f"4. **Risk Register**:\n"
        f"   - Top 3-5 risks with mitigation strategies\n"
        f"   - Research gaps that need to be closed\n"
        f"   - Assumptions that need validation\n\n"
        f"**CRITICAL**: If any specialist output contains unsourced claims, "
        f"flag them explicitly in the Quality Audit Report."
    )

    content = _call_llm(system_prompt, user_prompt)

    output: SubAgentOutput = {
        "task_id": f"task_{company_name.lower().replace(' ', '_')}_analyst_4",
        "specialist": "analyst",
        "title": f"{company_name} Executive GTM Synthesis & Quality Review",
        "content": content,
        "metadata": {
            "status": "SUCCESS",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "quality_audit_included": True,
            "data_source": "llm_generated" if _get_llm_client() else "prompt_package",
        },
    }

    agent_outputs.append(output)
    logs.append(f"[Analyst Reviewer Node] Completed synthesis ({len(content)} chars)")

    return {
        "agent_outputs": agent_outputs,
        "logs": logs,
    }
