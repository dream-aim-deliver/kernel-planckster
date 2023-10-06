from distutils import core
from typing import List
from lib.core.dto.conversation_repository_dto import ConversationDTO
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
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAConversation, SQLAResearchContext, SQLAUser


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
                status="error",
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
                status="error",
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

        except Exception as e:
            self.logger.error(f"Error while creating new conversation: {e}")
            errorDTO = ConversationDTO(
                status="error",
                errorCode=-1,  # TODO: is this code ok?
                errorMessage=f"Error while creating new conversation: {e}",
                errorName="Error while creating new conversation",
                errorType="ErrorWhileCreatingNewConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        return ConversationDTO(status="success")

    def get_conversation(self, conversation_id: int) -> GetConversationDTO[TMessageBase] | ErrorConversationDTO:
        """ """
        if conversation_id is None:
            errorDTO = ErrorConversationDTO(
                status="error",
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
            errorDTO = ErrorConversationDTO(
                status="error",
                errorCode=-1,
                errorMessage=f"Conversation with ID {conversation_id} not found in the database.",
                errorName="Conversation not found",
                errorType="ConversationNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_user: SQLAUser | None = (
            self.session.query(SQLAUser).filter_by(id=sqla_conversation.research_context.user_id).first()
        )

        if sqla_user is None:
            self.logger.error(f"User with ID {sqla_conversation.research_context.user_id} not found in the database.")
            errorDTO = ErrorConversationDTO(
                status="error",
                errorCode=-1,
                errorMessage=f"User with ID {sqla_conversation.research_context.user_id} not found in the database.",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user = User(
            created_at=sqla_user.created_at,
            updated_at=sqla_user.updated_at,
            planckster_user_uuid=sqla_user.planckster_user_uuid,
        )

        sqla_llm: SQLALLM | None = (
            self.session.query(SQLALLM).filter_by(id=sqla_conversation.research_context.llm_id).first()
        )

        if sqla_llm is None:
            self.logger.error(f"LLM with ID {sqla_conversation.research_context.llm_id} not found in the database.")
            errorDTO = ErrorConversationDTO(
                status="error",
                errorCode=-1,
                errorMessage=f"LLM with ID {sqla_conversation.research_context.llm_id} not found in the database.",
                errorName="LLM not found",
                errorType="LLMNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_embedding_models: List[EmbeddingModel] = []
        for sqla_embedding_model in sqla_llm.embedding_models:
            core_embedding_models.append(
                EmbeddingModel(
                    id=sqla_embedding_model.id,
                    name=sqla_embedding_model.name,
                )
            )

        core_llm = LLM(
            id=sqla_llm.id,
            llm_name=sqla_llm.llm_name,
            embedding_models=core_embedding_models,
        )

        core_source_data: List[SourceData] = []
        for sqla_source_data in sqla_conversation.research_context.source_data:
            core_source_data.append(
                SourceData(
                    created_at=sqla_source_data.created_at,
                    updated_at=sqla_source_data.updated_at,
                    deleted=sqla_source_data.deleted,
                    deleted_at=sqla_source_data.deleted_at,
                    id=sqla_source_data.id,
                    name=sqla_source_data.name,
                    type=sqla_source_data.type,
                    lfn=sqla_source_data.lfn,
                    protocol=sqla_source_data.protocol,
                    knowledge_source=sqla_source_data.knowledge_source,
                )
            )

        core_research_context = ResearchContext(
            id=sqla_conversation.research_context.id,
            title=sqla_conversation.research_context.title,
            planckster_tagger_node_id=sqla_conversation.research_context.user_id,
            user=core_user,
            llm=core_llm,
            source_data=core_source_data,
        )

        core_conversation = Conversation(
            created_at=sqla_conversation.created_at,
            updated_at=sqla_conversation.updated_at,
            deleted=sqla_conversation.deleted,
            deleted_at=sqla_conversation.deleted_at,
            id=sqla_conversation.id,
            title=sqla_conversation.title,
            research_context=core_research_context,
        )

        core_messages: List[MessageBase] = []

        for sqla_message in sqla_conversation.messages:
            if sqla_message.type == "message_query":
                core_messages.append(
                    MessageQuery(
                        created_at=sqla_message.created_at,
                        updated_at=sqla_message.updated_at,
                        deleted=sqla_message.deleted,
                        deleted_at=sqla_message.deleted_at,
                        id=sqla_message.id,
                        content=sqla_message.content,
                        timestamp=sqla_message.timestamp,
                        conversation=core_conversation,
                        user=core_user,
                    )
                )
            if sqla_message.type == "message_response":
                core_messages.append(
                    MessageResponse(
                        created_at=sqla_message.created_at,
                        updated_at=sqla_message.updated_at,
                        deleted=sqla_message.deleted,
                        deleted_at=sqla_message.deleted_at,
                        id=sqla_message.id,
                        content=sqla_message.content,
                        timestamp=sqla_message.timestamp,
                        conversation=core_conversation,
                    )
                )

        return GetConversationDTO(
            created_at=sqla_conversation.created_at,
            updated_at=sqla_conversation.updated_at,
            deleted=sqla_conversation.deleted,
            deleted_at=sqla_conversation.deleted_at,
            id=sqla_conversation.id,
            title=sqla_conversation.title,
            research_context=core_research_context,
            status="success",
            messages=core_messages,
        )
