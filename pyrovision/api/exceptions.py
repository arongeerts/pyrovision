from typing import List


class StackNotFoundException(Exception):
    def __init__(self, stack_id: str):
        self.stack_id = stack_id


class MissingConfigException(Exception):
    def __init__(self, parameter: str):
        self.parameter = parameter

    def __repr__(self):
        return f"Missing Configuration parameter: {self.parameter}"


class TerraformOperationFailed(Exception):
    def __init__(self, cmd: List[str], message: str):
        self.cmd = cmd
        self.message = message
