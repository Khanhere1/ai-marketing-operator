"""
Unit and Integration Tests for LangGraph Graph Engineering Engine.
"""

import sys
import os
import unittest

# Ensure ai-marketing-operator is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph_engine.graph import create_marketing_graph, run_marketing_objective, should_continue
from graph_engine.state import GraphState
from langgraph.graph import END


class TestGraphEngine(unittest.TestCase):

    def test_graph_compilation(self):
        """Test that the StateGraph compiles without errors."""
        graph = create_marketing_graph()
        self.assertIsNotNone(graph)

    def test_should_continue_logic(self):
        """Test conditional edge routing logic."""
        # Case 1: Satisfactory -> END
        state_pass: GraphState = {"is_satisfactory": True, "iteration_count": 1, "max_iterations": 3}
        self.assertEqual(should_continue(state_pass), END)

        # Case 2: Unsatisfactory & under max_iterations -> planner
        state_loop: GraphState = {"is_satisfactory": False, "iteration_count": 1, "max_iterations": 3}
        self.assertEqual(should_continue(state_loop), "planner")

        # Case 3: Unsatisfactory & reached max_iterations -> END
        state_max: GraphState = {"is_satisfactory": False, "iteration_count": 3, "max_iterations": 3}
        self.assertEqual(should_continue(state_max), END)

    def test_run_marketing_objective_execution(self):
        """Test end-to-end execution of a marketing objective via LangGraph loop."""
        final_state = run_marketing_objective(
            objective="Launch OpenAI GPT-5 Enterprise GTM Strategy",
            company_name="OpenAI",
            max_iterations=3,
            thread_id="test_run_001",
        )

        self.assertEqual(final_state.get("status"), "COMPLETED")
        self.assertTrue(final_state.get("is_satisfactory"))
        self.assertGreaterEqual(len(final_state.get("agent_outputs", [])), 4)

        # Check specialists present
        specialists = {out["specialist"] for out in final_state.get("agent_outputs", [])}
        self.assertIn("seo", specialists)
        self.assertIn("paid_media", specialists)
        self.assertIn("content_strategy", specialists)
        self.assertIn("analyst", specialists)

        # Check logs presence
        self.assertGreater(len(final_state.get("logs", [])), 0)


if __name__ == "__main__":
    unittest.main()
