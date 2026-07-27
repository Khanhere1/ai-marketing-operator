"""
State definitions for LangGraph Graph Engineering Loops.
"""

from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TaskItem(TypedDict):
    id: str
    specialist: str  # 'seo', 'paid_media', 'content_strategy', 'analyst'
    title: str
    description: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    result: Optional[str]


class SubAgentOutput(TypedDict):
    task_id: str
    specialist: str
    title: str
    content: str
    metadata: Dict[str, Any]


class GraphState(TypedDict, total=False):
    """
    Main state schema for the LangGraph Graph Engineering loop.
    """
    objective: str
    company_name: str
    plan_summary: str
    tasks: List[TaskItem]
    current_task_index: int
    agent_outputs: List[SubAgentOutput]
    evaluator_feedback: Optional[str]
    is_satisfactory: bool
    status: str  # 'PLANNING' | 'EXECUTING' | 'EVALUATING' | 'REVISING' | 'COMPLETED'
    iteration_count: int
    max_iterations: int
    artifacts: List[str]
    logs: List[str]


class MarketingObjectiveInput(BaseModel):
    objective: str = Field(..., description="High-level marketing or GTM campaign objective")
    company_name: str = Field(default="OpenAI", description="Company or brand name")
    max_iterations: int = Field(default=3, description="Maximum graph loop iterations")
