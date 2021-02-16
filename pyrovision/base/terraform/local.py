import json
import os
import subprocess
from typing import List

from pyrocore.model.outputs import Outputs
from pyrovision.api.exceptions import TerraformOperationFailed
from pyrovision.api.terraform.client import TerraformClient
from pyrocore.model.plan import Plan
from pyrocore.model.stack import Stack
from pyrocore.model.state import State


class LocalTerraformClient(TerraformClient):
    def __init__(self, workspace: str):
        super().__init__(workspace)
        self.plan_file = f"terraform.plan"
        self.state_file = f"terraform.tfstate"
        self.__create_workspace()

    def apply(self, stack: Stack) -> Outputs:
        self.plan(stack)
        self.run_cmd(
            [
                f"terraform",
                f"-chdir={self.workspace}",
                f"apply",
                f"-state={self.state_file}",
                f"-state-out={self.state_file}",
                f"-input=false",
                f"-lock=false",
                f"{self.plan_file}",
            ]
        )
        outputs = self.get_outputs()
        return outputs

    def plan(self, stack: Stack, destroy: bool = False) -> Plan:
        d = stack.tf_json()

        # Some fixes to get outputs right
        outputs = d.get("output")
        if outputs:
            del d["output"]
            with open(f"{self.workspace}/output.tf.json", "w") as f:
                f.write(json.dumps({"output": outputs}))

        with open(f"{self.workspace}/main.tf.json", "w") as f:
            f.write(json.dumps(d))
        terraform_plan = [
            f"terraform",
            f"-chdir={self.workspace}",
            f"plan",
            f"-input=false",
            f"-out={self.plan_file}",
        ]
        if destroy:
            terraform_plan.append("-destroy")

        self.run_cmd(terraform_plan)
        plan_json = self.run_cmd(
            ["terraform", f"-chdir={self.workspace}", "show", "-json", self.plan_file]
        )
        return Plan(**json.loads(plan_json))

    def get(self, stack_id: str) -> State:
        output = self.run_cmd(
            [
                f"terraform",
                f"-chdir={self.workspace}",
                f"show",
                f"-json",
                f"{self.state_file}",
            ]
        )
        return State(**json.loads(output))

    def destroy(self, stack: Stack) -> Plan:
        p = self.plan(stack, destroy=True)
        cmd = [
            f"terraform",
            f"-chdir={self.workspace}",
            f"apply",
            f"-state={self.state_file}",
            f"-state-out={self.state_file}",
            f"-input=false",
            f"-lock=false",
            f"{self.plan_file}",
        ]
        self.run_cmd(cmd)
        return p

    def get_outputs(self) -> Outputs:
        try:
            outputs_json = self.run_cmd(
                ["terraform", f"-chdir={self.workspace}", "output", "-json"]
            )
            return json.loads(outputs_json)
        except subprocess.CalledProcessError:
            return {}

    def __create_workspace(self):
        try:
            os.mkdir(self.workspace)
        except FileExistsError:
            pass

    @classmethod
    def init(cls):
        cmd = ["terraform", "init", "-input=false"]
        print(f"Running terraform command: {cmd}")
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8")
        print(f"Returned output: {output}")

    def __init_in_folder(self):
        cmd = ["terraform", f"-chdir={self.workspace}", "init", "-input=false"]
        self.run_cmd(cmd, True)

    def run_cmd(self, cmd: List[str], is_retry=False) -> str:
        print(f"Running terraform command: {cmd}")
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(
                "utf-8"
            )
        except subprocess.CalledProcessError as e:
            print(f"Returned error output: {e.output}")
            print(f"CalledProcessError: {e}")
            if (
                "Plugin reinitialization required" in str(e.output or "")
                and not is_retry
            ):
                self.__init_in_folder()
                return self.run_cmd(cmd, True)
            raise TerraformOperationFailed(cmd, e.output.decode("utf-8"))
        print(f"Returned output: {output}")

        return output
