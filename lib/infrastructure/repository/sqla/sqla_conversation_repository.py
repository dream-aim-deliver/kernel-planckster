from datetime import datetime
from typing import List, Set

from lib.core.dto.conversation_repository_dto import (
    GetConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
    ListConversationSourcesDTO,
    SendMessageToConversationDTO,
    UpdateConversationDTO,
)
from lib.core.entity.models import (
    MessageBase,
    SourceData,
    TMessageBase,
)
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLAConversation,
    SQLAMessageBase,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLASourceData,
)
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_conversation_to_core_conversation,
    convert_sqla_message_query_to_core_message_query,
    convert_sqla_message_response_to_core_message_response,
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_source_data_to_core_source_data,
)


class SQLAConversationRepository(ConversationRepository):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()

        with session_factory() as session:
            self.session = session

    def get_conversation(self, conversation_id: int) -> GetConversationDTO:
        """
        Gets a conversation by ID.

        @param conversation_id: The ID of the conversation to get.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ConversationDTO
        """

        if conversation_id is None:
            errorDTO = GetConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = GetConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_conversation = convert_sqla_conversation_to_core_conversation(sqla_conversation)

        return GetConversationDTO(
            status=True,
            data=core_conversation,
        )

    def get_conversation_research_context(self, conversation_id: int) -> GetConversationResearchContextDTO:
        """
        Gets the research context of a conversation.

        @param research_context_id: The ID of the research context to get the conversation for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetConversationResearchContextDTO
        """

        if conversation_id is None:
            errorDTO = GetConversationResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = GetConversationResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = (
            self.session.query(SQLAResearchContext).filter_by(id=sqla_conversation.research_context_id).first()
        )

        if sqla_research_context is None:
            self.logger.error(
                f"Research Context with ID {sqla_conversation.research_context_id} not found in the database."
            )
            errorDTO = GetConversationResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {sqla_conversation.research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_research_context = convert_sqla_research_context_to_core_research_context(sqla_research_context)

        return GetConversationResearchContextDTO(
            status=True,
            data=core_research_context,
        )

    def list_conversation_messages(self, conversation_id: int) -> ListConversationMessagesDTO[TMessageBase]:
        """
        Lists all messages in a conversation.

        @param conversation_id: The ID of the conversation to list messages for.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        """
        if conversation_id is None:
            errorDTO = ListConversationMessagesDTO[TMessageBase](
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = ListConversationMessagesDTO[TMessageBase](
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_messages: List[MessageBase] = []

        for sqla_message in sqla_conversation.messages:
            if isinstance(sqla_message, SQLAMessageQuery):
                core_message_query = convert_sqla_message_query_to_core_message_query(sqla_message)
                core_messages.append(core_message_query)

            if isinstance(sqla_message, SQLAMessageResponse):
                core_message_response = convert_sqla_message_response_to_core_message_response(sqla_message)
                core_messages.append(core_message_response)

        return ListConversationMessagesDTO[TMessageBase](
            status=True,
            data=core_messages,
        )

    def update_conversation(self, conversation_id: int, conversation_title: str) -> UpdateConversationDTO:
        """
        Updates a conversation in the research context.

        @param conversation_id: The ID of the conversation to update.
        @type conversation_id: int
        @param conversation_title: The title of the conversation.
        @type conversation_title: str
        @return: A DTO containing the result of the operation.
        @rtype: ConversationDTO
        """
        if conversation_id is None:
            errorDTO = UpdateConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if conversation_title is None:
            errorDTO = UpdateConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation title cannot be None",
                errorName="Conversation title not provided",
                errorType="ConversationTitleNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = UpdateConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            sqla_conversation.update({"title": conversation_title}, session=self.session)
            self.session.commit()

            return UpdateConversationDTO(status=True, conversation_id=sqla_conversation.id)

        except Exception as e:
            self.logger.error(f"Error while updating the conversation: {e}")
            errorDTO = UpdateConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while updating the conversation: {e}",
                errorName="Error while updating the conversation",
                errorType="ErrorWhileUpdatingConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

    def list_conversation_sources(self, conversation_id: int) -> ListConversationSourcesDTO:
        """
        Lists all data sources of the citations of a conversation.

        @param conversation_id: The ID of the conversation to list data sources for.
        @type conversation_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListConversationSourcesDTO
        """
        if conversation_id is None:
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqlamessages: List[SQLAMessageBase] = sqla_conversation.messages
        sqlasourcedata_set: Set[SQLASourceData] = set()
        error_message_response_ids: List[int] = []

        for sqlamessage in sqlamessages:
            if isinstance(sqlamessage, SQLAMessageResponse):
                queried_sqla_source_data_list = (
                    self.session.query(SQLASourceData)
                    .join(SQLASourceData.message_response)
                    .filter_by(id=sqlamessage.id)
                    .all()
                )

                if queried_sqla_source_data_list == []:
                    error_message_response_ids.append(sqlamessage.id)

                queried_sqla_source_data_set = set(queried_sqla_source_data_list)
                sqlasourcedata_set.update(queried_sqla_source_data_set)

        sqlasourcedata = list(sqlasourcedata_set)

        if error_message_response_ids != []:
            self.logger.error(f"Message Responses with IDs {error_message_response_ids} have no source data.")
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Message Responses with ID {error_message_response_ids} have no source data.",
                errorName="Message Responses have no source data",
                errorType="MessageResponsesHaveNoSourceData",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_source_data: List[SourceData] = []

        for sqlasourcedatum in sqlasourcedata:
            coresourcedatum = convert_sqla_source_data_to_core_source_data(sqlasourcedatum)
            core_source_data.append(coresourcedatum)

        if core_source_data == []:
            self.logger.error(f"Conversation with ID {conversation_id} has no source data.")
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} has no source data.",
                errorName="Conversation has no source data",
                errorType="ConversationHasNoSourceData",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        return ListConversationSourcesDTO(
            status=True,
            data=core_source_data,
        )

    def send_message_to_conversation(self, conversation_id: int, message_content: str) -> SendMessageToConversationDTO:
        """
        Sends a message to a conversation.

        @param conversation_id: The ID of the conversation to send the message to.
        @type conversation_id: int
        @param message_content: The content of the message.
        @type message_content: str
        @return: A DTO containing the result of the operation.
        @rtype: SendMessageToConversationDTO
        """

        if conversation_id is None:
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if message_content is None:
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage="Message content cannot be None",
                errorName="Message content not provided",
                errorType="MessageContentNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversation: SQLAConversation | None = (
            self.session.query(SQLAConversation).filter_by(id=conversation_id).first()
        )

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = SendMessageToConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_message_query: SQLAMessageQuery = SQLAMessageQuery(
            content=message_content,
            timestamp=datetime.now(),
            conversation_id=conversation_id,
        )

        try:
            sqla_message_query.save(session=self.session)
            self.session.commit()

            core_message_query = convert_sqla_message_query_to_core_message_query(sqla_message_query)

            return SendMessageToConversationDTO(status=True, data=core_message_query)

        except Exception as e:
            self.logger.error(f"Error while sending message to conversation: {e}")
            errorDTO = SendMessageToConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while sending message to conversation: {e}",
                errorName="Error while sending message to conversation",
                errorType="ErrorWhileSendingMessageToConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
