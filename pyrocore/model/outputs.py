from typing import Optional, Dict

from pydantic.main import BaseModel


class Output(BaseModel):
    value: str
    description: Optional[str] = ""
    sensitive: Optional[bool] = False


Outputs = Dict[str, Output]
