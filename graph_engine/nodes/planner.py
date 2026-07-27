"""
Planner Node for LangGraph Graph Engineering Loop.
Responsible for breaking high-level objectives into sub-tasks for specialist nodes.
"""

from typing import Dict, Any, List
from ..state import GraphState, TaskItem


def planner_node(state: GraphState) -> Dict[str, Any]:
    """
    Planner Node function: Analyzes objective and creates or updates a structured sub-task plan.
    """
    objective = state.get("objective", "Default Marketing Objective")
    company_name = state.get("company_name", "OpenAI")
    iteration_count = state.get("iteration_count", 0) + 1
    evaluator_feedback = state.get("evaluator_feedback")
    existing_outputs = state.get("agent_outputs", [])
    logs = state.get("logs", [])

    log_msg = f"[Planner Node] Iteration {iteration_count}: Processing objective '{objective}' for {company_name}"
    logs.append(log_msg)

    # Check if this is a revision loop based on Evaluator feedback
    is_revision = evaluator_feedback is not None and not state.get("is_satisfactory", False)

    if is_revision:
        plan_summary = (
            f"REVISED PLAN (Iter {iteration_count}) for {company_name}: Addressing feedback: {evaluator_feedback}. "
            f"Refining SEO strategy, paid media positioning, and ABM content sequence."
        )
    else:
        plan_summary = (
            f"STRATEGIC GTM PLAN for {company_name}: Deconstruct objective '{objective}' into "
            f"4 execution streams: (1) SEO Keyword & Search Architecture, (2) Paid Media Campaign Suite, "
            f"(3) Outbound ABM Messaging & Landing Briefs, (4) Analytical Strategy Consolidation."
        )

    # Construct actionable tasks for Sub-Agent Nodes
    tasks: List[TaskItem] = [
        {
            "id": f"task_{company_name.lower()}_seo_1",
            "specialist": "seo",
            "title": f"{company_name} Organic Search & Competitive Keyword Matrix",
            "description": f"Analyze high-intent search queries, AEO/GEO vectors, and positioning for {company_name}.",
            "status": "pending",
            "result": None,
        },
        {
            "id": f"task_{company_name.lower()}_paid_2",
            "specialist": "paid_media",
            "title": f"{company_name} Performance Ad Suite & Paid Channel Allocation",
            "description": f"Design high-ROAS paid campaign structures and creative ad briefs for {company_name}.",
            "status": "pending",
            "result": None,
        },
        {
            "id": f"task_{company_name.lower()}_content_3",
            "specialist": "content_strategy",
            "title": f"{company_name} ABM Outbound Sequence & Conversion Briefs",
            "description": f"Draft multi-touch outbound email sequences and landing page ROI frameworks for {company_name}.",
            "status": "pending",
            "result": None,
        },
        {
            "id": f"task_{company_name.lower()}_analyst_4",
            "specialist": "analyst",
            "title": f"{company_name} Executive GTM Playbook & Measurement Framework",
            "description": f"Synthesize all specialist outputs into a unified commercial strategy playbook for {company_name}.",
            "status": "pending",
            "result": None,
        },
    ]

    return {
        "plan_summary": plan_summary,
        "tasks": tasks,
        "current_task_index": 0,
        "iteration_count": iteration_count,
        "status": "EXECUTING",
        "logs": logs,
        "evaluator_feedback": None,  # Reset feedback for current iteration
    }
