from typing import Any, Dict, Optional

from pydantic import BaseModel


class Stack(BaseModel):
    id: str
    spec: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = {}

    def tf_json(self):
        return self.spec
