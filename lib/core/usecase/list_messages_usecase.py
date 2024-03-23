from lib.core.dto.conversation_repository_dto import ListConversationMessagesDTO
from lib.core.entity.models import MessageBase
from lib.core.ports.primary.list_messages_primary_ports import ListMessagesInputPort
from lib.core.usecase_models.list_messages_usecase_models import (
    ListMessagesError,
    ListMessagesRequest,
    ListMessagesResponse,
)


class ListMessagesUseCase(ListMessagesInputPort):
    def execute(self, request: ListMessagesRequest) -> ListMessagesResponse | ListMessagesError:
        conversation_id = request.conversation_id
        conversation_repository = self.conversation_repository

        try:
            dto: ListConversationMessagesDTO[MessageBase] = conversation_repository.list_conversation_messages(
                conversation_id=conversation_id
            )

            if dto.status:
                if isinstance(dto.data, list):
                    return ListMessagesResponse(message_list=dto.data)

                else:
                    return ListMessagesError(
                        errorCode=-1,
                        errorMessage="Repository reports success, but no list (even an empty one) was returned",
                        errorName="No List Returned On Repository Success",
                        errorType="NoListReturnedOnRepositorySuccess",
                        conversation_id=conversation_id,
                    )

            return ListMessagesError(
                errorCode=dto.errorCode,
                errorMessage=dto.errorMessage,
                errorName=dto.errorName,
                errorType=dto.errorType,
                conversation_id=conversation_id,
            )

        except Exception as e:
            return ListMessagesError(
                errorCode=-1,
                errorMessage=f"{e}",
                errorName="Unknown Usecase Error",
                errorType="Unknown Usecase Error",
                conversation_id=conversation_id,
            )
