from agent.plugin_system.models import Plugin


class PluginRegistry:

    def __init__(self):

        self._plugins: dict[str, Plugin] = {}

    def register(
        self,
        plugin: Plugin,
    ):

        self._plugins[
            plugin.name
        ] = plugin

    def get(
        self,
        name: str,
    ) -> Plugin:

        return self._plugins[name]

    def all(self):

        return list(
            self._plugins.values()
        )