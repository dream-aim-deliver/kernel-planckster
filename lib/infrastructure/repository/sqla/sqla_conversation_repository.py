from distutils import core
from typing import List
from lib.core.dto.conversation_repository_dto import (
    ConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
)
from lib.core.entity.models import (
    LLM,
    Conversation,
    EmbeddingModel,
    MessageBase,
    MessageQuery,
    MessageResponse,
    ResearchContext,
    SourceData,
    TMessageBase,
    User,
)
from lib.core.ports.secondary.conversation_repository import ConversationRepository
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLAUser,
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
        @return: A DTO containing the result of the operation.
        @rtype: SuccessConversationDTO | ErrorConversationDTO
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
            new_conversation = self.session.query(SQLAConversation).filter_by(id=sqla_new_conversation.id)[-1]
            return ConversationDTO(status="success", conversation_id=new_conversation.id)
        except Exception as e:
            self.logger.error(f"Error while creating new conversation: {e}")
            errorDTO = ConversationDTO(
                status=False,
                errorCode=-1,  # TODO: is this code ok?
                errorMessage=f"Error while creating new conversation: {e}",
                errorName="Error while creating new conversation",
                errorType="ErrorWhileCreatingNewConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

<<<<<<< HEAD
        return ConversationDTO(status="success")

    def get_conversation_research_context(self, conversation_id: int) -> GetConversationResearchContextDTO:
        """ """
=======
    def get_conversation_research_context(self, conversation_id: int) -> GetConversationResearchContextDTO:
        """ """

    def get_conversation(self, conversation_id: int) -> GetConversationDTO[TMessageBase] | ErrorConversationDTO:
        """ """
>>>>>>> bd17aa7 (sqla: return id of newly created conversation #13)
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
<<<<<<< HEAD

    def list_conversation_messages(self, conversation_id: int) -> ListConversationMessagesDTO[TMessageBase]:
        """ """
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
=======
>>>>>>> bd17aa7 (sqla: return id of newly created conversation #13)
