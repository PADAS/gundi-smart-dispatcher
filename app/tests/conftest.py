import datetime
import pytest
import asyncio
import gundi_core.schemas.v2 as schemas_v2
from smartconnect import SMARTClientException
from gundi_core import events as system_events
from gcloud.aio import pubsub
from app.core import settings


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


@pytest.fixture
def mock_cache(mocker):
    mock_cache = mocker.MagicMock()
    mock_cache.get.return_value = async_return(None)
    mock_cache.setex.return_value = async_return(None)
    mock_cache.incr.return_value = mock_cache
    mock_cache.decr.return_value = async_return(None)
    mock_cache.expire.return_value = mock_cache
    mock_cache.execute.return_value = async_return((1, True))
    mock_cache.__aenter__.return_value = mock_cache
    mock_cache.__aexit__.return_value = None
    mock_cache.pipeline.return_value = mock_cache
    return mock_cache


@pytest.fixture
def mock_cache_with_rate_limit_exceeded(mock_cache):
    mock_cache.execute.return_value = async_return(
        (4, True)
    )  # 3 req/sec is the default limit
    return mock_cache


@pytest.fixture
def observation_delivered_pubsub_message():
    return pubsub.PubsubMessage(
        b'{"event_id": "c05cf942-f543-4798-bd91-0e38a63d655e", "timestamp": "2023-07-12 20:34:07.210731+00:00", "schema_version": "v1", "payload": {"gundi_id": "23ca4b15-18b6-4cf4-9da6-36dd69c6f638", "related_to": "None", "external_id": "7f42ab47-fa7a-4a7e-acc6-cadcaa114646", "data_provider_id": "ddd0946d-15b0-4308-b93d-e0470b6d33b6", "destination_id": "338225f3-91f9-4fe1-b013-353a229ce504", "delivered_at": "2023-07-12 20:34:07.210542+00:00"}, "event_type": "ObservationDelivered"}'
    )


@pytest.fixture
def observation_delivery_failure_pubsub_message():
    return pubsub.PubsubMessage(
        b'{"event_id": "61e9c40b-60c2-4279-abeb-c918dc5d6442", "timestamp": "2024-01-08 19:51:42.750821+00:00", "schema_version": "v1", "payload": {"gundi_id": "3a09e9c8-525a-4431-a43e-12a9830f688e", "related_to": "None", "external_id": null, "data_provider_id": "d88ac520-2bf6-4e6b-ab09-38ed1ec6947a", "destination_id": "b42c9205-5228-49e0-a75b-ebe5b6a9f78e", "delivered_at": "2024-01-08 19:51:42.750646+00:00"}, "event_type": "ObservationDeliveryFailed"}'
    )


@pytest.fixture
def mock_pubsub_client(
    mocker, observation_delivered_pubsub_message, gcp_pubsub_publish_response
):
    mock_client = mocker.MagicMock()
    mock_publisher = mocker.MagicMock()
    mock_publisher.publish.return_value = async_return(gcp_pubsub_publish_response)
    mock_publisher.topic_path.return_value = (
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}"
    )
    mock_client.PublisherClient.return_value = mock_publisher
    mock_client.PubsubMessage.return_value = observation_delivered_pubsub_message
    return mock_client


@pytest.fixture
def mock_pubsub_client_with_observation_delivery_failure(
    mocker, observation_delivery_failure_pubsub_message, gcp_pubsub_publish_response
):
    mock_client = mocker.MagicMock()
    mock_publisher = mocker.MagicMock()
    mock_publisher.publish.return_value = async_return(gcp_pubsub_publish_response)
    mock_publisher.topic_path.return_value = (
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}"
    )
    mock_client.PublisherClient.return_value = mock_publisher
    mock_client.PubsubMessage.return_value = observation_delivery_failure_pubsub_message
    return mock_client


@pytest.fixture
def mock_get_cloud_storage(mocker):
    return mocker.MagicMock()


@pytest.fixture
def post_report_response():
    return {}


@pytest.fixture
def smartclient_post_smart_request_response():
    return {}


@pytest.fixture
def gcp_pubsub_publish_response():
    return {"messageIds": ["7061707768812258"]}


@pytest.fixture
def mock_gundi_client_v2(
    mocker,
    smart_integration_v2,
):
    mock_client = mocker.MagicMock()
    mock_client.get_integration_details.return_value = async_return(
        smart_integration_v2
    )
    mock_client.__aenter__.return_value = mock_client
    return mock_client


