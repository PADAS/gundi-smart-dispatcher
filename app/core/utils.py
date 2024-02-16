# ToDo: Move base classes or utils into some common package?
import asyncio
import base64
import json
from typing import Union

import aiohttp
import logging
import httpx
import backoff
import aioredis
import aiohttp
import logging
from enum import Enum
from gundi_core import schemas as gundi_schemas
from gundi_core.schemas import v2 as gundi_schemas_v2
from gundi_core.events import SystemEventBaseModel
from redis import exceptions as redis_exceptions
from gcloud.aio import pubsub
from uuid import UUID
from gundi_core import schemas
from app import settings
from gundi_client import PortalApi
from gundi_client_v2 import GundiClient
from . import settings, errors


logger = logging.getLogger(__name__)


def get_redis_db():
    logger.debug(
        f"Connecting to REDIS DB :{settings.REDIS_DB} at {settings.REDIS_HOST}:{settings.REDIS_PORT}"
    )
    return aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf-8",
        decode_responses=True,
    )


_cache_ttl = settings.PORTAL_CONFIG_OBJECT_CACHE_TTL
_cache_db = get_redis_db()
_portal = PortalApi()
connect_timeout, read_timeout = settings.DEFAULT_REQUESTS_TIMEOUT


async def read_config_from_cache_safe(cache_key, extra_dict):
    try:
        config = await _cache_db.get(cache_key)
    except redis_exceptions.ConnectionError as e:
        logger.warning(
            f"ConnectionError while reading integration configuration from Cache: {e}",
            extra={**extra_dict},
        )
        config = None
    except Exception as e:
        logger.warning(
            f"Unknown Error while reading integration configuration from Cache: {e}",
            extra={**extra_dict},
        )
        config = None
    finally:
        return config


async def write_config_in_cache_safe(key, ttl, config, extra_dict):
    try:
        await _cache_db.setex(key, ttl, config.json())
    except redis_exceptions.ConnectionError as e:
        logger.warning(
            f"ConnectionError while writing integration configuration to Cache: {e}",
            extra={**extra_dict},
        )
    except Exception as e:
        logger.warning(
            f"Unknown Error while writing integration configuration to Cache: {e}",
            extra={**extra_dict},
        )


@backoff.on_exception(backoff.expo, (httpx.HTTPError,), max_tries=5)
async def get_integration_details(integration_id: str) -> gundi_schemas.v2.Integration:
    """
    Helper function to retrieve integration configurations from Gundi API v2
    """

    if not integration_id:
        raise ValueError("integration_id must not be None")

    extra_dict = {
        ExtraKeys.AttentionNeeded: True,
        ExtraKeys.OutboundIntId: str(integration_id),
    }

    # Retrieve from cache if possible
    cache_key = f"integration_details.{integration_id}"
    cached = await read_config_from_cache_safe(
        cache_key=cache_key, extra_dict=extra_dict
    )

    if cached:
        config = gundi_schemas.v2.Integration.parse_raw(cached)
        logger.debug(
            "Using cached integration details",
            extra={
                **extra_dict,
                ExtraKeys.AttentionNeeded: False,
                "integration_detail": config,
            },
        )
        return config

    # Retrieve details from the portal
    logger.debug(f"Cache miss for integration details.", extra={**extra_dict})
    connect_timeout, read_timeout = settings.DEFAULT_REQUESTS_TIMEOUT
    async with GundiClient(
        connect_timeout=connect_timeout, data_timeout=read_timeout
    ) as portal_v2:
        try:
            integration = await portal_v2.get_integration_details(
                integration_id=integration_id
            )
        # ToDo: Catch more specific exceptions once the gundi client supports them
        except Exception as e:
            error_msg = (
                f"Error retrieving integration details from the portal (v2): {e}"
            )
            logger.error(
                error_msg,
                extra=extra_dict,
            )
            raise e
        else:
            if integration:  # don't cache empty response
                await write_config_in_cache_safe(
                    key=cache_key,
                    ttl=_cache_ttl,
                    config=integration,
                    extra_dict=extra_dict,
                )
            return integration


