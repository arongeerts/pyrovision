from http.client import HTTPException

import requests

from pyrosdk.exceptions import PyroVisionException
from pyrosdk.model.stack import PyroVisionStack
from pyrovision.common.model.plan import Plan


class PyroVisionClient:
    def __init__(self, endpoint_url: str):
        if endpoint_url.endswith("/"):
            endpoint_url = endpoint_url[:-1]
        self.endpoint_url = endpoint_url

    def plan(self, stack: PyroVisionStack):
        payload = stack.json()
        resp = requests.post(self.endpoint_url + "/stacks/plan", json=payload)
        try:
            resp.raise_for_status()
        except HTTPException:
            raise PyroVisionException(
                resp.status_code, resp.json().get("message", resp.json())
            )
        plan = Plan(**resp.json())
        return plan

    def deploy(self, stack: PyroVisionStack):
        payload = stack.json()
        resp = requests.post(self.endpoint_url + "/stacks", json=payload)
        try:
            resp.raise_for_status()
        except HTTPException:
            raise PyroVisionException(
                resp.status_code, resp.json().get("message", resp.json())
            )
        return resp
