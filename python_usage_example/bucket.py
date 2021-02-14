from pyrosdk.model.resource import Resource


class Bucket(Resource):
    resource_type = "aws_s3_bucket"
    acl = "private"

    def __init__(self, name: str, **kwargs):
        defaults = {"acl": self.acl, "bucket": name, "provider": "aws.python-local"}
        defaults.update(kwargs)
        super().__init__(name, self.resource_type, defaults)
