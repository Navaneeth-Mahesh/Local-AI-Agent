from dataclasses import dataclass

from agent.permissions.enums import PermissionType


@dataclass(slots=True, frozen=True)
class ToolMetadata:
    """
    Metadata describing a tool.
    """

    name: str

    description: str

    requires_permission: bool = False

    permission_type: PermissionType | None = None