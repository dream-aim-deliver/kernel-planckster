from typing import List
from lib.core.dto.user_repository_dto import GetUserDTO, ListUserResearchContextsDTO, NewUserResearchContextDTO
from lib.core.entity.models import ResearchContext, SourceData, User, VectorStore
from lib.core.ports.secondary.user_repository import UserRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAResearchContext,
    SQLASourceData,
    SQLAUser,
    SQLAVectorStore,
)
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_user_to_core_user,
)


class SQLAUserRepository(UserRepositoryOutputPort):
    """
    A SQLAlchemy implementation of the user repository.
    """

    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

    def get_user(self, user_id: int) -> GetUserDTO:
        """
        Gets a user by ID.

        @param user_id: The ID of the user to get.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetUserDTO
        """

        if user_id is None:
            self.logger.error("User ID cannot be None")
            errorDTO = GetUserDTO(
                status=False,
                errorCode=-1,
                errorMessage="User ID cannot be None",
                errorName="User ID not provided",
                errorType="UserIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_user: SQLAUser | None = self.session.get(SQLAUser, user_id)

        if sqla_user is None:
            self.logger.error(f"User with ID {user_id} not found in the database")
            errorDTO = GetUserDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"User with ID {user_id} not found in the database",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user: User = convert_sqla_user_to_core_user(sqla_user)

        return GetUserDTO(status=True, data=core_user)

    def new_research_context(
        self, research_context_title: str, user_id: int, llm_id: int, source_data_ids: List[int]
    ) -> NewUserResearchContextDTO:
        """
        Creates a new research context for a user.

        @param research_context_title: The title of the research context.
        @type research_context_title: str
        @param user_id: The ID of the user to create the research context for.
        @type user_id: int
        @param llm_id: The ID of the LLM tied to the research context.
        @type llm_id: int
        @param source_data: The source data tied to the research context.
        @type source_data: List[SourceData]
        @param vector_store: The vector store tied to the research context.
        @type vector_store: VectorStore
        @return: A DTO containing the result of the operation.
        @rtype: NewUserResearchContextDTO
        """
        # TODO: vector store should be nullable
        if user_id is None:
            self.logger.error("User ID cannot be None")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="User ID cannot be None",
                errorName="User ID not provided",
                errorType="UserIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if llm_id is None:
            self.logger.error("LLM ID cannot be None")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="LLM ID cannot be None",
                errorName="LLM ID not provided",
                errorType="LLMIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if source_data_ids is None:
            self.logger.error("Source data cannot be None")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data cannot be None",
                errorName="Source data not provided",
                errorType="SourceDataNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if source_data_ids == []:
            self.logger.error("Source data cannot be empty")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data cannot be empty",
                errorName="Source data empty",
                errorType="SourceDataEmpty",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_source_data: List[SQLASourceData] = []
        sqla_source_data_error_ids: List[int] = []

        for source_data_id in source_data_ids:
            try:
                sqla_source_datum = self.session.get(SQLASourceData, source_data_id)

                if sqla_source_datum is None:
                    sqla_source_data_error_ids.append(source_data_id)
                    continue

                sqla_source_data.append(sqla_source_datum)

            except:
                sqla_source_data_error_ids.append(source_data_id)
                continue

        if sqla_source_data_error_ids != []:
            self.logger.error(f"Source data with IDs {sqla_source_data_error_ids} not found in the database")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Source data with IDs {sqla_source_data_error_ids} not found in the database",
                errorName="Source data not found",
                errorType="SourceDataNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_new_research_context: SQLAResearchContext = SQLAResearchContext(
            title=research_context_title,
            user_id=user_id,
            llm_id=llm_id,
            source_data=sqla_source_data,
        )

        try:
            sqla_new_research_context.save(session=self.session)
            self.session.commit()

            return NewUserResearchContextDTO(status=True, research_context_id=sqla_new_research_context.id)

        except Exception as e:
            self.logger.error(f"Error while creating new research context: {e}")
            errorDTO = NewUserResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating new research context: {e}",
                errorName="Error while creating new research context",
                errorType="ErrorWhileCreatingNewResearchContext",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

    def list_research_contexts(self, user_id: int) -> ListUserResearchContextsDTO:
        """
        Lists all research contexts for a user.

        @param user_id: The ID of the user to list research contexts for.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListUserResearchContextsDTO
        """

        if user_id is None:
            self.logger.error("User ID cannot be None")
            errorDTO = ListUserResearchContextsDTO(
                status=False,
                errorCode=-1,
                errorMessage="User ID cannot be None",
                errorName="User ID not provided",
                errorType="UserIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_user: SQLAUser | None = self.session.get(SQLAUser, user_id)

        if sqla_user is None:
            self.logger.error(f"User with ID {user_id} not found in the database")
            errorDTO = ListUserResearchContextsDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"User with ID {user_id} not found in the database",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_contexts: List[SQLAResearchContext] = sqla_user.research_contexts
        core_research_contexts: List[ResearchContext] = []

        for sqla_research_context in sqla_research_contexts:
            core_research_context = convert_sqla_research_context_to_core_research_context(sqla_research_context)
            core_research_contexts.append(core_research_context)

        return ListUserResearchContextsDTO(status=True, data=core_research_contexts)
