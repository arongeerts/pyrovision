from typing import Any, Dict, List

from pyrocore.model.outputs import Output
from pyrosdk.model.provider import Provider
from pyrosdk.model.resource import Resource


class PyroVisionStack:
    def __init__(self, name: str):
        self.id = name
        self.resources: List[Resource] = []
        self.providers: List[Provider] = []
        self.outputs: Dict[str, Dict[str, str]] = {}

    def json(self) -> Dict[str, Any]:
        d = {"resource": {}, "provider": {}}
        for r in self.resources:
            if r.resource_type not in d["resource"]:
                d["resource"][r.resource_type] = {}
            d["resource"][r.resource_type] = {
                **d["resource"][r.resource_type],
                **r.json()[r.resource_type],
            }
        for p in self.providers:
            d["provider"].update(p.json())

        if self.outputs:
            d["output"] = self.outputs
        return {"id": self.id, "spec": d}

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

    def add_provider(self, provider: Provider):
        self.providers.append(provider)

    def with_output(self, name: str, output: Output):
        self.outputs.update({name: output.dict()})
