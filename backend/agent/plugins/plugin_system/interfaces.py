from abc import ABC, abstractmethod

from agent.plugin_system.models import Plugin


class BasePlugin(ABC):

    @abstractmethod
    def load(self) -> Plugin:
        ...