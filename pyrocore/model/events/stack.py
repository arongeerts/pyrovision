from pydantic.main import BaseModel

from pyrocore.model.events.base import Event
from pyrocore.model.stack import Stack


class _StackUpdated(BaseModel):
    stack: Stack


class _StackDeleted(BaseModel):
    stack: Stack


StackUpdatedEvent = Event[_StackUpdated]
StackDeletedEvent = Event[_StackDeleted]
