from typing import ClassVar

from pyrovision.api.exceptions import StackNotFoundException
from pyrovision.api.notification.service import Notifier
from pyrocore.model.events.stack import StackDeletedEvent, StackUpdatedEvent
from pyrocore.model.plan import Plan
from pyrocore.model.responses.responses import (
    ListStacksResponse,
    CreateStackResponse,
)
from pyrocore.model.state import State
from pyrocore.model.stack import Stack
from pyrovision.api.store.stacks import StackStore
from pyrovision.api.terraform.client import TerraformClient as TerraformClientABC


class Controller:
    store = StackStore.create()
    TerraformClient: ClassVar[TerraformClientABC] = TerraformClientABC.get_class()
    notifier = Notifier.create()

    async def plan(self, stack: Stack, destroy: bool = False):
        tf = self.TerraformClient(workspace=stack.id)
        plan = tf.plan(stack, destroy)
        return plan

    async def destroy(self, stack: Stack) -> Plan:
        tf = self.TerraformClient(workspace=stack.id)
        plan = tf.destroy(stack)
        self.store.delete(stack.id)

        # Push event
        await self.notifier.push_stack_deleted_event(
            StackDeletedEvent.from_payload({"stack": stack})
        )
        return plan

    async def get_state(self, stack_id: str) -> State:
        tf = self.TerraformClient(workspace=stack_id)
        state = tf.get(stack_id)
        return state

    async def list_stacks(self, token: str) -> ListStacksResponse:
        return self.store.list(token)

    async def get_stack(self, stack_id: str) -> Stack:
        stack = self.store.get(stack_id)
        if not stack:
            raise StackNotFoundException(stack_id)
        return stack

    async def create_stack(self, stack: Stack) -> CreateStackResponse:
        tf = self.TerraformClient(workspace=stack.id)
        outputs = tf.apply(stack)
        stack.outputs = outputs
        self.store.save(stack)

        # Push event
        await self.notifier.push_stack_updated_event(
            StackUpdatedEvent.from_payload({"stack": stack})
        )
        return CreateStackResponse(stack=stack)
