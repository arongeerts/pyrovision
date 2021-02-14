import json

import boto3

from pyrovision.api.config import config
from pyrovision.api.exceptions import MissingConfigException
from pyrovision.api.notification.service import Notifier
from pyrovision.common.model.events.stack import StackDeletedEvent, StackUpdatedEvent

CONFIG_UPDATED_TOPIC = "notification.sns.topics.stack_updated"
CONFIG_DELETED_TOPIC = "notification.sns.topics.stack_deleted"
CONFIG_SNS_ENDPOINT = "notification.sns.endpoint_url"
CONFIG_SNS_REGION = "notification.sns.region"
CONFIG_AWS_ACCESS_KEY_ID = "notification.sns.aws_access_key_id"
CONFIG_AWS_SECRET_ACCESS_KEY = "notification.sns.aws_secret_access_key"
CONFIG_AWS_SESSION_TOKEN = "notification.sns.aws_session_token"


class SNSNotifier(Notifier):
    def __init__(self):
        try:
            self.update_topic = config[CONFIG_UPDATED_TOPIC]
            self.delete_topic = config[CONFIG_DELETED_TOPIC]
            region = config[CONFIG_SNS_REGION]
            endpoint = config.get(
                CONFIG_SNS_ENDPOINT, f"https://sns.{region}.amazonaws.com"
            )
            access_key = config.get(CONFIG_AWS_ACCESS_KEY_ID)
            secret_key = config.get(CONFIG_AWS_SECRET_ACCESS_KEY)
            session_token = config.get(CONFIG_AWS_SESSION_TOKEN)
            self.client = boto3.client(
                "sns",
                region_name=region,
                endpoint_url=endpoint,
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token,
            )
        except KeyError as e:
            raise MissingConfigException(e.args[0])

    async def push_stack_updated_event(self, event: StackUpdatedEvent):
        self.client.publish(
            TopicArn=self.update_topic, Message=json.dumps(event.json())
        )

    async def push_stack_deleted_event(self, event: StackDeletedEvent):
        self.client.publish(
            TopicArn=self.delete_topic, Message=json.dumps(event.json())
        )
