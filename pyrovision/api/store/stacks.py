from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from pyrovision.api.exceptions import MissingConfigException
from pyrovision.api.utils import init_class
from pyrocore.model.responses.responses import ListStacksResponse
from pyrovision.api.config import config
from pyrocore.model.stack import Stack


class StackStore(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save(self, stack: Stack) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, stack_id: str) -> Stack:
        raise NotImplementedError()

    @abstractmethod
    def update(self, stack: Stack) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, stack_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def list(self, token: Optional[str]) -> ListStacksResponse:
        raise NotImplementedError()

    @classmethod
    def create(cls) -> StackStore:
        store_type = config.get("stackstore.implementation")
        if not store_type:
            raise MissingConfigException("stackstore.implementation")
        c = init_class(store_type)
        if not isinstance(c, StackStore):
            raise ImportError(f"Not a valid stackstore: {store_type}")
        return c
