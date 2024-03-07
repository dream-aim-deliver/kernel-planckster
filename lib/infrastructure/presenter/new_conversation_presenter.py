from lib.core.ports.primary.new_conversation_primary_ports import NewConversationOutputPort
from lib.core.usecase_models.new_conversation_usecase_models import NewConversationError, NewConversationResponse
from lib.core.view_model.new_conversation_view_model import NewConversationViewModel


class NewConversationPresenter(NewConversationOutputPort):
    def convert_error_response_to_view_model(self, response: NewConversationError) -> NewConversationViewModel:
        return NewConversationViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            conversation_id=-1,
        )

    def convert_response_to_view_model(self, response: NewConversationResponse) -> NewConversationViewModel:
        return NewConversationViewModel(
            status=True,
            code=200,
            conversation_id=response.conversation_id,
        )
