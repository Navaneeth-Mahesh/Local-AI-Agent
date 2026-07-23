from enum import Enum


class PlanStepType(str, Enum):
    LLM = "llm"

    TOOL = "tool"

    FINISH = "finish"