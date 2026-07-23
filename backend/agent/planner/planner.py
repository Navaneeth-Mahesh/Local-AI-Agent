from agent.planner.interfaces import BasePlanner
from agent.planner.models import ExecutionPlan
from agent.planner.strategies import RuleBasedPlanningStrategy
from agent.state.models import AgentState


class Planner(BasePlanner):
    """
    Default planner implementation.
    """

    def __init__(self) -> None:
        self._strategy = RuleBasedPlanningStrategy()

    async def plan(
        self,
        state: AgentState,
    ) -> ExecutionPlan:

        return self._strategy.create_plan(
            state
        )