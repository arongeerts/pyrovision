from typing import List

from pydantic import BaseModel

from pyrovision.common.model.resource import Resource


class _RootModule(BaseModel):
    resources: List[Resource]


class _Values(BaseModel):
    root_module: _RootModule


class State(BaseModel):
    format_version: str
    terraform_version: str
    values: _Values
