from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar

from pyrocore.model.outputs import Outputs
from pyrovision.api.config import config
from pyrovision.api.utils import import_class
from pyrocore.model.plan import Plan
from pyrocore.model.stack import Stack
from pyrocore.model.state import State


CONFIG_TERRAFORM_CLIENT = "terraform.client"


class TerraformClient(ABC):
    def __init__(self, workspace: str):
        self.workspace = workspace

    @abstractmethod
    def apply(self, stack: Stack) -> Outputs:
        raise NotImplementedError()

    @abstractmethod
    def plan(self, stack: Stack) -> Plan:
        raise NotImplementedError()

    @abstractmethod
    def get(self, stack_id: str) -> State:
        raise NotImplementedError()

    @abstractmethod
    def destroy(self, stack: Stack) -> Plan:
        raise NotImplementedError()

    @abstractmethod
    def get_outputs(self) -> Outputs:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def init(cls):
        raise NotImplementedError()

    @classmethod
    def get_class(cls) -> ClassVar[TerraformClient]:
        name = config.get(
            CONFIG_TERRAFORM_CLIENT,
            "pyrovision.base.terraform.local.LocalTerraformClient",
        )
        return import_class(name)
