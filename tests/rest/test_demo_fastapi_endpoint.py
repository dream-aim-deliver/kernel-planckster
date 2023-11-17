from fastapi.testclient import TestClient

from lib.core.view_model.demo_view_model import DemoViewModel


def test_demo_fastapi_get_endpoint_returns_valid_response(client: TestClient) -> None:
    response = client.get("/demo/sum", params={"num1": 1, "num2": 2})
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


def test_demo_fastapi_get_endpoint_invalid_query(client: TestClient) -> None:
    response = client.get("/demo/sum")
    assert response.status_code == 422
