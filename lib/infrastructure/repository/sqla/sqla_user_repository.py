from typing import Dict, List
from lib.core.dto.user_repository_dto import GetUserDTO, ListUserResearchContextsDTO, NewResearchContextDTO
from lib.core.entity.models import LLM, ResearchContext, SourceData, User, VectorStore
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
    convert_sqla_LLM_to_core_LLM,
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
        self,
        research_context_title: str,
        research_context_description: str,
        user_sid: str,
        llm_name: str,
        source_data_ids: List[int],
    ) -> NewResearchContextDTO:
        """
        Creates a new research context for a user.

        @param research_context_title: The title of the research context.
        @type research_context_title: str
        @param research_context_description: The description of the research context.
        @type research_context_description: str
        @param user_sid: The SID of the user to create the research context for.
        @type user_sid: str
        @param llm_name: The name of the LLM to create the research context for.
        @type llm_name: str
        @param source_data_ids: The IDs of the source data to create the research context for.
        @type source_data_ids: List[int]
        @return: A DTO containing the result of the operation.
        @rtype: NewUserResearchContextDTO
        """

        # 0. Check that research_context_title is not None
        if research_context_title is None:
            self.logger.error("Research context title cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research context title cannot be None",
                errorName="Research context title not provided",
                errorType="ResearchContextTitleNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if research_context_description is None:
            self.logger.error("Research context description cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Research context description cannot be None",
                errorName="Research context description not provided",
                errorType="ResearchContextDescriptionNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 1. Get SQLAUser and SQLALLM from the database
        if user_sid is None:
            self.logger.error("User SID cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="User SID cannot be None",
                errorName="User SID not provided",
                errorType="UserSidNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if llm_name is None:
            self.logger.error("LLM name cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="LLM name cannot be None",
                errorName="LLM name not provided",
                errorType="LLMNameNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            queried_sqla_llm: SQLALLM | None = self.session.query(SQLALLM).filter_by(llm_name=llm_name).first()

        except Exception as e:
            self.logger.error(f"Error while querying for LLM: {e}")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying for LLM: {e}",
                errorName="Error while querying for LLM",
                errorType="ErrorWhileQueryingForLLM",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if queried_sqla_llm is None:
            self.logger.error(f"LLM with name {llm_name} not found in the database")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"LLM with name {llm_name} not found in the database",
                errorName="LLM not found",
                errorType="LLMNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            queried_sqla_user: SQLAUser | None = self.session.query(SQLAUser).filter_by(sid=user_sid).first()

        except Exception as e:
            self.logger.error(f"Error while querying for user: {e}")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying for user: {e}",
                errorName="Error while querying for user",
                errorType="ErrorWhileQueryingForUser",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if queried_sqla_user is None:
            self.logger.error(f"User with SID {user_sid} not found in the database")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"User with SID {user_sid} not found in the database",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 2. Handle source data IDs
        if source_data_ids is None:
            self.logger.error("Source data cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data cannot be None",
                errorName="Source data not provided",
                errorType="SourceDataNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if source_data_ids == []:
            self.logger.error("Source data list cannot be empty")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data list cannot be empty",
                errorName="Source data list empty",
                errorType="SourceDataListEmpty",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # Make the IDs unique
        source_data_ids = list(set(source_data_ids))

        sqla_source_data: List[SQLASourceData] = []
        sqla_source_data_error_ids: List[int] = []
        sqla_source_data_error_dict: Dict[str, str] = {}

        for source_datum_id in source_data_ids:
            try:
                sqla_source_datum = self.session.get(SQLASourceData, source_datum_id)

                if sqla_source_datum is None:
                    sqla_source_data_error_ids.append(source_datum_id)
                    sqla_source_data_error_dict[f"ID {source_datum_id}"] = "Source data not found in the database"
                    continue

                sqla_source_data.append(sqla_source_datum)

            except Exception as e:
                sqla_source_data_error_ids.append(source_datum_id)
                sqla_source_data_error_dict[
                    f"ID {source_datum_id}"
                ] = f"Error while getting source data from the database: {e}"
                continue

        if sqla_source_data_error_ids != []:
            self.logger.error(
                f"Error with the following source data. Operation aborted.\n\n {sqla_source_data_error_dict}"
            )
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error with the following source data. Operation aborted.\n\n {sqla_source_data_error_dict}",
                errorName="Source data database errors",
                errorType="SourceDataDatabaseErrors",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 3. Create the new research context

        llm_id = queried_sqla_llm.id
        user_id = queried_sqla_user.id

        sqla_new_research_context: SQLAResearchContext = SQLAResearchContext(
            title=research_context_title,
            description=research_context_description,
            user_id=user_id,
            llm_id=llm_id,
            source_data=sqla_source_data,
        )

        try:
            sqla_new_research_context.save(session=self.session)
            self.session.commit()

        except Exception as e:
            self.logger.error(f"Error while creating new research context: {e}")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating new research context: {e}",
                errorName="Error while creating new research context",
                errorType="ErrorWhileCreatingNewResearchContext",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_new_research_context: ResearchContext = convert_sqla_research_context_to_core_research_context(
            sqla_new_research_context
        )

        core_llm: LLM = convert_sqla_LLM_to_core_LLM(queried_sqla_llm)

        return NewResearchContextDTO(
            status=True,
            research_context=core_new_research_context,
            llm=core_llm,
        )

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
