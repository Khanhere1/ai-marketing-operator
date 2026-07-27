"""
LangGraph Assembly & Graph Engineering Loop Construction.
Configures StateGraph nodes, sequential sub-agent execution, validation, 
and loop feedback edges.

UPDATED: Added validation_node between analyst_reviewer and evaluator.
Output quality is now checked before evaluation and delivery.
"""

import warnings
warnings.filterwarnings("ignore")

import logging
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import GraphState
from .nodes.planner import planner_node
from .nodes.sub_agents import (
    seo_specialist_node,
    paid_media_specialist_node,
    content_strategy_specialist_node,
    analyst_reviewer_node,
)
from .nodes.evaluator import evaluator_node

logger = logging.getLogger(__name__)


def validation_node(state: GraphState) -> Dict[str, Any]:
    """
    Output Validation Node.
    
    Runs all specialist outputs through the validation pipeline:
    - Citation density check (>80% threshold)
    - Data freshness check (90-day staleness)
    - Policy compliance check (prohibited patterns)
    - Content substance check (placeholder detection)
    
    Validation results are appended to the state for the evaluator
    to use in its quality assessment.
    """
    agent_outputs = state.get("agent_outputs", [])
    logs = list(state.get("logs", []))

    logs.append(f"[Validation Node] Validating {len(agent_outputs)} specialist outputs")

    try:
        from .validators.output_validator import validate_all_outputs
        
        validation_results = validate_all_outputs(agent_outputs)
        
        total_errors = 0
        total_warnings = 0
        validation_summary_parts = []
        
        for task_id, result in validation_results.items():
            total_errors += len(result.errors)
            total_warnings += len(result.warnings)
            validation_summary_parts.append(
                f"  - {task_id}: {'✅ PASS' if result.passed else '❌ FAIL'} "
                f"(citations: {result.citation_score:.0%}, "
                f"errors: {len(result.errors)}, warnings: {len(result.warnings)})"
            )
            logs.append(
                f"[Validation Node] {task_id}: "
                f"{'PASS' if result.passed else 'FAIL'} — "
                f"citation_score={result.citation_score:.2f}, "
                f"errors={len(result.errors)}, warnings={len(result.warnings)}"
            )

        validation_summary = (
            f"## Output Validation Summary\n\n"
            f"**Total Errors**: {total_errors}\n"
            f"**Total Warnings**: {total_warnings}\n\n"
            f"### Per-Specialist Results\n\n"
            + "\n".join(validation_summary_parts)
        )

        # Add detailed violation reports
        if total_errors > 0 or total_warnings > 0:
            validation_summary += "\n\n### Detailed Findings\n\n"
            for task_id, result in validation_results.items():
                if result.errors or result.warnings:
                    validation_summary += f"\n**{task_id}**:\n"
                    for err in result.errors:
                        validation_summary += f"  - ❌ {err}\n"
                    for warn in result.warnings:
                        validation_summary += f"  - ⚠️ {warn}\n"

        logs.append(
            f"[Validation Node] Complete: {total_errors} errors, {total_warnings} warnings"
        )

    except ImportError as e:
        logger.warning("Validation module not available: %s", str(e))
        validation_summary = (
            "## Output Validation Summary\n\n"
            "⚠️ Validation module not available. Install pyyaml for full policy checks.\n"
            "Basic validation skipped."
        )
        logs.append(f"[Validation Node] Skipped — module import error: {e}")

    return {
        "logs": logs,
        # Store validation summary for the evaluator to reference
        "evaluator_feedback": validation_summary if state.get("evaluator_feedback") is None else state.get("evaluator_feedback"),
    }


def should_continue(state: GraphState) -> Literal["planner", "__end__"]:
    """
    Conditional routing edge logic for the Graph Engineering Loop.
    Determines whether to loop back to the Planner Node or terminate at END.
    """
    is_satisfactory = state.get("is_satisfactory", False)
    iteration_count = state.get("iteration_count", 1)
    max_iterations = state.get("max_iterations", 3)

    if is_satisfactory or iteration_count >= max_iterations:
        return END
    else:
        return "planner"


def create_marketing_graph():
    """
    Constructs and compiles the LangGraph StateGraph for Marketing Graph Engineering Loops.
    
    Pipeline: Planner → SEO → Paid Media → Content Strategy → Analyst Reviewer → Validator → Evaluator
    """
    builder = StateGraph(GraphState)

    # Add Nodes
    builder.add_node("planner", planner_node)
    builder.add_node("seo_specialist", seo_specialist_node)
    builder.add_node("paid_media_specialist", paid_media_specialist_node)
    builder.add_node("content_strategy_specialist", content_strategy_specialist_node)
    builder.add_node("analyst_reviewer", analyst_reviewer_node)
    builder.add_node("validator", validation_node)
    builder.add_node("evaluator", evaluator_node)

    # Set Entry Point
    builder.add_edge(START, "planner")

    # Define Node Connections (Execution Flow)
    builder.add_edge("planner", "seo_specialist")
    builder.add_edge("seo_specialist", "paid_media_specialist")
    builder.add_edge("paid_media_specialist", "content_strategy_specialist")
    builder.add_edge("content_strategy_specialist", "analyst_reviewer")
    builder.add_edge("analyst_reviewer", "validator")
    builder.add_edge("validator", "evaluator")

    # Add Conditional Edge (Loop or Exit)
    builder.add_conditional_edges(
        "evaluator",
        should_continue,
        {
            "planner": "planner",
            END: END,
        },
    )

    # Compile Graph with Checkpointer
    checkpointer = MemorySaver()
    compiled_graph = builder.compile(checkpointer=checkpointer)
    return compiled_graph


def run_marketing_objective(
    objective: str,
    company_name: str = "OpenAI",
    max_iterations: int = 3,
    thread_id: str = "marketing_session_001",
) -> Dict[str, Any]:
    """
    Runs a complete LangGraph Graph Engineering Loop for a given objective and company.
    """
    graph = create_marketing_graph()

    initial_state: GraphState = {
        "objective": objective,
        "company_name": company_name,
        "plan_summary": "",
        "tasks": [],
        "current_task_index": 0,
        "agent_outputs": [],
        "evaluator_feedback": None,
        "is_satisfactory": False,
        "status": "PLANNING",
        "iteration_count": 0,
        "max_iterations": max_iterations,
        "artifacts": [],
        "logs": [],
    }

    config = {"configurable": {"thread_id": thread_id}}
    final_state = graph.invoke(initial_state, config=config)
    return final_state
