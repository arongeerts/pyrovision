import boto3

dynamodb = boto3.client(
    "dynamodb",
    region_name="eu-west-1",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="foo",
    aws_secret_access_key="bar",
)

dynamodb.create_table(
    TableName="pyrovision-table",
    AttributeDefinitions=[{"AttributeName": "partition_key", "AttributeType": "S"}],
    BillingMode="PAY_PER_REQUEST",
    KeySchema=[{"AttributeName": "partition_key", "KeyType": "HASH"}],
)

sns = boto3.client(
    "sns",
    region_name="eu-west-1",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="foo",
    aws_secret_access_key="bar",
)

sns.create_topic(Name="StackUpdated")
sns.create_topic(Name="StackDeleted")
