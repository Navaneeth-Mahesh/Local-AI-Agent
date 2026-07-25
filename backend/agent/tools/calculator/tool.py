from agent.tools.base import BaseTool
from agent.tools.context import ToolContext
from agent.tools.metadata import ToolMetadata
from agent.tools.result import ToolResult
from agent.tools.calculator.models import CalculatorInput


class CalculatorTool(BaseTool):

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="calculator",
            description="Perform arithmetic calculations.",
            requires_permission=False,
        )

    @property
    def input_model(self):
        return CalculatorInput

    async def execute(
        self,
        context: ToolContext,
        arguments: CalculatorInput,
    ) -> ToolResult:

        try:
            result = eval(
                arguments.expression,
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