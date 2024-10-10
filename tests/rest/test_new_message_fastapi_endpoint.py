from fastapi.testclient import TestClient
from lib.core.view_model.new_message_view_model import NewMessageViewModel
from lib.infrastructure.config.containers import ApplicationContainer


def test_new_message_fastapi_post_endpoint_returns_view_model(
    httpx_client: TestClient, app_container: ApplicationContainer
) -> None:
    headers = {
        "x-auth-token": "test123",
    }

    response = httpx_client.post(
        "/conversation/1/message",
        params={
            "sender_type": "client",
            "unix_timestamp": 1633096800,
        },
        json=[
            {
                "content": "body",
                "content_type": "text",
            }
        ],
        headers=headers,
    )

    assert response is not None
    assert "code" in response.json()

    received_vm = NewMessageViewModel.model_validate(response.json())

    assert isinstance(received_vm, NewMessageViewModel)