@backoff.on_exception(backoff.expo, (httpx.HTTPError,), max_tries=5)
async def get_inbound_integration_detail(
    integration_id: Union[str, UUID],
) -> schemas.IntegrationInformation:
    if not integration_id:
        raise ValueError("integration_id must not be None")

    extra_dict = {
        ExtraKeys.AttentionNeeded: True,
        ExtraKeys.InboundIntId: str(integration_id),
    }

    cache_key = f"inbound_detail.{integration_id}"
    cached = await _cache_db.get(cache_key)

    if cached:
        config = schemas.IntegrationInformation.parse_raw(cached)
        logger.debug(
            "Using cached inbound integration detail",
            extra={**extra_dict, "integration_detail": config},
        )
        return config

    logger.debug(f"Cache miss for inbound integration detai", extra={**extra_dict})

    connect_timeout, read_timeout = settings.DEFAULT_REQUESTS_TIMEOUT
    timeout_settings = aiohttp.ClientTimeout(
        sock_connect=connect_timeout, sock_read=read_timeout
    )
    async with aiohttp.ClientSession(
        timeout=timeout_settings, raise_for_status=True
    ) as s:
        try:
            response = await _portal.get_inbound_integration(
                session=s, integration_id=str(integration_id)
            )
        except aiohttp.ServerTimeoutError as e:
            # ToDo: Try to get the url from the exception or from somewhere else
            target_url = (
                f"{settings.PORTAL_INBOUND_INTEGRATIONS_ENDPOINT}/{str(integration_id)}"
            )
            logger.error(
                "Read Timeout",
                extra={**extra_dict, ExtraKeys.Url: target_url},
            )
            raise errors.ReferenceDataError(f"Read Timeout for {target_url}")
        except aiohttp.ClientResponseError as e:
            target_url = str(e.request_info.url)
            logger.exception(
                "Portal returned bad response during request for inbound config detail",
                extra={
                    ExtraKeys.AttentionNeeded: True,
                    ExtraKeys.InboundIntId: integration_id,
                    ExtraKeys.Url: target_url,
                    ExtraKeys.StatusCode: e.status,
                },
            )
            raise errors.ReferenceDataError(
                f"Request for InboundIntegration({integration_id})"
            )
        else:
            try:
                config = schemas.IntegrationInformation.parse_obj(response)
            except Exception:
                logger.error(
                    f"Failed decoding response for InboundIntegration Detail",
                    extra={**extra_dict, "resp_text": response},
                )
                raise errors.ReferenceDataError(
                    "Failed decoding response for InboundIntegration Detail"
                )
            else:
                if config:  # don't cache empty response
                    await _cache_db.setex(cache_key, _cache_ttl, config.json())
                return config


@backoff.on_exception(backoff.expo, (httpx.HTTPError,), max_tries=5)
async def get_outbound_config_detail(
    outbound_id: Union[str, UUID],
) -> schemas.OutboundConfiguration:
    if not outbound_id:
        raise ValueError("integration_id must not be None")

    extra_dict = {
        ExtraKeys.AttentionNeeded: True,
        ExtraKeys.OutboundIntId: str(outbound_id),
    }

    cache_key = f"outbound_detail.{outbound_id}"
    cached = await _cache_db.get(cache_key)

    if cached:
        config = schemas.OutboundConfiguration.parse_raw(cached)
        logger.debug(
            "Using cached outbound integration detail",
            extra={
                **extra_dict,
                ExtraKeys.AttentionNeeded: False,
                "outbound_detail": config,
            },
        )
        return config

    logger.debug(f"Cache miss for outbound integration detail", extra={**extra_dict})

    connect_timeout, read_timeout = settings.DEFAULT_REQUESTS_TIMEOUT
    timeout_settings = aiohttp.ClientTimeout(
        sock_connect=connect_timeout, sock_read=read_timeout
    )
    async with aiohttp.ClientSession(
        timeout=timeout_settings, raise_for_status=True
    ) as s:
        try:
            response = await _portal.get_outbound_integration(
                session=s, integration_id=str(outbound_id)
            )
        except aiohttp.ServerTimeoutError as e:
            target_url = (
                f"{settings.PORTAL_OUTBOUND_INTEGRATIONS_ENDPOINT}/{str(outbound_id)}"
            )
            logger.error(
                "Read Timeout",
                extra={**extra_dict, ExtraKeys.Url: target_url},
            )
            raise errors.ReferenceDataError(f"Read Timeout for {target_url}")
        except aiohttp.ClientConnectionError as e:
            target_url = str(settings.PORTAL_OUTBOUND_INTEGRATIONS_ENDPOINT)
            logger.error(
                "Connection Error",
                extra={**extra_dict, ExtraKeys.Url: target_url},
            )
            raise errors.ReferenceDataError(
                f"Failed to connect to the portal at {target_url}, {e}"
            )
        except aiohttp.ClientResponseError as e:
            target_url = str(e.request_info.url)
            logger.exception(
                "Portal returned bad response during request for outbound config detail",
                extra={
                    ExtraKeys.AttentionNeeded: True,
                    ExtraKeys.OutboundIntId: outbound_id,
                    ExtraKeys.Url: target_url,
                    ExtraKeys.StatusCode: e.status,
                },
            )
            raise errors.ReferenceDataError(
                f"Request for OutboundIntegration({outbound_id}) returned bad response"
            )
        else:
            try:
                config = schemas.OutboundConfiguration.parse_obj(response)
            except Exception:
                logger.error(
                    f"Failed decoding response for Outbound Integration Detail",
                    extra={**extra_dict, "resp_text": response},
                )
                raise errors.ReferenceDataError(
                    "Failed decoding response for Outbound Integration Detail"
                )
            else:
                if config:  # don't cache empty response
                    await _cache_db.setex(cache_key, _cache_ttl, config.json())
                return config


