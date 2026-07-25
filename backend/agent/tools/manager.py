from agent.tools.context import ToolContext
from agent.tools.registry import ToolRegistry
from agent.tools.result import ToolResult


class ToolManager:
    """
    Responsible for executing registered tools.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self._registry = registry

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

        validated_arguments = tool.input_model(
            **kwargs,
        )

        return await tool.execute(
            context,
            validated_arguments,
        )