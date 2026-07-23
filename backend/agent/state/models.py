from dataclasses import dataclass, field

from agent.context.models import LLMContext
from agent.state.enums import AgentStatus


@dataclass(slots=True)
class AgentState:
    """
    Represents the complete execution state
    of the agent.
    """

    user_input: str

    status: AgentStatus = AgentStatus.IDLE

    current_step: int = 0

    context: LLMContext | None = None

    tool_results: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)