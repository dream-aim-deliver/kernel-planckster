from datetime import datetime
from lib.core.dto.conversation_repository_dto import NewMessageDTO
from lib.core.entity.models import MessageBase, MessageSenderTypeEnum
from lib.core.ports.primary.new_message_primary_ports import NewMessageInputPort
from lib.core.usecase_models.new_message_usecase_models import NewMessageError, NewMessageRequest, NewMessageResponse


class NewMessageUseCase(NewMessageInputPort):
    def execute(self, request: NewMessageRequest) -> NewMessageResponse | NewMessageError:
        try:
            conversation_id = request.conversation_id
            message_contents = request.message_contents
            sender_type_str_raw = request.sender_type
            timestamp_int = request.unix_timestamp
            thread_id = request.thread_id

            try:
                sender_type_str = "".join(sender_type_str_raw.lower().split())
                sender_type = MessageSenderTypeEnum(sender_type_str)

            except Exception as e:
                return NewMessageError(
                    errorCode=-1,
                    errorMessage=f"Couldn't validate the sender type provided. Error: {e}",
                    errorName="Sender Type Validation Error",
                    errorType="SenderTypeValidationError",
                )

            try:
                timestamp = datetime.fromtimestamp(timestamp_int)

            except Exception as e:
                return NewMessageError(
                    errorCode=-1,
                    errorMessage=f"Couldn't validate the timestamp provided. Error: {e}",
                    errorName="Timestamp Validation Error",
                    errorType="TimestampValidationError",
                )

            dto: NewMessageDTO = self.conversation_repository.new_message(
                conversation_id=conversation_id,
                message_contents=message_contents,
                sender_type=sender_type,
                timestamp=timestamp,
                thread_id=thread_id,
            )

            if dto.status:
                message = dto.data

                if message is not None:
                    return NewMessageResponse(message_id=message.id)

                return NewMessageError(
                    errorCode=-1,
                    errorMessage=f"An unexpected error occurred: repository reports success, but got back an unexpected object: '{dto.data}'",
                    errorName="UnexpectedError",
                    errorType="UnexpectedError",
                )

            return NewMessageError(
                errorCode=dto.errorCode, errorMessage=dto.errorMessage, errorName=dto.errorName, errorType=dto.errorType
            )

        except Exception as e:
            return NewMessageError(
                errorCode=-1,
                errorMessage=f"An unexpected error occurred:\n{e}",
                errorName="UnexpectedError",
                errorType="UnexpectedError",
            )
