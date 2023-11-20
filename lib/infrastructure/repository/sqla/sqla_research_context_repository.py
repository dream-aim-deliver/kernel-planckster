from typing import List
from lib.core.dto.research_context_repository_dto import (
    GetResearchContextDTO,
    GetResearchContextUserDTO,
    ListResearchContextConversationsDTO,
    NewResearchContextConversationDTO,
    UpdateResearchContextVectorStoreDTO,
)
from lib.core.entity.models import Conversation, ProtocolEnum, ResearchContext
from lib.core.ports.secondary.research_context_repository import ResearchContextRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import (
    SQLAConversation,
    SQLAEmbeddingModel,
    SQLAResearchContext,
    SQLAUser,
    SQLAVectorStore,
)
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_conversation_to_core_conversation,
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_user_to_core_user,
)


class SQLAReseachContextRepository(ResearchContextRepositoryOutputPort):
    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

    def get_research_context(self, research_context_id: int) -> GetResearchContextDTO:
        """
        Gets a research context by ID.

        @param research_context_id: The ID of the research context to get.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetResearchContextDTO
        """

        if research_context_id is None:
            errorDTO = GetResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = self.session.get(SQLAResearchContext, research_context_id)

        if sqla_research_context is None:
            self.logger.error(f"Research context {research_context_id} not found.")
            errorDTO = GetResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_research_context: ResearchContext = convert_sqla_research_context_to_core_research_context(
            sqla_research_context
        )

        return GetResearchContextDTO(status=True, data=core_research_context)

    def update_research_context_vector_store(
        self,
        research_context_id: int,
        vector_store_id: int,
    ) -> UpdateResearchContextVectorStoreDTO:
        """
        Updates the vector store of a research context.

        @param research_context_id: The ID of the research context to update the vector store for.
        @type research_context_id: int
        @param vector_store_id: The ID of the vector store to set.
        @type vector_store_id: int
        """

        if research_context_id is None:
            self.logger.error(f"Research Context ID cannot be None")
            errorDTO = UpdateResearchContextVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        queried_sqla_research_context: SQLAResearchContext | None = self.session.get(
            SQLAResearchContext, research_context_id
        )

        if queried_sqla_research_context is None:
            self.logger.error(f"Research context with ID {research_context_id} not found.")
            errorDTO = UpdateResearchContextVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if vector_store_id is None:
            self.logger.error(f"Vector Store ID cannot be None")
            errorDTO = UpdateResearchContextVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage="Vector Store ID cannot be None",
                errorName="Vector Store ID not provided",
                errorType="VectorStoreIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        queried_sqla_vector_store: SQLAVectorStore | None = self.session.get(SQLAVectorStore, vector_store_id)

        if queried_sqla_vector_store is None:
            self.logger.error(f"Vector store with ID {vector_store_id} not found.")
            errorDTO = UpdateResearchContextVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Vector Store with ID {vector_store_id} not found in the database.",
                errorName="Vector Store not found",
                errorType="VectorStoreNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            queried_sqla_research_context.update({"vector_store": queried_sqla_vector_store}, session=self.session)
            self.session.commit()

            return UpdateResearchContextVectorStoreDTO(
                status=True,
                research_context_id=queried_sqla_research_context.id,
                vector_store_id=queried_sqla_research_context.vector_store.id,
            )

        except Exception as e:
            self.logger.error(f"Error while updating vector store of research context: {e}")
            errorDTO = UpdateResearchContextVectorStoreDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while updating vector store of research context: {e}",
                errorName="Error while updating vector store of research context",
                errorType="ErrorWhileUpdatingVectorStoreOfResearchContext",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

    def get_research_context_user(self, research_context_id: int) -> GetResearchContextUserDTO:
        """
        Gets the user of a research context.

        @param research_context_id: The ID of the research context to get the user for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetResearchContextUserDTO
        """

        if research_context_id is None:
            errorDTO = GetResearchContextUserDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = self.session.get(SQLAResearchContext, research_context_id)

        if sqla_research_context is None:
            self.logger.error(f"Research context {research_context_id} not found.")
            errorDTO = GetResearchContextUserDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_user: SQLAUser | None = sqla_research_context.user

        if sqla_user is None:
            self.logger.error(f"User of research context {research_context_id} not found in the database.")
            errorDTO = GetResearchContextUserDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"User of research context with ID {research_context_id} not found in the database.",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user = convert_sqla_user_to_core_user(sqla_user)

        return GetResearchContextUserDTO(status=True, data=core_user)

    def new_conversation(self, research_context_id: int, conversation_title: str) -> NewResearchContextConversationDTO:
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
            errorDTO = NewResearchContextConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if conversation_title is None:
            errorDTO = NewResearchContextConversationDTO(
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
            errorDTO = NewResearchContextConversationDTO(
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
            self.session.commit()

            return NewResearchContextConversationDTO(status=True, conversation_id=sqla_new_conversation.id)

        except Exception as e:
            self.logger.error(f"Error while creating new conversation: {e}")
            errorDTO = NewResearchContextConversationDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating new conversation: {e}",
                errorName="Error while creating new conversation",
                errorType="ErrorWhileCreatingNewConversation",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

    def list_conversations(self, research_context_id: int) -> ListResearchContextConversationsDTO:
        """
        Lists all conversations in the research context.

        @return: A DTO containing the result of the operation.
        @rtype: ListResearchContextConversationsDTO
        """

        if research_context_id is None:
            errorDTO = ListResearchContextConversationsDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = self.session.get(SQLAResearchContext, research_context_id)

        if sqla_research_context is None:
            self.logger.error(f"Research context {research_context_id} not found.")
            errorDTO = ListResearchContextConversationsDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_conversations: List[SQLAConversation] = sqla_research_context.conversations
        core_conversations: List[Conversation] = []

        for sqla_conversation in sqla_conversations:
            core_conversation = convert_sqla_conversation_to_core_conversation(sqla_conversation)
            core_conversations.append(core_conversation)

        return ListResearchContextConversationsDTO(
            status=True,
            data=core_conversations,
        )
