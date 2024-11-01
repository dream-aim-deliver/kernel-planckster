from typing import List, Callable
from contextlib import _GeneratorContextManager
from lib.core.dto.research_context_repository_dto import (
    GetResearchContextDTO,
    GetResearchContextClientDTO,
    ListResearchContextConversationsDTO,
    ListSourceDataDTO,
    NewResearchContextConversationDTO,
)
from lib.core.entity.models import Conversation, ResearchContext, SourceData
from lib.core.ports.secondary.research_context_repository import ResearchContextRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLAConversation, SQLAResearchContext, SQLAClient
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_conversation_to_core_conversation,
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_source_data_to_core_source_data,
    convert_sqla_client_to_core_client,
    session_context,
)


class SQLAReseachContextRepository(ResearchContextRepositoryOutputPort):
    def __init__(self, session_generator_factory: Callable[[], _GeneratorContextManager[Session]]) -> None:
        super().__init__()
        self._session_generator = session_generator_factory()

    # @property
    def session_generator(self) -> _GeneratorContextManager[Session]:
        return self._session_generator

    @session_context()
    def get_research_context(self, session: Session, research_context_id: int) -> GetResearchContextDTO:
        """
        Gets a research context by ID.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
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

        sqla_research_context: SQLAResearchContext | None = session.get(SQLAResearchContext, research_context_id)

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

    @session_context()
    def get_research_context_client(self, session: Session, research_context_id: int) -> GetResearchContextClientDTO:
        """
        Gets the user of a research context.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param research_context_id: The ID of the research context to get the user for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetResearchContextClientDTO
        """

        if research_context_id is None:
            errorDTO = GetResearchContextClientDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = session.get(SQLAResearchContext, research_context_id)

        if sqla_research_context is None:
            self.logger.error(f"Research context {research_context_id} not found.")
            errorDTO = GetResearchContextClientDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research Context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_client: SQLAClient | None = sqla_research_context.client

        if sqla_client is None:
            self.logger.error(f"Client of research context {research_context_id} not found in the database.")
            errorDTO = GetResearchContextClientDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client of research context with ID {research_context_id} not found in the database.",
                errorName="Client not found",
                errorType="ClientNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user = convert_sqla_client_to_core_client(sqla_client)

        return GetResearchContextClientDTO(status=True, data=core_user)

    @session_context()
    def new_conversation(
        self,
        session: Session,
        research_context_id: int,
        conversation_title: str,
    ) -> NewResearchContextConversationDTO:
        """
        Creates a new conversation in the research context.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
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

        sqla_research_context: SQLAResearchContext | None = session.get(SQLAResearchContext, research_context_id)

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
            sqla_new_conversation.save(session=session)
            session.commit()

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

    @session_context()
    def list_conversations(self, session: Session, research_context_id: int) -> ListResearchContextConversationsDTO:
        """
        Lists all conversations in the research context.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param research_context_id: The ID of the research context to list source data for.
        @type research_context_id: int
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

        sqla_research_context: SQLAResearchContext | None = session.get(SQLAResearchContext, research_context_id)

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

    @session_context()
    def list_source_data(self, session: Session, research_context_id: int) -> ListSourceDataDTO:
        """
        Lists all source data related to a research context.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param research_context_id: The ID of the research context to list source data for.
        @type research_context_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListSourceDataDTO
        """

        if research_context_id is None:
            errorDTO = ListSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research Context ID cannot be None",
                errorName="Research Context ID not provided",
                errorType="ResearchContextIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_context: SQLAResearchContext | None = session.get(SQLAResearchContext, research_context_id)

        if sqla_research_context is None:
            self.logger.error(f"Research context with ID {research_context_id} not found in the database.")
            errorDTO = ListSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research context with ID {research_context_id} not found in the database.",
                errorName="Research Context not found",
                errorType="ResearchContextNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_source_data = sqla_research_context.source_data

        core_source_data: List[SourceData] = []
        for sqla_source_datum in sqla_source_data:
            core_source_datum = convert_sqla_source_data_to_core_source_data(sqla_source_datum)
            core_source_data.append(core_source_datum)

        return ListSourceDataDTO(
            status=True,
            data=core_source_data,
        )
