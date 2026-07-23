from agent.planner.enums import PlanStepType
from agent.planner.models import (
    ExecutionPlan,
    PlanStep,
)
from agent.state.models import AgentState


class RuleBasedPlanningStrategy:
    """
    Extremely simple planning strategy.

    Later this will become LLM-powered.
    """

    TOOL_KEYWORDS = (
        "file",
        "folder",
        "directory",
        "terminal",
        "browser",
        "search",
    )

    def create_plan(
        self,
        state: AgentState,
    ) -> ExecutionPlan:

        plan = ExecutionPlan()

        prompt = state.user_input.lower()

        needs_tool = any(
            keyword in prompt
            for keyword in self.TOOL_KEYWORDS
        )

        if needs_tool:
            plan.add_step(
                PlanStep(
                    step_type=PlanStepType.TOOL,
                    action="tool_selection",
                )
            )

        plan.add_step(
            PlanStep(
                step_type=PlanStepType.LLM,
                action="generate_response",
            )
        )

        plan.add_step(
            PlanStep(
                step_type=PlanStepType.FINISH,
                action="complete",
            )
        )

        return plan