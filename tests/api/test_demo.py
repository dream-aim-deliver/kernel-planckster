from lib.core.usecase_models.demo_usecase_models import DemoRequest, DemoResponse
from lib.core.view_model.demo_view_model import DemoViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.demo_controller import DemoControllerParameters


def test_demo_presenter(app_container: ApplicationContainer) -> None:
    presenter = app_container.demo_feature.presenter()
    assert presenter is not None
    view_model: DemoViewModel = presenter.present_success(DemoResponse(sum=10))
    assert view_model is not None
    assert view_model.status is True
    assert view_model.sum == 10


def test_demo_usecase(app_container: ApplicationContainer) -> None:
    usecase = app_container.demo_feature.usecase()
    assert usecase is not None
    response = usecase.execute(request=DemoRequest(numbers=[1, 2, 3]))
    assert response is not None
    assert response.sum == 6


def test_demo_controller(app_container: ApplicationContainer) -> None:
    controller = app_container.demo_feature.controller()
    assert controller is not None
    view_model = controller.execute(parameters=None)
    assert view_model is not None
    assert view_model.status is True
    assert view_model.sum == 0

    controller_parameters: DemoControllerParameters = DemoControllerParameters(num1=1, num2=2)
    view_model = controller.execute(parameters=controller_parameters)
    assert view_model is not None
    assert view_model.status is True
    assert view_model.sum == 3


def test_demo_feature_descriptor(app_container: ApplicationContainer) -> None:
    demo_descriptor = app_container.demo_feature.feature_descriptor()
    print(app_container.config)
    assert demo_descriptor is not None
    assert demo_descriptor.name == "Sum Feature"
    assert demo_descriptor.description == "Adds 2 numbers"
    assert demo_descriptor.version == "1.0.0"
    assert demo_descriptor.verb == "GET"
    assert demo_descriptor.endpoint == "/sum"
    assert demo_descriptor.enabled is True
