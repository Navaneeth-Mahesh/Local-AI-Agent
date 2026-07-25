from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

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
        ...

    @property
    @abstractmethod
    def input_model(self) -> type[BaseModel]:
        """
        Pydantic model used to validate tool arguments.
        """

    @abstractmethod
    async def execute(
        self,
        context: ToolContext,
        arguments: BaseModel,
    ) -> ToolResult:
        ...