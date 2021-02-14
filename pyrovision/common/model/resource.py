from typing import Optional, Any, Dict

from pydantic import BaseModel, Field


class Resource(BaseModel):
    address: str
    mode: Optional[str]
    type_: str = Field(..., alias="type")
    name: str
    provider_name: Optional[str]
    schema_version: Optional[int]
    values: Optional[Dict[str, Any]]
    expressions: Optional[Dict[str, Any]]
    provider_config_key: Optional[str]

    def tf_json(self):
        return {self.type_: {self.name: {**self.values}}}
