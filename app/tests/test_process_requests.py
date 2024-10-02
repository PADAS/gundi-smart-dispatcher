import pytest
from app.core import settings
from smartconnect import SMARTClientException
from fastapi.testclient import TestClient
from app.core.errors import TooManyRequests
from app.main import app

api_client = TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pubsub_message, is_completion_expected",
    [
        ("event_v2_pubsub_message", True),
        ("event_v2_pubsub_message_with_future_timestamp", True),
        ("event_v2_pubsub_message_with_old_timestamp", False),
    ],
)
async def test_process_event_v2_successfully(
    request,
    is_completion_expected,
    mocker,
    mock_cache,
    mock_gundi_client_v2_class,
    mock_smartclient_class,
    mock_pubsub_client,
    pubsub_message,
    pubsub_request_headers,
    observation_delivered_pubsub_message,
):
    pubsub_message = request.getfixturevalue(pubsub_message)
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client)
    mock_services_pubsub_client = mocker.patch(
        "app.services.process_messages.pubsub", mock_pubsub_client
    )
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=pubsub_message,
    )
    assert response.status_code == 200
    # Check that the report was sent o SMART
    assert mock_smartclient_class.called == is_completion_expected
    assert (
        mock_smartclient_class.return_value.post_smart_request.called
        == is_completion_expected
    )
    # Check that the trace was written to redis db
    assert mock_cache.setex.called == is_completion_expected
    # Check that the right event was published to the right pubsub topic
    assert mock_pubsub_client.PublisherClient.called
    assert mock_pubsub_client.PubsubMessage.called
    # Message published either to dispatcher-events topic or dead-letter
    assert mock_pubsub_client.PublisherClient.return_value.publish.called
    if is_completion_expected:
        mock_pubsub_client.PublisherClient.return_value.publish.assert_any_call(
            f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}",
            [observation_delivered_pubsub_message],
        )
    else:
        mock_services_pubsub_client.PublisherClient.return_value.topic_path.assert_any_call(
            settings.GCP_PROJECT_ID, settings.DEAD_LETTER_TOPIC
        )


@pytest.mark.asyncio
async def test_process_event_update_v2_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v2_class,
    mock_smartclient_class_for_updates,
    mock_pubsub_client_updates,
    pubsub_request_headers,
    event_update_v2_pubsub_message,
    observation_updated_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch(
        "app.services.dispatchers.AsyncSmartClient", mock_smartclient_class_for_updates
    )
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client_updates)
    mocker.patch("app.services.process_messages.pubsub", mock_pubsub_client_updates)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=event_update_v2_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the report was sent o SMART
    assert mock_smartclient_class_for_updates.called
    assert mock_smartclient_class_for_updates.return_value.post_smart_request
    # Check that the trace was written to redis db
    assert mock_cache.setex.called
    # Check that the right event was published to the right pubsub topic
    assert mock_pubsub_client_updates.PublisherClient.called
    assert mock_pubsub_client_updates.PubsubMessage.called
    # Message published either to dispatcher-events topic or dead-letter
    assert mock_pubsub_client_updates.PublisherClient.return_value.publish.called
    mock_pubsub_client_updates.PublisherClient.return_value.publish.assert_any_call(
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}",
        [observation_updated_pubsub_message],
    )


@pytest.mark.asyncio
async def test_system_event_is_published_on_smartclient_error(
    mocker,
    mock_cache,
    mock_smartclient_class_with_400_response,
    mock_pubsub_client_with_observation_delivery_failure,
    mock_gundi_client_v2_class,
    pubsub_request_headers,
    event_v2_pubsub_message,
    observation_delivery_failure_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch(
        "app.services.dispatchers.AsyncSmartClient",
        mock_smartclient_class_with_400_response,
    )
    mocker.patch(
        "app.core.utils.pubsub", mock_pubsub_client_with_observation_delivery_failure
    )
    # Check that the dispatcher raises an exception so the message is retried later
    with pytest.raises(SMARTClientException):
        api_client.post(
            "/",
            headers=pubsub_request_headers,
            json=event_v2_pubsub_message,
        )
    # Check that the call to send the report to SMART was made
    assert mock_smartclient_class_with_400_response.called
    assert (
        mock_smartclient_class_with_400_response.return_value.post_smart_request.called
    )
    # Check that an event was published to the right pubsub topic to inform other services about the error
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert mock_pubsub_client_with_observation_delivery_failure.PubsubMessage.called
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert (
        mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.called
    )
    mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.assert_any_call(
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}",
        [observation_delivery_failure_pubsub_message],
    )


@pytest.mark.asyncio
async def test_throttling_on_event_creation(
    mocker,
    mock_cache_with_rate_limit_exceeded,
    mock_smartclient_class,
    mock_pubsub_client_with_observation_delivery_failure,
    mock_gundi_client_v2_class,
    pubsub_request_headers,
    event_v2_pubsub_message,
    observation_delivery_failure_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache_with_rate_limit_exceeded)
    mocker.patch(
        "app.services.dispatchers._redis_client", mock_cache_with_rate_limit_exceeded
    )
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch(
        "app.core.utils.pubsub", mock_pubsub_client_with_observation_delivery_failure
    )
    # Check that the dispatcher raises an exception so the message is retried later
    with pytest.raises(TooManyRequests):
        api_client.post(
            "/",
            headers=pubsub_request_headers,
            json=event_v2_pubsub_message,
        )
    # Check that the call to send the report to SMART was NOT made
    assert not mock_smartclient_class.return_value.post_smart_request.called
    # Check that an event was published to the right pubsub topic to inform other services about the error
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert mock_pubsub_client_with_observation_delivery_failure.PubsubMessage.called
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert (
        mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.called
    )
    mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.assert_any_call(
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}",
        [observation_delivery_failure_pubsub_message],
    )


