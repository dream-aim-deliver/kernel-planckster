from abc import abstractmethod
from lib.core.sdk.primary_ports import BaseOutputPort
from lib.core.sdk.usecase import BaseUseCase
from lib.core.sdk.usecase_models import BaseErrorResponse
from lib.core.usecase_models.list_conversations_usecase_models import (
    ListConversationsError,
    ListConversationsRequest,
    ListConversationsResponse,
)
from lib.core.view_model.list_conversations_view_model import ListConversationsViewModel


class ListConversationsInputPort(
    BaseUseCase[ListConversationsRequest, ListConversationsResponse, ListConversationsError]
):
    @abstractmethod
    def execute(self, request: ListConversationsRequest) -> ListConversationsResponse | ListConversationsError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class ListConversationsOutputPort(
    BaseOutputPort[ListConversationsResponse, ListConversationsError, ListConversationsViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: ListConversationsError) -> ListConversationsViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: ListConversationsResponse) -> ListConversationsViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
