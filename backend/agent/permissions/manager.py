from agent.permissions.interfaces import BasePermissionManager
from agent.permissions.models import (
    PermissionRequest,
    PermissionResult,
)


class PermissionManager(BasePermissionManager):
    """
    Default permission manager.

    Currently auto-approves requests.
    This will be replaced by a real user approval flow.
    """

    async def request_permission(
        self,
        request: PermissionRequest,
    ) -> PermissionResult:

        return PermissionResult(
            granted=True,
            message=f"{request.permission.value} approved.",
        )