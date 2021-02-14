from typing import Any, Dict

from pydantic import BaseModel


class Stack(BaseModel):
    id: str
    spec: Dict[str, Any]

    def tf_json(self):
        return self.spec
