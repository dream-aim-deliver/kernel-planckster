from lib.core.ports.primary.list_messages_primary_ports import ListMessagesOutputPort
from lib.core.usecase_models.list_messages_usecase_models import ListMessagesError, ListMessagesResponse
from lib.core.view_model.list_messages_view_model import ListMessagesViewModel


class ListMessagesPresenter(ListMessagesOutputPort):
    def convert_error_response_to_view_model(self, response: ListMessagesError) -> ListMessagesViewModel:
        return ListMessagesViewModel(
            status=False,
            message_list=[],
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(self, response: ListMessagesResponse) -> ListMessagesViewModel:
        return ListMessagesViewModel(
            status=True,
            code=200,
            message_list=response.message_list,
        )
