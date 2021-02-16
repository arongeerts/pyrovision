from abc import ABC, abstractmethod

from pyrovision.api.config import config
from pyrovision.api.exceptions import MissingConfigException
from pyrovision.api.utils import init_class
from pyrocore.model.events.stack import StackUpdatedEvent, StackDeletedEvent

DUMMY_NOTIFIER = "pyrovision.base.notification.none.Disabled"


class Notifier(ABC):
    @abstractmethod
    async def push_stack_updated_event(self, event: StackUpdatedEvent):
        raise NotImplementedError()

    @abstractmethod
    async def push_stack_deleted_event(self, event: StackDeletedEvent):
        raise NotImplementedError()

    @classmethod
    def create(cls):
        store_type = config.get("notification.implementation", DUMMY_NOTIFIER)
        if not store_type:
            raise MissingConfigException("notification.implementation")
        c = init_class(store_type)
        if not isinstance(c, Notifier):
            raise ImportError(f"Not a valid notification service: {store_type}")
        return c