async def get_dispatched_observation(
    gundi_id: str, destination_id: str
) -> gundi_schemas_v2.DispatchedObservation:
    """
    Helper function that looks into the cache for dispatched observations
    """
    observation = None
    extra_dict = {ExtraKeys.GundiId: gundi_id, ExtraKeys.OutboundIntId: destination_id}
    try:
        cache_key = f"dispatched_observation.{gundi_id}.{destination_id}"
        cached_data = _cache_db.get(cache_key)
        if cached_data:
            observation = gundi_schemas_v2.DispatchedObservation.parse_raw(cached_data)
        else:  # Try to rebuild the cache entry
            # Retrieve traces from the portal
            logger.debug(
                f"Cache miss for dispatched observation.", extra={**extra_dict}
            )
            connect_timeout, read_timeout = settings.DEFAULT_REQUESTS_TIMEOUT
            async with GundiClient(
                connect_timeout=connect_timeout, data_timeout=read_timeout
            ) as portal_v2:
                try:
                    filters = {
                        "object_id": gundi_id,
                        "destination_id": destination_id,
                    }
                    traces = await portal_v2.get_traces(params=filters)
                    observation_trace = traces[0]
                # ToDo: Catch more specific exceptions once the gundi client supports them
                except Exception as e:
                    error_msg = f"Error retrieving traces from the portal (v2): {e}"
                    logger.error(
                        error_msg,
                        extra={**extra_dict, **filters},
                    )
                    return None
                else:
                    # Rebuild from the trace
                    observation = gundi_schemas_v2.DispatchedObservation(
                        gundi_id=observation_trace.object_id,
                        related_to=observation_trace.related_to,
                        external_id=observation_trace.external_id,
                        data_provider_id=observation_trace.data_provider,
                        destination_id=observation_trace.destination,
                        delivered_at=observation_trace.delivered_at,
                    )
                    # Save in cache again
                    await cache_dispatched_observation(observation=observation)
    except redis_exceptions.ConnectionError as e:
        logger.error(
            f"ConnectionError while reading dispatched observations from Cache: {e}",
            extra={**extra_dict},
        )
    except Exception as e:
        logger.error(
            f"Internal Error while reading dispatched observations from Cache: {e}",
            extra={**extra_dict},
        )
    finally:
        return observation


async def cache_dispatched_observation(
    observation: gundi_schemas_v2.DispatchedObservation,
):
    try:
        gundi_id = str(observation.gundi_id)
        destination_id = str(observation.destination_id)

        if not gundi_id or not destination_id:
            return  # Can't build the key

        extra_dict = {
            ExtraKeys.GundiId: gundi_id,
            ExtraKeys.OutboundIntId: destination_id,
        }
        cache_key = f"dispatched_observation.{gundi_id}.{destination_id}"
        await _cache_db.setex(
            name=cache_key,
            time=settings.DISPATCHED_OBSERVATIONS_CACHE_TTL,
            value=observation.json(),
        )
    except redis_exceptions.ConnectionError as e:
        logger.warning(
            f"ConnectionError while writing integration configuration to Cache: {e}",
            extra=extra_dict,
        )
    except Exception as e:
        logger.warning(
            f"Unknown Error while writing integration configuration to Cache: {e}",
            extra=extra_dict,
        )


