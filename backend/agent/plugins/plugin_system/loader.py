import importlib
import pkgutil

from agent.plugin_system.interfaces import (
    BasePlugin,
)


class PluginLoader:

    def load_plugins(
        self,
        package,
    ):

        plugins = []

        for _, module_name, _ in pkgutil.iter_modules(
            package.__path__
        ):

            module = importlib.import_module(
                f"{package.__name__}.{module_name}"
            )

            plugin: BasePlugin = module.Plugin()

            plugins.append(
                plugin.load()
            )

        return plugins