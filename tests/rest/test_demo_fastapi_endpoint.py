from fastapi.testclient import TestClient

from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.config.containers import ApplicationContainer


def test_demo_fastapi_get_endpoint_returns_valid_response(
    httpx_client: TestClient, app_container: ApplicationContainer
) -> None:
    response = httpx_client.get("/sum", params={"num1": 1, "num2": 2})
    assert response.status_code == 200
    data = response.json()
    assert (
        response.json()
        == DemoViewModel(
            status=True,
            sum=3,
            code=200,
        ).model_dump()
    )


def test_demo_fastapi_get_endpoint_invalid_query(httpx_client: TestClient, app_container: ApplicationContainer) -> None:
    response = httpx_client.get("/sum")
    assert response.status_code == 422