@pytest.fixture
def mock_gundi_client_v2_class(mocker, mock_gundi_client_v2):
    mock_gundi_client_v2_class = mocker.MagicMock()
    mock_gundi_client_v2_class.return_value = mock_gundi_client_v2
    return mock_gundi_client_v2_class


@pytest.fixture
def event_v2_cloud_event_payload():
    return {
        "message": {
            "attributes": {
                "annotations": "{}",
                "data_provider_id": "88ac5e9c-a3f0-47ff-9382-58d0abfa95f3",
                "destination_id": "58c44611-e356-4e4d-82bb-26f50f1fc1e8",
                "external_source_id": "default-source",
                "gundi_id": "44eaf798-fa87-48d9-9baf-42dfdb4c6231",
                "gundi_version": "v2",
                "provider_key": "gundi_cellstop_88ac5e9c-a3f0-47ff-9382-58d0abfa95f3",
                "related_to": "",
                "source_id": "e702598d-42d0-4094-8d1e-856caca4926e",
                "stream_type": "ev",
                "tracing_context": "{}",
            },
            "data": "eyJjYV91dWlkIjogIjRiMjMyNDJhLTExNjEtNDZjMy1hZjg0LTVlMzVkYzgwMWM0MyIsICJwYXRyb2xfcmVxdWVzdHMiOiBbXSwgIndheXBvaW50X3JlcXVlc3RzIjogW3sidHlwZSI6ICJGZWF0dXJlIiwgImdlb21ldHJ5IjogeyJjb29yZGluYXRlcyI6IFstNzIuNzA0NDI1LCAtNTEuNjg4NjQ1XX0sICJwcm9wZXJ0aWVzIjogeyJkYXRlVGltZSI6ICIyMDI0LTAxLTA4VDA5OjUxOjE0IiwgInNtYXJ0RGF0YVR5cGUiOiAiaW5jaWRlbnQiLCAic21hcnRGZWF0dXJlVHlwZSI6ICJ3YXlwb2ludC9uZXciLCAic21hcnRBdHRyaWJ1dGVzIjogeyJvYnNlcnZhdGlvbkdyb3VwcyI6IFt7Im9ic2VydmF0aW9ucyI6IFt7Im9ic2VydmF0aW9uVXVpZCI6ICI0NGVhZjc5OC1mYTg3LTQ4ZDktOWJhZi00MmRmZGI0YzYyMzEiLCAiY2F0ZWdvcnkiOiAiYW5pbWFscy5zaWduIiwgImF0dHJpYnV0ZXMiOiB7InNwZWNpZXMiOiAibGlvbiJ9fV19XSwgInBhdHJvbFV1aWQiOiBudWxsLCAicGF0cm9sTGVnVXVpZCI6IG51bGwsICJwYXRyb2xJZCI6IG51bGwsICJpbmNpZGVudElkIjogImd1bmRpX2V2XzQ0ZWFmNzk4LWZhODctNDhkOS05YmFmLTQyZGZkYjRjNjIzMSIsICJpbmNpZGVudFV1aWQiOiAiNDRlYWY3OTgtZmE4Ny00OGQ5LTliYWYtNDJkZmRiNGM2MjMxIiwgInRlYW0iOiBudWxsLCAib2JqZWN0aXZlIjogbnVsbCwgImNvbW1lbnQiOiAiUmVwb3J0OiBBbmltYWxzIFNpZ25cbkltcG9ydGVkOiAyMDI0LTAxLTA4VDEwOjQwOjU5LjU4MzE4MC0wMzowMCIsICJpc0FybWVkIjogbnVsbCwgInRyYW5zcG9ydFR5cGUiOiBudWxsLCAibWFuZGF0ZSI6IG51bGwsICJudW1iZXIiOiBudWxsLCAibWVtYmVycyI6IG51bGwsICJsZWFkZXIiOiBudWxsLCAiYXR0YWNobWVudHMiOiBudWxsfX19XSwgInRyYWNrX3BvaW50X3JlcXVlc3RzIjogW119",  # pragma: allowlist secret
            "messageId": "9155786613739819",
            "message_id": "9155786613739819",
            "publishTime": "2024-01-08T13:40:59.649Z",
            "publish_time": "2024-01-08T13:40:59.649Z",
        },
        "subscription": "projects/cdip-stage-78ca/subscriptions/eventarc-us-central1-smart-dispatcher-topic-test-trigger-1zb7crbq-sub-909",
    }


