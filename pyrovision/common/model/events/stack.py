from pydantic.main import BaseModel

from pyrovision.common.model.events.base import Event
from pyrovision.common.model.stack import Stack


class _StackUpdated(BaseModel):
    stack: Stack


class _StackDeleted(BaseModel):
    stack: Stack


StackUpdatedEvent = Event[_StackUpdated]
StackDeletedEvent = Event[_StackDeleted]
