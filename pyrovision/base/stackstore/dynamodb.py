import base64
import json
from typing import Dict, Optional

import boto3
from dynamodb_json import json_util as dynamo_json

from pyrovision.api.config import config
from pyrovision.api.exceptions import StackNotFoundException, MissingConfigException
from pyrovision.api.store.stacks import StackStore
from pyrovision.common.model.responses.responses import ListStacksResponse
from pyrovision.common.model.stack import Stack

CONFIG_TABLE = "stackstore.dynamodb.table"
CONFIG_PART_KEY = "stackstore.dynamodb.partition_key"
CONFIG_REGION = "stackstore.dynamodb.region"
CONFIG_ENDPOINT_URL = "stackstore.dynamodb.endpoint_url"
CONFIG_ACCESS_KEY = "stackstore.dynamodb.aws_access_key_id"
CONFIG_SECRET_KEY = "stackstore.dynamodb.aws_secret_access_key"
CONFIG_SESSION_TOKEN = "stackstore.dynamodb.aws_session_token"


class DynamoDBStackStore(StackStore):
    def __init__(self):
        super().__init__()
        try:
            table = config[CONFIG_TABLE]
            partition_key = config[CONFIG_PART_KEY]
            region = config[CONFIG_REGION]
            endpoint_url = config.get(
                CONFIG_ENDPOINT_URL, f"https://dynamodb.{region}.amazonaws.com"
            )
            access_key = config.get(CONFIG_ACCESS_KEY)
            secret_key = config.get(CONFIG_SECRET_KEY)
            session_token = config.get(CONFIG_SESSION_TOKEN)
        except KeyError as e:
            raise MissingConfigException(e.args[0])

        self.client = boto3.client(
            "dynamodb",
            region_name=region,
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token,
        )
        self.partition_key = partition_key
        self.table = table

    def save(self, stack: Stack) -> None:
        d = stack.dict()
        d[self.partition_key] = stack.id
        payload = json.loads(dynamo_json.dumps(d))
        self.client.put_item(Item=payload, TableName=self.table)

    def get(self, stack_id: str) -> Stack:
        key = {self.partition_key: {"S": stack_id}}
        item = self.client.get_item(Key=key, TableName=self.table).get("Item")
        if not item:
            raise StackNotFoundException(stack_id)
        return Stack(**dynamo_json.loads(item))

    def update(self, stack: Stack) -> None:
        self.save(stack)

    def delete(self, stack_id: str) -> None:
        key = {self.partition_key: {"S": stack_id}}
        self.client.delete_item(Key=key, TableName=self.table).get("Item")

    def list(self, token: Optional[str]) -> ListStacksResponse:
        params = {
            "TableName": self.table,
        }
        if token:
            start_key = decode_item(token)
            params["ExclusiveStartKey"] = start_key
        response = self.client.scan(**params)
        items = response.get("Items", [])
        items = [Stack(**dynamo_json.loads(i)) for i in items]
        token = response.get("LastEvaluatedKey")
        if token:
            token = encode_item(token)
        return ListStacksResponse(stacks=items, continuation_token=token)


def encode_item(item: Dict[str, Dict[str, str]]) -> str:
    s = json.dumps(item)
    return base64.urlsafe_b64encode(s.encode()).decode()


def decode_item(s: str) -> Dict:
    result = base64.urlsafe_b64decode(s)
    return json.loads(result)
