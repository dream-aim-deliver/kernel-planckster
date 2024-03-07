from lib.core.view_model.new_conversation_view_model import NewConversationViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_conversation_controller import NewConversationControllerParameters


def test_new_converstion_presenter(app_container: ApplicationContainer) -> None:
    presenter = app_container.new_conversation_feature.presenter()
    assert presenter is not None


def test_new_research_context_usecase(app_container: ApplicationContainer) -> None:
    usecase = app_container.new_conversation_feature.usecase()
    assert usecase is not None


def test_new_research_context_controller(app_container: ApplicationContainer) -> None:
    controller = app_container.new_conversation_feature.controller()
    assert controller is not None

    controller_parameters = NewConversationControllerParameters(
        research_context_id=1, conversation_title="Test Conversation"
    )

    view_model: NewConversationViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
