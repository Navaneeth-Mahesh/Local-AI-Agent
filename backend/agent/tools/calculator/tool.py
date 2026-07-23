from agent.tools.base import BaseTool
from agent.tools.context import ToolContext
from agent.tools.metadata import ToolMetadata
from agent.tools.result import ToolResult


class CalculatorTool(BaseTool):

    @property
    def metadata(self) -> ToolMetadata:

        return ToolMetadata(
            name="calculator",
            description="Perform arithmetic calculations.",
            requires_permission=False,
        )

    async def execute(
        self,
        context: ToolContext,
        *,
        expression: str,
    ) -> ToolResult:

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {},
            )

            return ToolResult(
                success=True,
                output=str(result),
            )

        except Exception as exc:
            return ToolResult(
                success=False,
                output=str(exc),
            )