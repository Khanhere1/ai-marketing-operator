#!/usr/bin/env python3
"""
Runnable example demonstrating LangGraph Graph Engineering Loops.
Runs a multi-agent loop with Planner, SEO Specialist, Paid Media Specialist,
Content Strategy Specialist, Analyst Reviewer, and Evaluator nodes.
"""

import os
import sys
import json
import warnings

warnings.filterwarnings("ignore")

# Ensure ai-marketing-operator is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph_engine import run_marketing_objective


def main():
    print("================================================================================")
    print("🚀 LANGGRAPH GRAPH ENGINEERING ENGINE — AI MARKETING OPERATOR")
    print("================================================================================\n")

    objective = "Execute Enterprise GTM campaign for OpenAI: Launch autonomous agent platform for Fortune 500 decision makers."
    company_name = "OpenAI"

    print(f"📌 Objective: {objective}")
    print(f"🏢 Company: {company_name}")
    print(f"🔄 Max Loop Iterations: 3\n")
    print("Starting LangGraph StateGraph execution loop...\n")

    # Run the graph loop
    final_state = run_marketing_objective(
        objective=objective,
        company_name=company_name,
        max_iterations=3,
        thread_id="openai_gtm_run_001",
    )

    print("--------------------------------------------------------------------------------")
    print("📋 GRAPH EXECUTION LOGS:")
    print("--------------------------------------------------------------------------------")
    for log in final_state.get("logs", []):
        print(f"  • {log}")

    print("\n--------------------------------------------------------------------------------")
    print("🎯 EXECUTION SUMMARY:")
    print("--------------------------------------------------------------------------------")
    print(f"Status: {final_state.get('status')}")
    print(f"Iterations Completed: {final_state.get('iteration_count')}")
    print(f"Satisfactory Quality: {final_state.get('is_satisfactory')}")
    print(f"Plan Summary:\n{final_state.get('plan_summary')}\n")

    print("--------------------------------------------------------------------------------")
    print("📦 GENERATED AGENT DELIVERABLES:")
    print("--------------------------------------------------------------------------------")
    for output in final_state.get("agent_outputs", []):
        print(f"\n[Specialist: {output['specialist'].upper()}] Task: {output['title']}")
        print(f"Task ID: {output['task_id']}")
        print(f"Content Preview:\n{output['content'][:250]}...\n")

    print("--------------------------------------------------------------------------------")
    print("✨ TARGET ARTIFACT DESTINATIONS:")
    print("--------------------------------------------------------------------------------")
    for artifact in final_state.get("artifacts", []):
        print(f"  📄 {artifact}")

    print("\n================================================================================")
    print("✅ LANGGRAPH GRAPH ENGINEERING LOOP COMPLETED SUCCESSFULLY!")
    print("================================================================================\n")


if __name__ == "__main__":
    main()
