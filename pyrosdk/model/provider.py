from typing import Dict, Any


class Provider:
    def __init__(self, name: str, values: Dict[str, Any]):
        self.name = name
        self.values = values

    def json(self):
        return {self.name: {**self.values}}
