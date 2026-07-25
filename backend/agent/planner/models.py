from dataclasses import dataclass, field
from typing import Any
from agent.planner.enums import PlanStepType


@dataclass(slots=True)
class PlanStep:
    """
    Represents a single executable step in an execution plan.
    """

    step_type: PlanStepType

    action: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

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