@pytest.mark.asyncio
async def test_throttling_on_event_updates(
    mocker,
    mock_cache_with_rate_limit_exceeded,
    mock_smartclient_class,
    mock_pubsub_client_with_observation_delivery_failure,
    mock_gundi_client_v2_class,
    pubsub_request_headers,
    event_update_v2_pubsub_message,
    observation_delivery_failure_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache_with_rate_limit_exceeded)
    mocker.patch(
        "app.services.dispatchers._redis_client", mock_cache_with_rate_limit_exceeded
    )
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch(
        "app.core.utils.pubsub", mock_pubsub_client_with_observation_delivery_failure
    )
    # Check that the dispatcher raises an exception so the message is retried later
    with pytest.raises(TooManyRequests):
        api_client.post(
            "/",
            headers=pubsub_request_headers,
            json=event_update_v2_pubsub_message,
        )
    # Check that the call to send the report to SMART was NOT made
    assert not mock_smartclient_class.return_value.post_smart_request.called
    # Check that an event was published to the right pubsub topic to inform other services about the error
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert mock_pubsub_client_with_observation_delivery_failure.PubsubMessage.called
    assert mock_pubsub_client_with_observation_delivery_failure.PublisherClient.called
    assert (
        mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.called
    )
    mock_pubsub_client_with_observation_delivery_failure.PublisherClient.return_value.publish.assert_any_call(
        f"projects/{settings.GCP_PROJECT_ID}/topics/{settings.DISPATCHER_EVENTS_TOPIC}",
        [observation_delivery_failure_pubsub_message],
    )


@pytest.mark.asyncio
async def test_process_geoevent_v1_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v1,
    mock_smartclient_class,
    mock_pubsub_client,
    pubsub_request_headers,
    geoevent_v1_pubsub_message,
    observation_delivered_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils._portal", mock_gundi_client_v1)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=geoevent_v1_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the report was sent o SMART
    assert mock_smartclient_class.called
    assert mock_smartclient_class.return_value.post_smart_request.called
    # Check that the trace was written to redis db
    assert mock_cache.setex.called


@pytest.mark.asyncio
async def test_process_er_event_v1_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v1,
    mock_smartclient_class,
    mock_pubsub_client,
    pubsub_request_headers,
    er_event_v1_pubsub_message,
    observation_delivered_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils._portal", mock_gundi_client_v1)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=er_event_v1_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the report was sent o SMART
    assert mock_smartclient_class.called
    assert mock_smartclient_class.return_value.post_smart_request.called
    # Check that the trace was written to redis db
    assert mock_cache.setex.called


@pytest.mark.asyncio
async def test_process_er_event_v1_with_attachment_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v1,
    mock_smartclient_class,
    mock_pubsub_client,
    pubsub_request_headers,
    mock_cloud_storage_client_class,
    er_event_v1_with_attachment_pubsub_message,
    observation_delivered_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils._portal", mock_gundi_client_v1)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch("app.services.dispatchers.Storage", mock_cloud_storage_client_class)
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=er_event_v1_with_attachment_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the attachment was downloaded from cloud storage
    assert mock_cloud_storage_client_class.return_value.download.called
    # Check that the report was sent o SMART
    assert mock_smartclient_class.called
    assert mock_smartclient_class.return_value.post_smart_request.called


@pytest.mark.asyncio
async def test_process_er_patrol_v1_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v1,
    mock_smartclient_class,
    mock_pubsub_client,
    pubsub_request_headers,
    er_patrol_v1_pubsub_message,
    observation_delivered_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils._portal", mock_gundi_client_v1)
    mocker.patch("app.services.dispatchers.AsyncSmartClient", mock_smartclient_class)
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=er_patrol_v1_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the report was sent o SMART
    assert mock_smartclient_class.called
    assert mock_smartclient_class.return_value.post_smart_request.called
    # Check that the trace was written to redis db
    assert mock_cache.setex.called


@pytest.mark.asyncio
async def test_process_attachment_v2_successfully(
    mocker,
    mock_cache,
    mock_gundi_client_v2_class,
    mock_cloud_storage_client_class,
    mock_smartclient_class_for_updates,
    mock_pubsub_client_updates,
    pubsub_request_headers,
    attachment_as_event_update_v2_pubsub_message,
    observation_delivered_pubsub_message,
):
    # Mock external dependencies
    mocker.patch("app.core.utils._cache_db", mock_cache)
    mocker.patch("app.services.dispatchers._redis_client", mock_cache)
    mocker.patch("app.core.utils.GundiClient", mock_gundi_client_v2_class)
    mocker.patch(
        "app.services.dispatchers.AsyncSmartClient", mock_smartclient_class_for_updates
    )
    mocker.patch("app.core.utils.pubsub", mock_pubsub_client_updates)
    mocker.patch("app.services.dispatchers.Storage", mock_cloud_storage_client_class)
    mocker.patch("app.services.process_messages.pubsub", mock_pubsub_client_updates)
    response = api_client.post(
        "/",
        headers=pubsub_request_headers,
        json=attachment_as_event_update_v2_pubsub_message,
    )
    assert response.status_code == 200
    # Check that the attachment was downloaded from cloud storage
    assert mock_cloud_storage_client_class.return_value.download.called
    # Check that the report was sent o SMART
    assert mock_smartclient_class_for_updates.called
    assert mock_smartclient_class_for_updates.return_value.post_smart_request.called
    # Message published either to dispatcher-events topic
    assert mock_pubsub_client_updates.PublisherClient.return_value.publish.called