@pytest.fixture
def event_v2_cloud_event_headers():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return {
        "host": "smart-dispatcher-jabcutl7za-uc.a.run.app",
        "content-type": "application/json",
        "authorization": "Bearer fake-token",
        "content-length": "2057",
        "accept": "application/json",
        "from": "noreply@google.com",
        "user-agent": "APIs-Google; (+https://developers.google.com/webmasters/APIs-Google.html)",
        "x-cloud-trace-context": "",
        "traceparent": "",
        "x-forwarded-for": "64.233.172.137",
        "x-forwarded-proto": "https",
        "forwarded": 'for="64.233.172.137";proto=https',
        "accept-encoding": "gzip, deflate, br",
        "ce-id": "10090163454824830",
        "ce-source": "//pubsub.googleapis.com/projects/cdip-stage-78ca/topics/smart-dispatcher-topic-test",
        "ce-specversion": "1.0",
        "ce-type": "google.cloud.pubsub.topic.v1.messagePublished",
        "ce-time": timestamp,
    }


@pytest.fixture
def mock_smartclient(
    mocker,
    smartclient_post_smart_request_response,
):
    mock_client = mocker.MagicMock()
    mock_client.post_smart_request.return_value = async_return(
        smartclient_post_smart_request_response
    )
    mock_client.__aenter__.return_value = mock_client
    return mock_client


@pytest.fixture
def mock_smartclient_with_400_response(
    mocker,
):
    mock_client = mocker.MagicMock()
    error = SMARTClientException(
        "SMART request failed for https://fakesmartconnectsite.smartconservationtools.org/server/api/data/4b23242a-1161-46c3-af84-5e35dc801c43 with response code 400"
    )
    mock_client.post_smart_request.side_effect = error
    mock_client.__aenter__.return_value = mock_client
    return mock_client


@pytest.fixture
def mock_smartclient_class(mocker, mock_smartclient):
    mock_smartclient_class = mocker.MagicMock()
    mock_smartclient_class.return_value = mock_smartclient
    return mock_smartclient_class


@pytest.fixture
def mock_smartclient_class_with_400_response(
    mocker, mock_smartclient_with_400_response
):
    mock_smartclient_class = mocker.MagicMock()
    mock_smartclient_class.return_value = mock_smartclient_with_400_response
    return mock_smartclient_class


