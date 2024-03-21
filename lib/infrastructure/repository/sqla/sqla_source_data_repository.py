from typing import List
from lib.core.dto.source_data_repository_dto import GetSourceDataByLFNDTO, ListSourceDataDTO
from lib.core.entity.models import LFN, SourceData
from lib.core.ports.secondary.source_data_repository import SourceDataRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_source_data_to_core_source_data


class SQLASourceDataRepository(SourceDataRepositoryOutputPort):
    """
    A SQLAlchemy implementation of the source data repository.
    """

    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

    def list_source_data(self, knowledge_source_id: int | None = None) -> ListSourceDataDTO:
        """
        Lists source data. If a knowledge source ID is provided, only source data for that knowledge source will be listed, otherwise all source data will be listed.

        @param knowledge_source_id: The ID of the knowledge source to list the source data for.
        @type knowledge_source_id: int
        @return: A DTO containing the result of the operation.
        @rtype: ListSourceDataDTO
        """

        if knowledge_source_id is None:
            self.logger.info("No knowledge source ID provided, listing all source data")

            try:
                sqla_source_data_list = self.session.query(SQLASourceData).all()

            except Exception as e:
                self.logger.error(f"Could not query the database for source data: {e}")
                errorDTO = ListSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Could not query the database for source data: {e}",
                    errorName="CouldNotListSourceData",
                    errorType="CouldNotListSourceData",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            core_source_data_list: List[SourceData] = [
                convert_sqla_source_data_to_core_source_data(sqla_sd) for sqla_sd in sqla_source_data_list
            ]

            return ListSourceDataDTO(
                status=True,
                data=core_source_data_list,
            )

        else:
            self.logger.info(f"Listing source data for knowledge source with ID {knowledge_source_id}")

            try:
                sqla_knowledge_source: SQLAKnowledgeSource | None = self.session.get(
                    SQLAKnowledgeSource, knowledge_source_id
                )

            except Exception as e:
                self.logger.error(
                    f"Could not query the database for knowledge source with ID {knowledge_source_id}: {e}"
                )
                errorDTO = ListSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Could not query the database for knowledge source with ID {knowledge_source_id}: {e}",
                    errorName="CouldNotListSourceData",
                    errorType="CouldNotListSourceData",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            if sqla_knowledge_source is None:
                self.logger.error(f"Knowledge source with ID {knowledge_source_id} not found in the database")
                errorDTO = ListSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Knowledge source with ID {knowledge_source_id} not found in the database",
                    errorName="KnowledgeSourceNotFound",
                    errorType="KnowledgeSourceNotFound",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            sqla_source_data_list = sqla_knowledge_source.source_data

            core_source_data_list = [
                convert_sqla_source_data_to_core_source_data(sqla_sd) for sqla_sd in sqla_source_data_list
            ]

            return ListSourceDataDTO(
                status=True,
                data=core_source_data_list,
            )

    def get_source_data_by_lfn(self, lfn: LFN) -> GetSourceDataByLFNDTO:
        """
        Gets source data by LFN.

        @param lfn: The logical file name of the source data to get.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: GetSourceDataByLFNDTO
        """

        try:
            if not lfn:
                self.logger.error("LFN cannot be None")
                return GetSourceDataByLFNDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage="LFN cannot be None",
                    errorName="LFNNotProvided",
                    errorType="LFNNotProvided",
                )

            sqla_lfn = lfn.to_json()

            try:
                queried_source_data = self.session.query(SQLASourceData).filter_by(lfn=sqla_lfn).first()

                if not queried_source_data:
                    self.logger.error(f"Source Data with LFN {lfn.to_json()} not found in the database")
                    return GetSourceDataByLFNDTO(
                        status=False,
                        errorCode=-1,
                        errorMessage=f"Source Data with LFN {lfn.to_json()} not found in the database",
                        errorName="SourceDataNotFound",
                        errorType="SourceDataNotFound",
                    )

                core_source_data = convert_sqla_source_data_to_core_source_data(queried_source_data)

                return GetSourceDataByLFNDTO(
                    status=True,
                    data=core_source_data,
                )

            except Exception as e:
                self.logger.error(f"Could not query the database for source data with LFN {lfn.to_json()}: {e}")
                errorDTO = GetSourceDataByLFNDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Could not query the database for source data with LFN {lfn.to_json()}: {e}",
                    errorName="CouldNotGetSourceDataByLFN",
                    errorType="CouldNotGetSourceDataByLFN",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

        except Exception as e:
            self.logger.error(f"Could not query the database for source data with LFN {lfn.to_json()}: {e}")
            errorDTO = GetSourceDataByLFNDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not query the database for source data with LFN {lfn.to_json()}: {e}",
                errorName="CouldNotGetSourceDataByLFN",
                errorType="CouldNotGetSourceDataByLFN",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
