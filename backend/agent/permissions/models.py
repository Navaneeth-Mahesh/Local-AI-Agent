from dataclasses import dataclass

from agent.permissions.enums import PermissionType


@dataclass(slots=True)
class PermissionRequest:
    permission: PermissionType
    reason: str


@dataclass(slots=True)
class PermissionResult:
    granted: bool
    message: str