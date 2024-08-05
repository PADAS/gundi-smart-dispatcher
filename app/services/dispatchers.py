import base64
import uuid
import logging
import aioredis
from abc import ABC, abstractmethod
from urllib.parse import urlparse
from gundi_core import schemas
from gundi_client_v2 import GundiClient
from smartconnect import AsyncSmartClient
from gcloud.aio.storage import Storage
from smartconnect.models import SMARTRequest, SMARTCompositeRequest
from app.core import settings
from app.core.utils import find_config_for_action, RateLimiterSemaphore

_portal = GundiClient()
_redis_client = aioredis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    encoding="utf-8",
    decode_responses=True,
)
logger = logging.getLogger(__name__)


DEFAULT_TIMEOUT = (3.1, 20)
# ToDo: Implement dispatchers


class DispatcherV2(ABC):
    stream_type: schemas.v2.StreamPrefixEnum
    destination_type: schemas.DestinationTypes

    def __init__(self, integration: schemas.v2.Integration, **kwargs):
        self.integration = integration

    @abstractmethod
    async def send(self, data, **kwargs):
        ...


class SmartConnectDispatcherV2(DispatcherV2, ABC):
    DEFAULT_CONNECT_TIMEOUT_SECONDS = 10.0

    def __init__(self, integration: schemas.v2.Integration, **kwargs):
        super().__init__(integration, **kwargs)
        url_parse = urlparse(integration.base_url)
        # Looks for the configurations needed by the transformer
        # Look for the configuration of the authentication action
        self.configurations = integration.configurations
        auth_config = find_config_for_action(
            configurations=self.configurations, action_value="auth"
        )
        if not auth_config:
            raise ValueError(
                f"Authentication settings for integration {str(integration.id)} are missing. Please fix the integration setup in the portal."
            )
        self.auth_config = schemas.v2.SMARTAuthActionConfig.parse_obj(auth_config.data)
        domain = (
            f"{url_parse.hostname}:{url_parse.port}"
            if url_parse.port
            else url_parse.hostname
        )
        path = url_parse.path or "/server"
        path = path.replace("//", "/")
        api_url = (
            getattr(auth_config, "endpoint", None)
            or f"{url_parse.scheme}://{domain}{path}"
        )
        self.smart_client = AsyncSmartClient(
            api=api_url,
            username=self.auth_config.login,
            password=self.auth_config.password,
            version=self.auth_config.version,
        )


class SmartConnectEventDispatcher(SmartConnectDispatcherV2):
    def __init__(self, integration: schemas.v2.Integration, **kwargs):
        super().__init__(integration, **kwargs)
        push_events_config = find_config_for_action(
            configurations=self.configurations, action_value="push_events"
        )
        if not push_events_config:
            raise ValueError(
                f"Push Events settings for integration {str(integration.id)} are missing. Please fix the integration setup in the portal."
            )
        self.push_config = schemas.v2.SMARTPushEventActionConfig.parse_obj(
            push_events_config.data
        )

    def clean_smart_request(self, item: SMARTRequest):
        if hasattr(item.properties.smartAttributes, "observationUuid"):
            if item.properties.smartAttributes.observationUuid in ("None", None):
                item.properties.smartAttributes.observationUuid = str(uuid.uuid4())

    async def send(self, request: SMARTCompositeRequest, **kwargs):
        # Events are called Waypoints in SMART
        for waypoint_request in request.waypoint_requests:
            self.clean_smart_request(waypoint_request)
            # Todo: Ask James what this is for.
            if hasattr(
                waypoint_request.properties.smartAttributes, "observationGroups"
            ):
                for (
                    ogroup
                ) in waypoint_request.properties.smartAttributes.observationGroups:
                    for observation in ogroup.observations:
                        if observation.observationUuid in (None, "None"):
                            observation.observationUuid = None

            payload = waypoint_request.json(exclude_none=True)
            logger.debug(
                f"SmartConnectEventDispatcher > Waypoint payload: {payload}",
                extra={"payload": payload},
            )
            async with RateLimiterSemaphore(
                redis_client=_redis_client, url=self.integration.base_url
            ):
                return await self.smart_client.post_smart_request(
                    json=payload, ca_uuid=request.ca_uuid
                )