@pytest.fixture
def smart_integration_v2():
    return schemas_v2.Integration.parse_obj(
        {
            "id": "b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
            "name": "Gundi Test CA - SMART Connect",
            "type": {
                "id": "265922fa-4682-4157-a055-d3ce3f12eea3",
                "name": "SMART Connect",
                "value": "smart_connect",
                "description": "",
                "actions": [
                    {
                        "id": "b0a0e7ed-d668-41b5-96d2-397f026c4ecb",
                        "type": "auth",
                        "name": "Authenticate",
                        "value": "auth",
                        "description": "Authenticate against smart",
                        "action_schema": {
                            "type": "object",
                            "title": "SMARTAuthActionConfig",
                            "required": ["login", "password"],
                            "properties": {
                                "login": {"type": "string", "title": "Login"},
                                "endpoint": {"type": "string", "title": "Endpoint"},
                                "password": {"type": "string", "title": "Password"},
                            },
                        },
                    },
                    {
                        "id": "ebe72917-c112-4064-9f38-707bbd14a50f",
                        "type": "push",
                        "name": "Push Events",
                        "value": "push_events",
                        "description": "Send Events to SMART Connect (a.k.a Incidents or waypoints)",
                        "action_schema": {
                            "type": "object",
                            "title": "SMARTPushEventActionConfig",
                            "properties": {
                                "ca_uuid": {
                                    "type": "string",
                                    "title": "Ca Uuid",
                                    "format": "uuid",
                                },
                                "version": {"type": "string", "title": "Version"},
                                "ca_uuids": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uuid"},
                                    "title": "Ca Uuids",
                                },
                                "transformation_rules": {
                                    "$ref": "#/definitions/TransformationRules"
                                },
                                "configurable_models_lists": {
                                    "type": "object",
                                    "title": "Configurable Models Lists",
                                },
                                "configurable_models_enabled": {
                                    "type": "array",
                                    "items": {"type": "string", "format": "uuid"},
                                    "title": "Configurable Models Enabled",
                                },
                            },
                            "definitions": {
                                "OptionMap": {
                                    "type": "object",
                                    "title": "OptionMap",
                                    "required": ["from_key", "to_key"],
                                    "properties": {
                                        "to_key": {"type": "string", "title": "To Key"},
                                        "from_key": {
                                            "type": "string",
                                            "title": "From Key",
                                        },
                                    },
                                },
                                "CategoryPair": {
                                    "type": "object",
                                    "title": "CategoryPair",
                                    "required": ["event_type", "category_path"],
                                    "properties": {
                                        "event_type": {
                                            "type": "string",
                                            "title": "Event Type",
                                        },
                                        "category_path": {
                                            "type": "string",
                                            "title": "Category Path",
                                        },
                                    },
                                },
                                "AttributeMapper": {
                                    "type": "object",
                                    "title": "AttributeMapper",
                                    "required": ["from_key", "to_key"],
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "title": "Type",
                                            "default": "string",
                                        },
                                        "to_key": {"type": "string", "title": "To Key"},
                                        "from_key": {
                                            "type": "string",
                                            "title": "From Key",
                                        },
                                        "event_types": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "title": "Event Types",
                                        },
                                        "options_map": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/definitions/OptionMap"
                                            },
                                            "title": "Options Map",
                                        },
                                        "default_option": {
                                            "type": "string",
                                            "title": "Default Option",
                                        },
                                    },
                                },
                                "TransformationRules": {
                                    "type": "object",
                                    "title": "TransformationRules",
                                    "properties": {
                                        "category_map": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/definitions/CategoryPair"
                                            },
                                            "title": "Category Map",
                                            "default": [],
                                        },
                                        "attribute_map": {
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/definitions/AttributeMapper"
                                            },
                                            "title": "Attribute Map",
                                            "default": [],
                                        },
                                    },
                                },
                            },
                        },
                    },
                ],
            },
            "base_url": "https://fakesmartconnectsite.smartconservationtools.org",
            "enabled": True,
            "owner": {
                "id": "a91b400b-482a-4546-8fcb-ee42b01deeb6",
                "name": "Test Org",
                "description": "",
            },
            "configurations": [
                {
                    "id": "abce8c67-a74c-46fd-b5c3-62a7b76f2b17",
                    "integration": "b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
                    "action": {
                        "id": "b0a0e7ed-d668-41b5-96d2-397f026c4ecb",
                        "type": "auth",
                        "name": "Authenticate",
                        "value": "auth",
                    },
                    "data": {
                        "login": "fake-username",
                        "password": "fake-password",  # pragma: allowlist secret
                    },
                },
                {
                    "id": "55760315-3d68-4925-bf2d-c4d39de433c9",
                    "integration": "b42c9205-5228-49e0-a75b-ebe5b6a9f78e",
                    "action": {
                        "id": "ebe72917-c112-4064-9f38-707bbd14a50f",
                        "type": "push",
                        "name": "Push Events",
                        "value": "push_events",
                    },
                    "data": {
                        "version": "7.5.4",
                        "ca_uuids": ["4b23242a-1161-46c3-af84-5e35dc801c43"],
                        "transformation_rules": {
                            "category_map": [],
                            "attribute_map": [],
                        },
                    },
                },
            ],
            "default_route": None,
            "additional": {
                "topic": "smart-dispatcher-topic-test",
                "broker": "gcp_pubsub",
            },
            "status": {
                "id": "mockid-b16a-4dbd-ad32-197c58aeef59",
                "is_healthy": True,
                "details": "Last observation has been delivered with success.",
                "observation_delivered_24hrs": 50231,
                "last_observation_delivered_at": "2023-03-31T11:20:00+0200",
            },
        }
    )


@pytest.fixture
def dispatched_event():
    return schemas_v2.DispatchedObservation(
        gundi_id="23ca4b15-18b6-4cf4-9da6-36dd69c6f638",
        related_to=None,
        external_id="ABC123",  # ID returned by the destination system
        data_provider_id="ddd0946d-15b0-4308-b93d-e0470b6d33b6",
        destination_id="338225f3-91f9-4fe1-b013-353a229ce504",
        delivered_at=datetime.datetime.now(),  # UTC
    )


@pytest.fixture
def observation_delivered_event(dispatched_observation):
    return system_events.ObservationDelivered(payload=dispatched_observation)
