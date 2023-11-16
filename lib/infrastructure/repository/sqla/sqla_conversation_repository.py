from typing import List, Set

from lib.core.dto.conversation_repository_dto import (
    ConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
    ListConversationSourcesDTO,
    ListConversationsDTO,
)
from lib.core.entity.models import (
    Conversation,
    MessageBase,
    MessageQuery,
    MessageResponse,
    ResearchContext,
    SourceData,
    TMessageBase,
)
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLACitation,
    SQLAConversation,
    SQLAMessageBase,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLASourceData,
)


class SQLAConversationRepository(ConversationRepository):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()

        with session_factory() as session:
            self.session = session

    def new_conversation(self, research_context_id: int, conversation_title: str) -> ConversationDTO:
        """
        Creates a new conversation in the research context.

        @param research_context_id: The ID of the research context to create the conversation in.
        @type research_context_id: int
        @param conversation_title: The title of the conversation.
        @type conversation_title: str
        @return: A DTO containing the result of the operation.
        @rtype: ConversationDTO
        """
        if research_context_id is None:
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if conversation_title is None:
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation title cannot be None",
                errorName="Conversation title not provided",
                errorType="ConversationTitleNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = (
            self.session.query(SQLAResearchContext).filter_by(id=research_context_id).first()
        )

        if sqla_research_context is None:
            self.logger.error(f"Research Context with ID {research_context_id} not found in the database.")
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_new_conversation: SQLAConversation = SQLAConversation(
            title=conversation_title,
            research_context_id=research_context_id,
            messages=[],
        )

        try:
            sqla_new_conversation.save(session=self.session)
            new_conversation = self.session.query(SQLAConversation).filter_by(id=sqla_new_conversation.id)[0]
            self.session.commit()

            return ConversationDTO(status=True, conversation_id=new_conversation.id)

        except Exception as e:
            self.logger.error(f"Error while creating new conversation: {e}")
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating new conversation: {e}",
                errorName="Error while creating new conversation",
                errorType="ErrorWhileCreatingNewConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

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

        core_research_context = ResearchContext(
            created_at=sqla_research_context.created_at,
            updated_at=sqla_research_context.updated_at,
            deleted=sqla_research_context.deleted,
            deleted_at=sqla_research_context.deleted_at,
            id=sqla_research_context.id,
            title=sqla_research_context.title,
        )

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
                core_message_query = MessageQuery(
                    created_at=sqla_message.created_at,
                    updated_at=sqla_message.updated_at,
                    deleted=sqla_message.deleted,
                    deleted_at=sqla_message.deleted_at,
                    id=sqla_message.id,
                    content=sqla_message.content,
                    timestamp=sqla_message.timestamp,
                )
                core_messages.append(core_message_query)
            if isinstance(sqla_message, SQLAMessageResponse):
                core_message_response = MessageResponse(
                    created_at=sqla_message.created_at,
                    updated_at=sqla_message.updated_at,
                    deleted=sqla_message.deleted,
                    deleted_at=sqla_message.deleted_at,
                    id=sqla_message.id,
                    content=sqla_message.content,
                    timestamp=sqla_message.timestamp,
                )
                core_messages.append(core_message_response)

        return ListConversationMessagesDTO[TMessageBase](
            status=True,
            data=core_messages,
        )

    def update_conversation(self, conversation_id: int, conversation_title: str) -> ConversationDTO:
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
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Conversation ID cannot be None",
                errorName="Conversation ID not provided",
                errorType="ConversationIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if conversation_title is None:
            errorDTO = ConversationDTO(
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
            errorDTO = ConversationDTO(
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

            return ConversationDTO(status=True, conversation_id=sqla_conversation.id)

        except Exception as e:
            self.logger.error(f"Error while updating the conversation: {e}")
            errorDTO = ConversationDTO(
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
            coresourcedatum = SourceData(
                created_at=sqlasourcedatum.created_at,
                updated_at=sqlasourcedatum.updated_at,
                deleted=sqlasourcedatum.deleted,
                deleted_at=sqlasourcedatum.deleted_at,
                id=sqlasourcedatum.id,
                name=sqlasourcedatum.name,
                type=sqlasourcedatum.type,
                lfn=sqlasourcedatum.lfn,
                protocol=sqlasourcedatum.protocol,
            )
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

    def list_conversations(self) -> ListConversationsDTO:
        """
        Lists all conversations in the database.

        @return: A DTO containing the result of the operation.
        @rtype: ListConversationsDTO
        """

        sqla_conversations: List[SQLAConversation] = self.session.query(SQLAConversation).all()

        if sqla_conversations == []:
            self.logger.error("No Conversations found in the database.")
            errorDTO = ListConversationsDTO(
                status=False,
                errorCode=-1,
                errorMessage="No Conversations found in the database.",
                errorName="No Conversations found",
                errorType="NoConversationsFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_conversations: List[Conversation] = []

        for sqla_conversation in sqla_conversations:
            core_conversations.append(
                Conversation(
                    created_at=sqla_conversation.created_at,
                    updated_at=sqla_conversation.updated_at,
                    deleted=sqla_conversation.deleted,
                    deleted_at=sqla_conversation.deleted_at,
                    id=sqla_conversation.id,
                    title=sqla_conversation.title,
                )
            )

        return ListConversationsDTO(
            status=True,
            data=core_conversations,
        )
