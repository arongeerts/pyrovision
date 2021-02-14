from pyrosdk.model.provider import Provider


class AWSLocalProvider(Provider):
    name = "aws"
    values = {
        "alias": "python-local",
        "region": "eu-west-1",
        "access_key": "foo",
        "secret_key": "bar",
        "s3_force_path_style": True,
        "skip_credentials_validation": True,
        "skip_metadata_api_check": True,
        "skip_requesting_account_id": True,
        "endpoints": {"s3": "http://localstack:4566"},
    }

    def __init__(self):
        super().__init__(self.name, self.values)
