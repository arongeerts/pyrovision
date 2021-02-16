import traceback
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from pyrovision.api.controller import Controller
from pyrovision.api.exceptions import StackNotFoundException, TerraformOperationFailed
from pyrocore.model.stack import Stack
from pyrovision.api.terraform.client import TerraformClient

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
controller = Controller()


@app.on_event("startup")
def init():
    TerraformClient.get_class().init()


@app.get("/")
async def hello():
    return {"detail": "PyroVision is running"}


@app.post("/stacks/plan")
async def plan_stack(stack: Stack):
    return await controller.plan(stack)


@app.post("/stacks")
async def create_stack(stack: Stack):
    return await controller.create_stack(stack)


@app.delete("/stacks/plan/{stack_id}")
async def plan_destroy(stack_id: str):
    stack = await controller.get_stack(stack_id)
    return await controller.plan(stack, destroy=True)


@app.delete("/stacks/{stack_id}")
async def destroy(stack_id: str):
    stack = await controller.get_stack(stack_id)
    return await controller.destroy(stack)


@app.get("/stacks/{stack_id}")
async def get_stack(stack_id: str):
    return await controller.get_stack(stack_id)


@app.get("/stacks")
async def list_stacks(continuation_token: Optional[str] = None):
    return await controller.list_stacks(continuation_token)


@app.exception_handler(StackNotFoundException)
def handle_stack_not_found(request: Request, exc: StackNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"Stack with ID '{exc.stack_id}' not found"},
    )


@app.exception_handler(TerraformOperationFailed)
def handle_tf_operation_failed(request: Request, exc: TerraformOperationFailed):
    return JSONResponse(
        status_code=409,
        content={
            "message": f"Execution of command {exc.cmd} failed with error: \n{exc.message}"
        },
    )


@app.exception_handler(Exception)
def handle_generic_exception(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": f"Operation failed with '{exc.__class__}': {str(exc)}"},
    )


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8080, log_level="info")
