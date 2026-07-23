from dataclasses import dataclass

from agent.state.models import AgentState


@dataclass(slots=True)
class ToolContext:
    """
    Context shared with every tool.
    """

    state: AgentState