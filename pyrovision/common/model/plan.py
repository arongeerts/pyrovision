from typing import Dict, List, Any, Optional

from pydantic import BaseModel, Field

from pyrovision.common.model.resource import Resource


class _RootModule(BaseModel):
    resources: Optional[List[Resource]]


class _Configuration(BaseModel):
    provider_config: Dict[str, Any]
    root_module: _RootModule


class _Change(BaseModel):
    actions: List[str]
    before: Optional[Dict[str, Any]]
    after: Optional[Dict[str, Any]]
    after_unknown: Optional[Dict[str, Any]]


class _ResourceChange(BaseModel):
    address: str
    mode: str
    type_: str = Field(..., alias="type")
    name: str
    provider_name: Optional[str]
    change: _Change


class _Values(BaseModel):
    root_module: _RootModule


class Plan(BaseModel):
    format_version: str
    terraform_version: str
    planned_values: _Values
    resource_changes: List[_ResourceChange]
    configuration: _Configuration
