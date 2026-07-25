from abc import ABC, abstractmethod

from agent.permissions.models import (
    PermissionRequest,
    PermissionResult,
)


class BasePermissionManager(ABC):

    @abstractmethod
    async def request_permission(
        self,
        request: PermissionRequest,
    ) -> PermissionResult:
        ...