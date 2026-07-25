registry = ToolRegistry()

calculator = CalculatorTool()

registry.register(calculator)

assert registry.exists("calculator")

tool = registry.get("calculator")

assert tool is calculator