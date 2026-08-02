from agent.tools.registry import ToolRegistry
from agent.tools.calculator.tool import CalculatorTool


def test_tool_registry():
    registry = ToolRegistry()
    calculator = CalculatorTool()

    registry.register(calculator)

    assert registry.exists("calculator")
    tool = registry.get("calculator")
    assert tool is calculator