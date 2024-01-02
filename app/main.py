import base64
import json
import logging
import os
from fastapi import FastAPI, Request, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import app.settings as settings
from fastapi.middleware.cors import CORSMiddleware


# For running behind a proxy, we'll want to configure the root path for OpenAPI browser.
root_path = os.environ.get("ROOT_PATH", "")
app = FastAPI(
    title="Gundi Integration Actions Execution Service",
    description="API to trigger actions against third-party systems",
    version="1",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


@app.get(
    "/",
    tags=["health-check"],
    summary="Check that the service is healthy",
)
def health_check(
    request: Request,
):
    return {"status": "healthy"}


@app.post(
    "/",
    summary="Process a message from Pub/Sub",
)
async def process_message(
    request: Request,
):
    body = await request.body()
    print(f"Message Received. RAW body: {body}")
    json_data = await request.json()
    print(f"JSON: {json_data}")
    payload = base64.b64decode(json_data["message"]["data"]).decode("utf-8").strip()
    print(f"Payload: {payload}")
    json_payload = json.loads(payload)
    print(f"JSON Payload: {json_payload}")
    # ToDo: run dispatcher
    return {}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    logger.debug(
        "Failed handling body: %s",
        jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
