from lib.core.ports.primary.list_conversations_primary_ports import ListConversationsOutputPort
from lib.core.usecase_models.list_conversations_usecase_models import ListConversationsError, ListConversationsResponse
from lib.core.view_model.list_conversations_view_model import ListConversationsViewModel


class ListConversationsPresenter(ListConversationsOutputPort):
    def convert_error_response_to_view_model(self, error: ListConversationsError) -> ListConversationsViewModel:
        return ListConversationsViewModel(
            status=False,
            conversations=[],
            research_context_id=error.research_context_id,
            code=error.errorCode,
            errorCode=error.errorCode,
            errorMessage=error.errorMessage,
            errorName=error.errorName,
            errorType=error.errorType,
        )

    def convert_response_to_view_model(self, response: ListConversationsResponse) -> ListConversationsViewModel:
        return ListConversationsViewModel(
            status=True,
            research_context_id=response.research_context_id,
            conversations=response.conversations,
            code=200,
        )
