from agent.permissions.manager import PermissionManager
from agent.permissions.models import PermissionRequest
from agent.tools.context import ToolContext
from agent.tools.registry import ToolRegistry
from agent.tools.result import ToolResult


class ToolManager:

    def __init__(
        self,
        registry: ToolRegistry,
        permission_manager: PermissionManager,
    ) -> None:

        self._registry = registry
        self._permission_manager = permission_manager

    async def execute(
        self,
        tool_name: str,
        context: ToolContext,
        **kwargs,
    ) -> ToolResult:

        tool = self._registry.get(tool_name)

        if tool is None:

            return ToolResult(
                success=False,
                output=f"Tool '{tool_name}' not found.",
            )

        metadata = tool.metadata

        # -----------------------------
        # Permission Enforcement
        # -----------------------------

        if metadata.requires_permission:

            result = await self._permission_manager.request_permission(
                PermissionRequest(
                    permission=metadata.permission_type,
                    reason=f"Execute '{metadata.name}' tool.",
                )
            )

            if not result.granted:

                return ToolResult(
                    success=False,
                    output=result.message,
                )

        # -----------------------------
        # Validate Input
        # -----------------------------

        arguments = tool.input_model(
            **kwargs,
        )

        return await tool.execute(
            context=context,
            arguments=arguments,
        )