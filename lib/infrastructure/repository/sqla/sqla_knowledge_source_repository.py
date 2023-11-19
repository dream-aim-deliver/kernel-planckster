from typing import Dict, List
from lib.core.dto.knowledge_source_repository_dto import NewSourceDataDTO
from lib.core.entity.models import SourceData
from lib.core.ports.secondary.knowledge_source_repository import KnowledgeSourceRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData


class SQLAKnowledgeSourceRepository(KnowledgeSourceRepositoryOutputPort):
    """
    A SQLAlchemy implementation of the knowledge source repository.
    """

    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

    def new_source_data(self, knowledge_source_id: int, source_data_list: List[SourceData]) -> NewSourceDataDTO:
        """
        Creates a new source data.

        @param knowledge_source_id: The ID of the knowledge source to create the source data for.
        @type knowledge_source_id: int
        @param source_data_list: The list of source data to create.
        @type source_data_list: List[SourceData]
        @return: A DTO containing the result of the operation.
        @rtype: NewSourceDataDTO
        """

        if knowledge_source_id is None:
            self.logger.error("Knowledge source ID cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Knowledge source ID cannot be None",
                errorName="KnowledgeSourceIdNotProvided",
                errorType="KnowledgeSourceIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if source_data_list is None:
            self.logger.error("Source data cannot be None")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data cannot be None",
                errorName="SourceDataNotProvided",
                errorType="SourceDataNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if len(source_data_list) == 0:
            self.logger.error("Source data list cannot be empty")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data list cannot be empty",
                errorName="SourceDataListEmpty",
                errorType="SourceDataListEmpty",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_source_data_list: List[SQLASourceData] = []

        for source_data in source_data_list:
            if not isinstance(source_data, SourceData):
                self.logger.error(f"Source data {source_data} is not a valid SourceData object")
                errorDTO = NewSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Source data {source_data} is not a valid SourceData object",
                    errorName="SourceDataNotValid",
                    errorType="SourceDataNotValid",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            sqla_source_data = SQLASourceData(
                name=source_data.name,
                type=source_data.type,
                lfn=source_data.lfn,
                protocol=source_data.protocol,
                status=source_data.status,
            )

            sqla_source_data_list.append(sqla_source_data)

        sqla_knowledge_source: SQLAKnowledgeSource | None = self.session.get(SQLAKnowledgeSource, knowledge_source_id)

        if sqla_knowledge_source is None:
            self.logger.error(f"Knowledge source with ID {knowledge_source_id} not found in the database")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Knowledge source with ID {knowledge_source_id} not found in the database",
                errorName="KnowledgeSourceNotFound",
                errorType="KnowledgeSourceNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        success_source_data_lfn_list: List[str] = []
        error_source_data_lfn_list: List[str] = []
        error_source_data_dict: Dict[str, str] = {}

        for sqla_source_datum in sqla_source_data_list:
            # TODO: fix this: if the second element of the input list is a duplicate of the first one, the first one will be added (correct), the second one catched in the duplicates list (correct), but from the third one onwards everything will fail because SQLA had an error in the session
            try:
                sqla_knowledge_source = self.session.get(SQLAKnowledgeSource, knowledge_source_id)
                sqla_knowledge_source.source_data.append(sqla_source_datum)  # type: ignore
                self.session.commit()
                success_source_data_lfn_list.append(sqla_source_datum.lfn)

            except Exception as e:
                error_source_data_lfn_list.append(sqla_source_datum.lfn)
                error_str = str(e).split("SQL:", 1)[0]
                error_source_data_dict[sqla_source_datum.lfn] = error_str
                continue

        if success_source_data_lfn_list != []:
            if error_source_data_lfn_list != []:
                self.logger.error(
                    f"Success for the following lfns: {success_source_data_lfn_list},\n\nbut error while creating source data for the following lfns: {error_source_data_dict}"
                )

                halfErrorDTO = NewSourceDataDTO(
                    status=True,
                    errorCode=-1,
                    errorMessage=f"Success for the following lfns: {success_source_data_lfn_list},\n\nbut error while creating source data for the following lfns: {error_source_data_dict}",
                    errorName="Success but Source Data creation error for some source data",
                    errorType="SuccesButSourceDataCreationError",
                )
                self.logger.error(f"{halfErrorDTO}")
                return halfErrorDTO

            else:
                return NewSourceDataDTO(
                    status=True,
                )

        else:
            self.logger.error(f"Error while creating source data for the following lfns: {error_source_data_dict}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating source data for the following lfns: {error_source_data_dict}",
                errorName="Source Data creation error",
                errorType="SourceDataCreationError",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

            ##with self.session.begin():
            # sqla_knowledge_source.update(
            # {"source_data": updated_sqla_source_data_list},
            # session=self.session,
            # )
            # sqla_knowledge_source.save(session=self.session)
            # self.session.commit()
