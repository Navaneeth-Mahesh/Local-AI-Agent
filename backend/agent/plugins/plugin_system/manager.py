from agent.plugin_system.loader import (
    PluginLoader,
)
from agent.plugin_system.registry import (
    PluginRegistry,
)


class PluginManager:

    def __init__(
        self,
        loader: PluginLoader,
        registry: PluginRegistry,
    ):

        self._loader = loader

        self._registry = registry

    def initialize(
        self,
        package,
    ):

        plugins = self._loader.load_plugins(
            package
        )

        for plugin in plugins:

            self._registry.register(
                plugin
            )