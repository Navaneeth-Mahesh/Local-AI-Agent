from dataclasses import dataclass


@dataclass(slots=True)
class AgentResult:
    """
    Final output produced by the agent.
    """

    response: str

    iterations: int

    tool_calls: int