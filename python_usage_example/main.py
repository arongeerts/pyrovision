from pyrocore.model.outputs import Output
from pyrosdk.client import PyroVisionClient

from pyrosdk.model.stack import PyroVisionStack
from python_usage_example.aws_provider import AWSLocalProvider
from python_usage_example.bucket import Bucket

PYRO_URL = "http://localhost:8080"


def create_stack():
    """
    This method creates three S3 buckets on a local instance of PyroVision.
    The S3 buckets are created on a localstack instance. See the docker-compose file to set this up.
    This example shows how you can use a programming language to automate repetitive tasks
    """
    # Initialize the stack
    client = PyroVisionClient(PYRO_URL)
    stack = PyroVisionStack("my-test-stack")
    stack.add_provider(AWSLocalProvider())

    # Add the resources
    buckets = ["test-bucket-1", "test-bucket-2", "test-bucket-3"]
    for b in buckets:
        stack.add_resource(Bucket(b))

    # Run the plan first
    plan = client.plan(stack)

    # Do some security checks on the plan
    for change in plan.resource_changes:
        if (
            change.type_ == "aws_s3_bucket"
            and (change.change.after or {}).get("acl", "private") != "private"
        ):
            raise Exception("You are creating a non-private bucket!")

    # Set the outputs
    stack.with_output("arn", Output(value="${aws_s3_bucket.test-bucket-3.arn}"))

    print(stack.json())
    # Deploy
    client.deploy(stack)


if __name__ == "__main__":
    create_stack()
