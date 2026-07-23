from abc import ABC, abstractmethod

from agent.planner.models import ExecutionPlan
from agent.state.models import AgentState


class BasePlanner(ABC):

    @abstractmethod
    async def plan(
        self,
        state: AgentState,
    ) -> ExecutionPlan:
        """
        Generate an execution plan.
        """