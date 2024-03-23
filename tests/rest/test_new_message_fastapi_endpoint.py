from fastapi.testclient import TestClient
from lib.core.view_model.new_message_view_model import NewMessageViewModel
from lib.infrastructure.config.containers import ApplicationContainer


def test_new_message_fastapi_post_endpoint_returns_view_model(
    client: TestClient, app_container: ApplicationContainer
) -> None:
    headers = {
        "x-auth-token": "test123",
    }

    response = client.post(
        "/conversations/1/new_message",
        params={
            "message_content": "Hello, World!",
            "sender_type": "user",
            "unix_timestamp": 1633096800,
        },
        headers=headers,
    )

    assert response is not None

    received_vm = NewMessageViewModel.model_validate(response.json())

    assert isinstance(received_vm, NewMessageViewModel)
