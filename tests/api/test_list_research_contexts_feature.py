from lib.core.usecase.list_research_contexts_usecase import ListResearchContextsUseCase
from lib.core.view_model.list_research_contexts_view_model import ListResearchContextsViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_research_contexts_controller import ListResearchContextsControllerParameters
from lib.infrastructure.presenter.list_research_contexts_presenter import ListResearchContextsPresenter
from lib.infrastructure.repository.sqla.database import TDatabaseFactory


def test_list_research_contexts_presenter(app_initialization_container: ApplicationContainer) -> None:
    presenter: ListResearchContextsPresenter = app_initialization_container.list_research_contexts_feature.presenter()
    assert presenter is not None


def test_list_research_contexts_usecase(
    app_initialization_container: ApplicationContainer,
) -> None:
    usecase: ListResearchContextsUseCase = app_initialization_container.list_research_contexts_feature.usecase()
    assert usecase is not None


def test_list_research_contexts_controller(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    controller = app_initialization_container.list_research_contexts_feature.controller()
    assert controller is not None

    controller_parameters = ListResearchContextsControllerParameters(client_id=1)

    view_model: ListResearchContextsViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
