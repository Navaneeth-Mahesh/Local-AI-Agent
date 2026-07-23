from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ToolMetadata:
    """
    Metadata describing a tool.
    """

    name: str

    description: str

    requires_permission: bool = True