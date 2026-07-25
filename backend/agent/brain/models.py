from dataclasses import dataclass

from agent.planner.models import ExecutionPlan
from agent.state.models import AgentState
from agent.tools.result import ToolResult


@dataclass(slots=True)
class AgentResponse:
    """
    Final response returned by the Agent Brain.
    """

    state: AgentState

    plan: ExecutionPlan

    response: str

    tool_results: list[ToolResult]