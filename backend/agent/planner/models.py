from dataclasses import dataclass, field

from agent.planner.enums import PlanStepType


@dataclass(slots=True)
class PlanStep:
    """
    Represents one step in an execution plan.
    """

    step_type: PlanStepType

    action: str

    metadata: dict = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionPlan:
    """
    Complete execution plan.
    """

    steps: list[PlanStep] = field(default_factory=list)

    def add_step(
        self,
        step: PlanStep,
    ) -> None:
        self.steps.append(step)