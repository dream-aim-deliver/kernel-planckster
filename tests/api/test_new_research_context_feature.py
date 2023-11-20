from lib.infrastructure.config.containers import ApplicationContainer


def test_new_research_context_presenter(app_container: ApplicationContainer) -> None:
    presenter = app_container.new_research_context_feature.presenter()
    assert presenter is not None


def test_new_research_context_usecase(app_container: ApplicationContainer) -> None:
    usecase = app_container.new_research_context_feature.usecase()
    assert usecase is not None


def test_new_research_context_controller(app_container: ApplicationContainer) -> None:
    controller = app_container.new_research_context_feature.controller()
    assert controller is not None
