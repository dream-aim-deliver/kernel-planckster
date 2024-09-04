from datetime import datetime
from typing import List, Set


from lib.core.dto.conversation_repository_dto import (
    GetConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
    ListConversationSourcesDTO,
    NewMessageDTO,
    NewMessageContentDTO,
    UpdateConversationDTO,
)
from lib.core.entity.models import (
    AgentMessage,
    MessageBase,
    MessageSenderTypeEnum,
    SourceData,
    TMessageBase,
    UserMessage,
    MessageContent,
)
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLAConversation,
    SQLAMessageBase,
    SQLAUserMessage,
    SQLAAgentMessage,
    SQLAMessageContent,
    SQLAResearchContext,
    SQLASourceData,
)
from sqlalchemy.orm import Session
from sqlalchemy import Select, Result, select, func

from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_conversation_to_core_conversation,
    convert_sqla_client_message_to_core_user_message,
    convert_sqla_agent_message_to_core_agent_message,
    convert_sqla_message_content_to_core_message_content,
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_source_data_to_core_source_data,
)


class SQLAConversationRepository(ConversationRepository):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

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

        sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

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

        sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

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

        sqla_research_context: SQLAResearchContext | None = sqla_conversation.research_context

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

        try:
            sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

        except Exception as e:
            self.logger.error(f"Error while querying the database for conversation with ID {conversation_id}: {e}")
            errorDTO = ListConversationMessagesDTO[TMessageBase](
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying the database for conversation with ID {conversation_id}: {e}",
                errorName="Error while querying the database",
                errorType="ErrorWhileQueryingDatabase",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

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
            if isinstance(sqla_message, SQLAUserMessage):
                core_user_message = convert_sqla_client_message_to_core_user_message(sqla_message)
                core_messages.append(core_user_message)

            if isinstance(sqla_message, SQLAAgentMessage):
                core_agent_message = convert_sqla_agent_message_to_core_agent_message(sqla_message)
                core_messages.append(core_agent_message)

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

        sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

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

        sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

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
        error_agent_message_ids: List[int] = []

        for sqlamessage in sqlamessages:
            if isinstance(sqlamessage, SQLAAgentMessage):
                queried_sqla_source_data_list = (
                    self.session.query(SQLASourceData)
                    .join(SQLASourceData.agent_message)
                    .filter_by(id=sqlamessage.id)
                    .all()
                )

                if queried_sqla_source_data_list == []:
                    error_agent_message_ids.append(sqlamessage.id)

                queried_sqla_source_data_set = set(queried_sqla_source_data_list)
                sqlasourcedata_set.update(queried_sqla_source_data_set)

        sqlasourcedata = list(sqlasourcedata_set)

        if error_agent_message_ids != []:
            self.logger.error(f"Message Responses with IDs {error_agent_message_ids} have no source data.")
            errorDTO = ListConversationSourcesDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Message Responses with ID {error_agent_message_ids} have no source data.",
                errorName="Message Responses have no source data",
                errorType="AgentMessagesHaveNoSourceData",
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

    # def new_message_content(self, message_id: int, content: str) -> NewMessageContentDTO:
    #     """
    #     Creates a piece of content for a message.

    #     @param content: The piece of content of the message
    #     @type content: str
    #     @param message_id: The ID of the message containing the message content
    #     @return: A DTO containing the result of the operation.
    #     @rtype: NewMessageContentDTO
    #     """

    #     if message_id is None:
    #         errorDTO = NewMessageContentDTO(
    #             status=False,
    #             errorCode=-1,
    #             errorMessage="Message ID cannot be None",
    #             errorName="Message ID not provided",
    #             errorType="MessageIdNotProvided",
    #         )
    #         self.logger.error(f"{errorDTO}")
    #         return errorDTO

    #     if content is None:
    #         errorDTO = NewMessageContentDTO(
    #             status=False,
    #             errorCode=-1,
    #             errorMessage="Content cannot be None",
    #             errorName="Content not provided",
    #             errorType="ContentNotProvided",
    #         )
    #         self.logger.error(f"{errorDTO}")
    #         return errorDTO

    #     # 1. Obtain the message and check if it exists

    #     try:
    #         sqla_message: SQLAMessageBase | None = self.session.get(SQLAMessageBase, message_id)

    #     except Exception as e:
    #         self.logger.error(f"Error while querying the database for message with ID {message_id}: {e}")
    #         errorDTO = NewMessageContentDTO(
    #             status=False,
    #             errorCode=-1,
    #             errorMessage=f"Error while querying the database for message with ID {message_id}: {e}",
    #             errorName="ErrorWhileQueryingDatabase",
    #             errorType="ErrorWhileQueryingDatabase",
    #         )
    #         self.logger.error(f"{errorDTO}")
    #         return errorDTO

    #     if sqla_message is None:
    #         self.logger.error(f"Message with ID {message_id} not found in the database.")
    #         errorDTO = NewMessageContentDTO(
    #             status=False,
    #             errorCode=-1,
    #             errorMessage=f"Message with ID {message_id} not found in the database.",
    #             errorName="Message not found",
    #             errorType="MessageNotFound",
    #         )
    #         self.logger.error(f"{errorDTO}")
    #         return errorDTO

    #     # 2. Create the message content object

    #     sqla_message_content: SQLAMessageContent = SQLAMessageContent(
    #         content=content,
    #         message_id=message_id,
    #         # message_id=SQLAMessageBase(message_id=message_id),
    #     )

    #     try:
    #         sqla_message_content.save(session=self.session)
    #         self.session.commit()

    #         core_message_content: MessageContent

    #         core_message_content = convert_sqla_message_content_to_core_message_content(
    #             sqla_message_content
    #         )

    #         return NewMessageContentDTO(status=True, data=core_message_content)

    #     except Exception as e:
    #         self.logger.error(f"Error while creating content for message: {e}")
    #         errorDTO = NewMessageContentDTO(
    #             status=False,
    #             errorCode=-1,
    #             errorMessage=f"Error while creating content for message: {e}",
    #             errorName="Error while creating content for message",
    #             errorType="ErrorWhileCreatingContentForMessage",
    #         )
    #         self.logger.error(f"{errorDTO}")
    #         return errorDTO


    def new_message(
        self,
        conversation_id: int,
        message_contents: List[str],
        sender_type: MessageSenderTypeEnum,
        timestamp: datetime,
        thread_id: int | None = None,
    ) -> NewMessageDTO:
        """
        Sends a message to a conversation.

        @param conversation_id: The ID of the conversation to send the message to.
        @type conversation_id: int
        @param thread_id: The ID of the thread of the message
        @type thread_id: int
        @param message_contents: A list of the content pieces of the message
        @type message_contents: List[MessageContent]
        @return: A DTO containing the result of the operation.
        @rtype: NewMessageDTO
        """

        if conversation_id is None:
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if not message_contents:
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage="Message contents must be a list with at least one item",
                errorName="Message contents not provided",
                errorType="MessageContentsNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if sender_type is None:
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage="Sender type cannot be None",
                errorName="Sender type not provided",
                errorType="SenderTypeNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 1. Obtain the conversation and check if it exists
        try:
            sqla_conversation: SQLAConversation | None = self.session.get(SQLAConversation, conversation_id)

        except Exception as e:
            self.logger.error(f"Error while querying the database for conversation with ID {conversation_id}: {e}")
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying the database for conversation with ID {conversation_id}: {e}",
                errorName="ErrorWhileQueryingDatabase",
                errorType="ErrorWhileQueryingDatabase",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if sqla_conversation is None:
            self.logger.error(f"Conversation with ID {conversation_id} not found in the database.")
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_message: SQLAAgentMessage | SQLAUserMessage

        # 2. If thread ID not provided, get the highest thread ID and increment by one

        max_thread_result: int = 0

        if thread_id is None:
            # max_thread_query: Select = select(
            #     func.max(SQLAMessageBase.thread_id).label("max_thread_id")
            # )
            # max_thread_result: Result = self._session.execute(max_thread_query).all()
            # max_thread_result = self._session.query(
            #     func.max(SQLAMessageBase.thread_id).label("max_thread_id")
            # ).first()

            max_thread_result = self._session.query(
                func.max(SQLAMessageBase.thread_id)
            ).first()

            # max_thread_id: int = [
            #     row.max_thread_id for row in max_thread_result
            # ] if max_thread_result else 0

            # max_thread_id: int = max_thread_result.max_thread_id if max_thread_result else 0
            if max_thread_result and max_thread_result > 0:
                max_thread_id = max_thread_result

        thread_id = max_thread_id + 1

        # 3. Create the message object based on its type

        if sender_type == MessageSenderTypeEnum.AGENT:
            sqla_message = SQLAAgentMessage(
                thread_id=thread_id,
                message_contents=[SQLAMessageContent(
                    content=content
                ) for content in message_contents],
                timestamp=timestamp,
                conversation_id=conversation_id,
            )

        elif sender_type == MessageSenderTypeEnum.USER:
            sqla_message = SQLAUserMessage(
                thread_id=thread_id,
                message_contents=[SQLAMessageContent(
                    content=content
                ) for content in message_contents],
                timestamp=timestamp,
                conversation_id=conversation_id,
            )

        else:
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage="Invalid sender type provided",
                errorName="Invalid sender type",
                errorType="InvalidSenderType",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 4. Add the contents and commit

        try:
            sqla_message.save(session=self.session)

            # sqla_message_content: SQLAMessageContent = SQLAMessageContent(
            #     content=content,
            #     message_id=message_id,
            # )
            self.session.commit()

            # for content in message_contents:
            #     message_content_dto: NewMessageContentDTO = self.new_message_content(
            #         sqla_message.id,
            #         content,
            #     )

            #     if not message_content_dto.status:
            #         errorDTO = NewMessageDTO(
            #             status=False,
            #             errorCode=message_content_dto.errorCode,
            #             errorMessage=message_content_dto.errorMessage,
            #             errorName=message_content_dto.errorName,
            #             errorType=message_content_dto.errorType,
            #         )
            #         return errorDTO

            #     sqla_message.message_contents.append(message_content_dto.data)

            core_message: UserMessage | AgentMessage

            if isinstance(sqla_message, SQLAUserMessage):
                core_message = convert_sqla_client_message_to_core_user_message(sqla_message)

            elif isinstance(sqla_message, SQLAAgentMessage):
                core_message = convert_sqla_agent_message_to_core_agent_message(sqla_message)

            return NewMessageDTO(status=True, data=core_message)

        except Exception as e:
            self.logger.error(f"Error while sending message to conversation: {e}")
            errorDTO = NewMessageDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while sending message to conversation: {e}",
                errorName="Error while sending message to conversation",
                errorType="ErrorWhileSendingMessageToConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
