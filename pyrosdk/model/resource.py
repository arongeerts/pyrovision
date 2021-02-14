from typing import Dict, Any


class Resource:
    def __init__(self, name: str, resource_type: str, values: Dict[str, Any]):
        self.name = name
        self.resource_type = resource_type
        self.values = values

    def json(self):
        return {self.resource_type: {self.name: {**self.values}}}
