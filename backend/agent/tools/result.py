from dataclasses import dataclass, field


@dataclass(slots=True)
class ToolResult:
    """
    Standard response returned by every tool.
    """

    success: bool

    output: str

    metadata: dict = field(default_factory=dict)