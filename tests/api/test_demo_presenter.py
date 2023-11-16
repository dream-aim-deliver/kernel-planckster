from lib.core.usecase_models.demo_usecase_models import DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.config.containers import Container


def test_demo_presenter(app_container: Container) -> None:
    presenter = app_container.demo.presenter()
    assert presenter is not None
    view_model: DemoViewModel = presenter.present_success(DemoResponse(sum=10))
    assert view_model is not None
    assert view_model.status is True
    assert view_model.sum == 10
