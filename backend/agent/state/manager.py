from agent.state.enums import AgentStatus
from agent.state.models import AgentState


class AgentStateManager:
    """
    Responsible for mutating AgentState.
    """

    @staticmethod
    def start(
        state: AgentState,
    ) -> None:

        state.status = AgentStatus.RUNNING

        state.current_step = 1

    @staticmethod
    def next_step(
        state: AgentState,
    ) -> None:

        state.current_step += 1

    @staticmethod
    def complete(
        state: AgentState,
    ) -> None:

        state.status = AgentStatus.COMPLETED

    @staticmethod
    def fail(
        state: AgentState,
    ) -> None:

        state.status = AgentStatus.FAILED