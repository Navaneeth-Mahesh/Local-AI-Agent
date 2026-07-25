from collections.abc import Iterable

from agent.tools.base import BaseTool


class ToolRegistry:
    """
    Central registry for all available tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:

        name = tool.metadata.name

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' already registered."
            )

        self._tools[name] = tool

    def get(
        self,
        name: str,
    ) -> BaseTool | None:

        return self._tools.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def list_tools(
        self,
    ) -> Iterable[BaseTool]:

        return self._tools.values()