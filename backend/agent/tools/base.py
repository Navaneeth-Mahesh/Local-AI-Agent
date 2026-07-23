from abc import ABC, abstractmethod

from agent.tools.context import ToolContext
from agent.tools.metadata import ToolMetadata
from agent.tools.result import ToolResult


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    @property
    @abstractmethod
    def metadata(self) -> ToolMetadata:
        """
        Tool description.
        """

    @abstractmethod
    async def execute(
        self,
        context: ToolContext,
        **kwargs,
    ) -> ToolResult:
        """
        Execute the tool.
        """