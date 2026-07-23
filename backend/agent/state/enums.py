from enum import Enum


class AgentStatus(str, Enum):
    IDLE = "idle"

    RUNNING = "running"

    WAITING_TOOL = "waiting_tool"

    COMPLETED = "completed"

    FAILED = "failed"