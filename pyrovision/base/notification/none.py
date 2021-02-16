from pyrovision.api.notification.service import Notifier
from pyrocore.model.events.stack import StackDeletedEvent, StackUpdatedEvent


class Disabled(Notifier):
    def push_stack_updated_event(self, event: StackUpdatedEvent):
        pass

    def push_stack_deleted_event(self, event: StackDeletedEvent):
        pass