class SmartConnectEventUpdateDispatcher(SmartConnectEventDispatcher):
    async def send(self, request: SMARTCompositeRequest, **kwargs):
        # Events are called Waypoints in SMART
        result = []
        for waypoint_request in request.waypoint_requests:
            payload = waypoint_request.json(exclude_none=True)
            logger.debug(
                f"SmartConnectEventDispatcher > Waypoint payload: {payload}",
                extra={"payload": payload},
            )
            async with RateLimiterSemaphore(
                redis_client=_redis_client, url=self.integration.base_url
            ):
                response = await self.smart_client.post_smart_request(
                    json=payload, ca_uuid=request.ca_uuid
                )
                result.append(response)
        return result


########################################################################################
# GUNDI V1
########################################################################################


class SmartConnectDispatcher:
    def __init__(self, config: schemas.OutboundConfiguration):
        self.config = config

    async def clean_smart_request(self, item: SMARTRequest):

        if hasattr(item.properties.smartAttributes, "observationUuid"):
            if item.properties.smartAttributes.observationUuid in ("None", None):
                item.properties.smartAttributes.observationUuid = str(uuid.uuid4())

        if attachments := getattr(item.properties.smartAttributes, "attachments", None):
            # if the file does not already have ".data" then download and assign it.
            for file in attachments:
                if file.data.startswith("gundi:storage"):
                    stored_name = file.data.split(":")[-1]
                    async with Storage() as gcp_storage:
                        downloaded_file = await gcp_storage.download(
                            bucket=settings.BUCKET_NAME, object_name=stored_name
                        )
                    downloaded_file_base64 = base64.b64encode(downloaded_file).decode()
                    file.data = downloaded_file_base64

    async def send(self, item: dict):
        item = SMARTCompositeRequest.parse_obj(item)
        base_url = urlparse(self.config.endpoint).hostname
        # orchestration order of operations
        smartclient = AsyncSmartClient(
            api=self.config.endpoint,
            username=self.config.login,
            password=self.config.password,
            version=self.config.additional.get("version"),
        )
        for patrol_request in item.patrol_requests:
            await self.clean_smart_request(patrol_request)
            async with RateLimiterSemaphore(redis_client=_redis_client, url=base_url):
                await smartclient.post_smart_request(
                    json=patrol_request.json(exclude_none=True), ca_uuid=item.ca_uuid
                )
        for waypoint_request in item.waypoint_requests:
            await self.clean_smart_request(waypoint_request)

            # Todo: Ask James what this is for.
            if hasattr(
                waypoint_request.properties.smartAttributes, "observationGroups"
            ):
                for (
                    ogroup
                ) in waypoint_request.properties.smartAttributes.observationGroups:
                    for observation in ogroup.observations:
                        if observation.observationUuid in (None, "None"):
                            observation.observationUuid = None

            payload = waypoint_request.json(exclude_none=True)
            logger.debug("Waypoint payload.", extra={"payload": payload})
            async with RateLimiterSemaphore(redis_client=_redis_client, url=base_url):
                await smartclient.post_smart_request(json=payload, ca_uuid=item.ca_uuid)
        for track_point_request in item.track_point_requests:
            await self.clean_smart_request(track_point_request)
            async with RateLimiterSemaphore(redis_client=_redis_client, url=base_url):
                await smartclient.post_smart_request(
                    json=track_point_request.json(exclude_none=True),
                    ca_uuid=item.ca_uuid,
                )
        return


########################################################################################

dispatcher_cls_by_type = {
    # Gundi v1
    schemas.v1.StreamPrefixEnum.geoevent: SmartConnectDispatcher,
    schemas.v1.StreamPrefixEnum.earthranger_event: SmartConnectDispatcher,
    schemas.v1.StreamPrefixEnum.earthranger_patrol: SmartConnectDispatcher,
    # Gundi v2
    schemas.v2.StreamPrefixEnum.event: SmartConnectEventDispatcher,
    schemas.v2.StreamPrefixEnum.event_update: SmartConnectEventUpdateDispatcher,
    # ToDo: Support Patrols and Observations
}
