class PyroVisionException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"""PyroVisionClient got an error:
status_code: {self.status_code}
message: {self.message}
"""

    def __repr__(self):
        return self.__str__()
