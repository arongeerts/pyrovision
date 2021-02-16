from __future__ import annotations

import datetime
import hashlib
import random
import string
import uuid
from typing import TypeVar, Generic

from pydantic.generics import GenericModel

Payload = TypeVar("Payload")


class Event(GenericModel, Generic[Payload]):
    timestamp: str  # For JSON encoding purposes, this is stored as a string
    event_id: str
    payload: Payload

    @classmethod
    def from_payload(cls, payload: Payload):
        timestamp = datetime.datetime.now()
        event_id = generate_id(timestamp)
        return Event(
            timestamp=timestamp.isoformat(), event_id=event_id, payload=payload
        )


def generate_id(timestamp):
    random_part = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
    return hashlib.md5(
        (timestamp.isoformat() + random_part).encode("utf-8")
    ).hexdigest()
