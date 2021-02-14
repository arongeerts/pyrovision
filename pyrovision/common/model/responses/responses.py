from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from pyrovision.common.model.plan import Plan
from pyrovision.common.model.stack import Stack


class Status(str, Enum):
    OK = "ok"
    CREATED = "CREATED"
    DELETED = "DELETED"


class OK(BaseModel):
    status: Status


class ListStacksResponse(BaseModel):
    stacks: List[Stack]
    continuation_token: Optional[str]


class CreateStackResponse(BaseModel):
    plan: Plan
    stack: Stack
