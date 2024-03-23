from lib.core.ports.primary.new_message_primary_ports import NewMessageOutputPort
from lib.core.usecase_models.new_message_usecase_models import NewMessageError, NewMessageResponse
from lib.core.view_model.new_message_view_model import NewMessageViewModel


class NewMessagePresenter(NewMessageOutputPort):
    def convert_error_response_to_view_model(self, response: NewMessageError) -> NewMessageViewModel:
        return NewMessageViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            message_id=-1,
        )

    def convert_response_to_view_model(self, response: NewMessageResponse) -> NewMessageViewModel:
        return NewMessageViewModel(
            status=True,
            code=200,
            message_id=response.message_id,
        )
