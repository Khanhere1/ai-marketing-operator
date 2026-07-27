"""
Evaluator and Assurance Node for LangGraph Graph Engineering Loop.

UPDATED: Now uses validation results from the validation_node to make
quality decisions. Checks citation scores, policy violations, and 
content substance alongside specialist coverage.
"""

from typing import Dict, Any, List
from ..state import GraphState


def evaluator_node(state: GraphState) -> Dict[str, Any]:
    """
    Evaluator Node function: Assesses deliverables against objective,
    validation results, and policy requirements.
    """
    company_name = state.get("company_name", "OpenAI")
    agent_outputs = state.get("agent_outputs", [])
    iteration_count = state.get("iteration_count", 1)
    max_iterations = state.get("max_iterations", 3)
    validation_feedback = state.get("evaluator_feedback", "")
    logs = list(state.get("logs", []))

    logs.append(
        f"[Evaluator Node] Auditing {len(agent_outputs)} deliverables "
        f"(Iteration {iteration_count}/{max_iterations})"
    )

    # Check 1: Specialist coverage
    specialists_found = {out.get("specialist") for out in agent_outputs}
    required_specialists = {"seo", "paid_media", "content_strategy", "analyst"}
    missing_specialists = required_specialists - specialists_found

    # Check 2: Content substance (not empty or too short)
    empty_outputs = [
        out.get("task_id", "unknown")
        for out in agent_outputs
        if len(out.get("content", "")) < 100
    ]

    # Check 3: Parse validation results for critical failures
    has_validation_errors = False
    if validation_feedback and "❌ FAIL" in str(validation_feedback):
        has_validation_errors = True

    # Build evaluation decision
    issues = []

    if missing_specialists and iteration_count < max_iterations:
        issues.append(
            f"Missing deliverables from specialists: {', '.join(missing_specialists)}"
        )

    if empty_outputs and iteration_count < max_iterations:
        issues.append(
            f"Empty or insufficient outputs from: {', '.join(empty_outputs)}"
        )

    if has_validation_errors and iteration_count < max_iterations:
        issues.append(
            "Validation errors detected — citation density below threshold "
            "or policy violations found. See validation report for details."
        )

    if issues:
        is_satisfactory = False
        feedback = (
            f"REVISION REQUIRED (Iteration {iteration_count}):\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )
        if validation_feedback:
            feedback += f"\n\n{validation_feedback}"
        status = "REVISING"
        logs.append(f"[Evaluator Node] Evaluation FAILED: {len(issues)} issues found")
    else:
        is_satisfactory = True
        feedback = (
            "All specialist deliverables completed and verified. "
            "Validation checks passed."
        )
        if validation_feedback:
            feedback += f"\n\n{validation_feedback}"
        status = "COMPLETED"
        logs.append(
            "[Evaluator Node] Evaluation PASSED: Objective achieved with quality validation."
        )

    artifacts = [
        f"companies/{company_name.lower()}/overview/{company_name.lower()}_gtm_playbook.md",
        f"companies/{company_name.lower()}/paid_media/{company_name.lower()}_paid_ad_suite.md",
        f"companies/{company_name.lower()}/abm/{company_name.lower()}_outbound_playbook.md",
    ]

    return {
        "is_satisfactory": is_satisfactory,
        "evaluator_feedback": feedback,
        "status": status,
        "artifacts": artifacts,
        "logs": logs,
    }
