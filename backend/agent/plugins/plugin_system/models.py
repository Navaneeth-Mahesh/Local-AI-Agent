from dataclasses import dataclass

from agent.tools.base import BaseTool


@dataclass(slots=True)
class Plugin:

    name: str

    version: str

    description: str

    tools: list[BaseTool]