from lib.core.view_model.list_conversations_view_model import ListConversationsViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_conversations_controller import ListConversationsControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory


def test_list_conversations_feature_is_successful(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    controller = app_initialization_container.list_conversations_feature.controller()
    assert controller is not None
    controller_parameters = ListConversationsControllerParameters(
        research_context_id=1,
    )
    view_model: ListConversationsViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
