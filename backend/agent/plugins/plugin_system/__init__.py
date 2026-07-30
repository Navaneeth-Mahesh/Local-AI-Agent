from agent.plugin_system.interfaces import (
    BasePlugin,
)
from agent.plugin_system.models import Plugin
from agent.tools.calculator import CalculatorTool


class Plugin(
    BasePlugin,
):

    def load(
        self,
    ):

        return Plugin(
            name="calculator",
            version="1.0.0",
            description="Math operations",
            tools=[
                CalculatorTool(),
            ],
        )