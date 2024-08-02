from opentelemetry.propagators.cloud_trace_propagator import (
    CloudTraceFormatPropagator,
)
from opentelemetry.propagate import set_global_textmap
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from app.core import settings
from . import config
from . import pubsub_instrumentation

if settings.TRACING_ENABLED:
    # Capture requests (sync and async)
    RequestsInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
else:
    RequestsInstrumentor().uninstrument()
    AioHttpClientInstrumentor().uninstrument()
    HTTPXClientInstrumentor().uninstrument()
# Using the X-Cloud-Trace-Context header
set_global_textmap(CloudTraceFormatPropagator())
tracer = config.configure_tracer(name="smart-dispatcher", version="0.1.0")