def extract_fields_from_message(message):
    if message:
        data = base64.b64decode(message.get("data", "").encode("utf-8"))
        observation = json.loads(data)
        attributes = message.get("attributes")
        if not observation:
            logger.warning(f"No observation was obtained from {message}")
        if not attributes:
            logger.debug(f"No attributes were obtained from {message}")
    else:
        logger.warning(f"message contained no payload", extra={"message": message})
        return None, None
    return observation, attributes


class ExtraKeys(str, Enum):
    def __str__(self):
        return str(self.value)

    DeviceId = "device_id"
    InboundIntId = "inbound_integration_id"
    OutboundIntId = "outbound_integration_id"
    AttentionNeeded = "attention_needed"
    StreamType = "stream_type"
    Provider = "provider"
    Error = "error"
    Url = "url"
    Observation = "observation"
    RetryTopic = "retry_topic"
    RetryAt = "retry_at"
    RetryAttempt = "retry_attempt"
    StatusCode = "status_code"
    DeadLetter = "dead_letter"
    GundiId = "gundi_id"
    RelatedTo = "related_to"


def is_null(value):
    return value in {None, "", "None", "null"}


def find_config_for_action(configurations, action_value):
    return next(
        (config for config in configurations if config.action.value == action_value),
        None,
    )


# Events for other services or system components
@backoff.on_exception(
    backoff.expo, (aiohttp.ClientError, asyncio.TimeoutError), max_tries=5
)
async def publish_event(event: SystemEventBaseModel, topic_name: str):
    timeout_settings = aiohttp.ClientTimeout(total=10.0)
    async with aiohttp.ClientSession(
        raise_for_status=True, timeout=timeout_settings
    ) as session:
        client = pubsub.PublisherClient(session=session)
        # Get the topic
        topic = client.topic_path(settings.GCP_PROJECT_ID, topic_name)
        # Prepare the payload
        binary_payload = json.dumps(event.dict(), default=str).encode("utf-8")
        messages = [pubsub.PubsubMessage(binary_payload)]
        logger.debug(f"Sending event {event} to PubSub topic {topic_name}..")
        try:  # Send to pubsub
            response = await client.publish(topic, messages)
        except Exception as e:
            logger.exception(
                f"Error publishing system event topic {topic_name}: {e}. This will be retried."
            )
            raise e
        else:
            logger.debug(f"System event {event} published successfully.")
            logger.debug(f"GCP PubSub response: {response}")


class RateLimiterSemaphore:
    def __init__(self, redis_client, url, **kwargs):
        self.url = url
        self.max_requests = kwargs.get("max_requests", settings.MAX_REQUESTS)
        self.max_requests_time_window_sec = kwargs.get(
            "max_requests_time_window_sec", settings.MAX_REQUESTS_TIME_WINDOW_SEC
        )
        self.redis_client = redis_client

    # Support using this as an async context manager.
    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.release()

    async def acquire(self, auto_release=True):
        """
        Try to acquire the counter semaphore:
            - Increase the number of requests made in the last time window
            - If the number of requests is greater than the limit, raise an exception
        """
        async with self.redis_client.pipeline(transaction=True) as pipe:
            operations = pipe.incr(self.url)
            if auto_release:
                operations = operations.expire(
                    self.url, self.max_requests_time_window_sec
                )
            res = await operations.execute()
        logger.debug(
            f"RateLimiterSemaphore<{self.url}>: {res[0]}/{self.max_requests} requests"
        )
        if res[0] > self.max_requests:
            raise errors.TooManyRequests(
                f"Too many requests in the last {self.max_requests_time_window_sec} seconds: {res[0]}"
            )

    async def release(self):
        """
        Release the semaphore:
            - Decrease the number of requests made in the last time window
        """
        await self.redis_client.decr(self.url)

    async def get_requests_count(self) -> int:
        """
        Get the number of requests made in the last time window
        """
        count = await self.redis_client.get(self.url)
        if count:
            return int(count)
        else:
            return 0

    def __str__(self):
        return f"RateLimiterSemaphore<{self.url}>: {self.max_requests}/{self.max_requests_time_window_sec} sec"

    def __repr__(self):
        return self.__str__()
