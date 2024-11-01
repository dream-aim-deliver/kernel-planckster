from datetime import datetime
from typing import Dict, List, Callable
from contextlib import _GeneratorContextManager
from lib.core.dto.client_repository_dto import (
    GetClientDTO,
    ListResearchContextsDTO,
    ListSourceDataDTO,
    NewResearchContextDTO,
    NewSourceDataDTO,
)
from lib.core.entity.models import LLM, ProtocolEnum, ResearchContext, SourceData, Client, SourceDataStatusEnum
from lib.core.ports.secondary.client_repository import ClientRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAResearchContext,
    SQLASourceData,
    SQLAClient,
)
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_LLM_to_core_LLM,
    convert_sqla_research_context_to_core_research_context,
    convert_sqla_client_to_core_client,
    convert_core_source_data_to_sqla_source_data,
    convert_sqla_source_data_to_core_source_data,
    session_context,
)


class SQLAClientRepository(ClientRepositoryOutputPort):
    """
    A SQLAlchemy implementation of the client repository.
    """

    def __init__(self, session_generator_factory: Callable[[], _GeneratorContextManager[Session]]) -> None:
        super().__init__()
        self._session_generator = session_generator_factory()

    # @property
    def session_generator(self) -> _GeneratorContextManager[Session]:
        return self._session_generator

    @session_context()
    def get_client(self, session: Session, client_id: int) -> GetClientDTO:
        """
        Gets a client by ID.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_id: The ID of the client to get.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetClientDTO
        """

        if client_id is None:
            self.logger.error("Client ID cannot be None")
            errorDTO = GetClientDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client ID cannot be None",
                errorName="Client ID not provided",
                errorType="ClientIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_client: SQLAClient | None = session.get(SQLAClient, client_id)

        if sqla_client is None:
            self.logger.error(f"Client with ID {client_id} not found in the database")
            errorDTO = GetClientDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client with ID {client_id} not found in the database",
                errorName="Client not found",
                errorType="ClientNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user: Client = convert_sqla_client_to_core_client(sqla_client)

        return GetClientDTO(status=True, data=core_user)

    @session_context()
    def get_client_by_sub(self, session: Session, client_sub: str) -> GetClientDTO:
        """
        Gets a client by SUB.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_sub: The SUB of the client to get.
        @type client_sub: str
        @return: A DTO containing the result of the operation.
        @rtype: GetClientDTO
        """
        if client_sub is None:
            self.logger.error("Client SUB cannot be None")
            errorDTO = GetClientDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client SUB cannot be None",
                errorName="Client SUB not provided",
                errorType="ClientSubNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            sqla_client = session.query(SQLAClient).filter_by(sub=client_sub).first()

            if sqla_client is None:
                self.logger.error(f"Client with SUB {client_sub} not found in the database")
                errorDTO = GetClientDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Client with SUB {client_sub} not found in the database",
                    errorName="Client not found",
                    errorType="ClientNotFound",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            core_user: Client = convert_sqla_client_to_core_client(sqla_client)

            return GetClientDTO(status=True, data=core_user)

        except Exception as e:
            self.logger.error(f"Error while querying for client '{client_sub}': {e}")
            errorDTO = GetClientDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying for client '{client_sub}': {e}",
                errorName="Error while querying for user",
                errorType="ErrorWhileQueryingForClient",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

    @session_context()
    def new_research_context(
        self,
        session: Session,
        research_context_title: str,
        research_context_description: str,
        client_sub: str,
        llm_name: str,
        source_data_ids: List[int],
    ) -> NewResearchContextDTO:
        """
        Creates a new research context for a client.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param research_context_title: The title of the research context.
        @type research_context_title: str
        @param research_context_description: The description of the research context.
        @type research_context_description: str
        @param client_sub: The SUB of the user to create the research context for.
        @type client_sub: str
        @param llm_name: The name of the LLM to create the research context for.
        @type llm_name: str
        @param source_data_ids: The IDs of the source data to create the research context for.
        @type source_data_ids: List[int]
        @return: A DTO containing the result of the operation.
        @rtype: NewResearchContextDTO
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

        # 1. Get SQLAClient and SQLALLM from the database
        if client_sub is None:
            self.logger.error("Client SUB cannot be None")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client SUB cannot be None",
                errorName="Client SUB not provided",
                errorType="ClientSubNotProvided",
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
            queried_sqla_llm: SQLALLM | None = session.query(SQLALLM).filter_by(llm_name=llm_name).first()

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
            queried_sqla_client: SQLAClient | None = session.query(SQLAClient).filter_by(sub=client_sub).first()

        except Exception as e:
            self.logger.error(f"Error while querying for user: {e}")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while querying for user: {e}",
                errorName="Error while querying for user",
                errorType="ErrorWhileQueryingForClient",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if queried_sqla_client is None:
            self.logger.error(f"Client with SUB {client_sub} not found in the database")
            errorDTO = NewResearchContextDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client with SUB {client_sub} not found in the database",
                errorName="Client not found",
                errorType="ClientNotFound",
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
                sqla_source_datum = session.get(SQLASourceData, source_datum_id)

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
        client_id = queried_sqla_client.id

        sqla_new_research_context: SQLAResearchContext = SQLAResearchContext(
            title=research_context_title,
            description=research_context_description,
            client_id=client_id,
            llm_id=llm_id,
            source_data=sqla_source_data,
        )

        try:
            sqla_new_research_context.save(session=session)
            session.commit()

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

    @session_context()
    def list_research_contexts(self, session: Session, client_id: int) -> ListResearchContextsDTO:
        """
        Lists all research contexts for a client.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_id: The ID of the user to list research contexts for.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListResearchContextsDTO
        """

        if client_id is None:
            self.logger.error("Client ID cannot be None")
            errorDTO = ListResearchContextsDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client ID cannot be None",
                errorName="Client ID not provided",
                errorType="ClientIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_client: SQLAClient | None = session.get(SQLAClient, client_id)

        if sqla_client is None:
            self.logger.error(f"Client with ID {client_id} not found in the database")
            errorDTO = ListResearchContextsDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client with ID {client_id} not found in the database",
                errorName="Client not found",
                errorType="ClientNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_research_contexts: List[SQLAResearchContext] = sqla_client.research_contexts
        core_research_contexts: List[ResearchContext] = []

        for sqla_research_context in sqla_research_contexts:
            core_research_context = convert_sqla_research_context_to_core_research_context(sqla_research_context)
            core_research_contexts.append(core_research_context)

        return ListResearchContextsDTO(status=True, data=core_research_contexts)

    @session_context()
    def new_source_data(
        self,
        session: Session,
        client_id: int,
        source_data_name: str,
        protocol: ProtocolEnum,
        relative_path: str,
    ) -> NewSourceDataDTO:
        """
        Registers a new source data in the database for a given client.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_id: The ID of the client to create the source data for.
        @type client_id: int
        @param source_data_name: The name of the source data.
        @type source_data_name: str
        @param protocol: The protocol of the source data.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the source data.
        @type relative_path: str
        @return: A DTO containing the result of the operation.
        @rtype: NewSourceDataDTO
        """
        if client_id is None:
            self.logger.error("Client ID cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client ID cannot be None",
                errorName="ClientIdNotProvided",
                errorType="ClientIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 1. Check that the client exists in the database
        sqla_client = session.get(SQLAClient, client_id)

        if sqla_client is None:
            self.logger.error(f"Client with ID {client_id} not found in the database")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client with ID {client_id} not found in the database",
                errorName="Client Not Found",
                errorType="ClientNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if source_data_name is None:
            self.logger.error("Source data name cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data name cannot be None",
                errorName="SourceDataNameNotProvided",
                errorType="SourceDataNameNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if protocol is None:
            self.logger.error("Protocol cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Protocol cannot be None",
                errorName="Protocol Not Provided",
                errorType="ProtocolNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if relative_path is None:
            self.logger.error("Relative path cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Relative path cannot be None",
                errorName="Relative Path Not Provided",
                errorType="RelativePathNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 2. Validate all fields
        try:
            source_data_name_val = SourceData.name_validation(source_data_name)
            relative_path_val = SourceData.relative_path_validation(relative_path)
            protocol_val = SourceData.protocol_validation(protocol.value)
            type_val = SourceData.populate_type(relative_path_val)
            status = SourceDataStatusEnum.AVAILABLE

            sqla_source_data = SQLASourceData(
                name=source_data_name_val,
                protocol=protocol_val,
                relative_path=relative_path_val,
                type=type_val,
                status=status,
            )

        except Exception as e:
            self.logger.error(f"Error while creating source data '{sqla_source_data}': {e}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating source data '{sqla_source_data}': {e}",
                errorName="Source Data creation error",
                errorType="SourceDataCreationError",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        # 3. Check if the source data is already present in the database
        try:
            queried_source_data_list = (
                session.query(SQLASourceData)
                .filter_by(
                    client_id=sqla_client.id,
                    protocol=sqla_source_data.protocol,
                    relative_path=sqla_source_data.relative_path,
                )
                .all()
            )

            if len(queried_source_data_list) > 0:
                self.logger.error(f"Source data already present in the database: '{queried_source_data_list}'")
                errorDTO = NewSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Source data already present in the database: '{queried_source_data_list}'",
                    errorName="SourceDataAlreadyPresent",
                    errorType="SourceDataAlreadyPresent",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

        except Exception as e:
            self.logger.error(f"Couldn't assert uniqueness of source data in the database. Error:\n{e}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Couldn't assert uniqueness of source data in the database. Error:\n{e}",
                errorName="Couldn't Assert SourceData uniqueness",
                errorType="Couldn'tAssertSourceDataUniqueness",
            )
            return errorDTO

        # 4. We used a triple composite index, so SD is unique, so we can commit it
        try:
            sqla_client.source_data.append(sqla_source_data)
            session.commit()

            new_source_data = convert_sqla_source_data_to_core_source_data(sqla_source_data)

            return NewSourceDataDTO(status=True, data=new_source_data)

        except Exception as e:
            self.logger.error(f"Error while creating source data '{sqla_source_data}': {e}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating source data '{sqla_source_data}': {e}",
                errorName="Source Data creation error",
                errorType="SourceDataCreationError",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

            # TODO OLD: In the previous version (allowing for a list for source data, instead of just one): fix this: if the second element of the input list is a duplicate of the first one, the first one will be added (correct), the second one catched in the duplicates list (correct), but from the third one onwards everything will fail because SQLA had an error in the session

    @session_context()
    def list_source_data(self, session: Session, client_id: int) -> ListSourceDataDTO:
        """
        Lists source data for a given client.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_id: The ID of the client to list the source data for.
        @type client_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListSourceDataDTO
        """

        if client_id is None:
            self.logger.error("Client ID cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client ID cannot be None",
                errorName="ClientIdNotProvided",
                errorType="ClientIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            sqla_client: SQLAClient | None = session.get(SQLAClient, client_id)

        except Exception as e:
            self.logger.error(f"Could not query the database for client with ID {client_id}: {e}")
            errorDTO = ListSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not query the database for client with ID {client_id}: {e}",
                errorName="CouldNotListSourceData",
                errorType="CouldNotListSourceData",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if sqla_client is None:
            self.logger.error(f"Client with ID {client_id} not found in the database")
            errorDTO = ListSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Client with ID {client_id} not found in the database",
                errorName="Client Not Found",
                errorType="ClientNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            sqla_source_data_list = sqla_client.source_data

            core_source_data_list = [
                convert_sqla_source_data_to_core_source_data(sqla_sd) for sqla_sd in sqla_source_data_list
            ]

            return ListSourceDataDTO(
                status=True,
                data=core_source_data_list,
            )

        except Exception as e:
            self.logger.error(f"Could not list source data for client with ID {client_id}: {e}")
            errorDTO = ListSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not list source data for client with ID {client_id}: {e}",
                errorName="CouldNotListSourceData",
                errorType="CouldNotListSourceData",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
