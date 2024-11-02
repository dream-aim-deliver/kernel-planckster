from lib.core.dto.source_data_repository_dto import GetSourceDataByProtocolRelativePathDTO
from lib.core.entity.models import ProtocolEnum
from lib.core.ports.secondary.source_data_repository import SourceDataRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLASourceData
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
        self._session.expire_all()
        return self._session

    def get_source_data_by_composite_index(
        self, client_id: int, protocol: ProtocolEnum, relative_path: str
    ) -> GetSourceDataByProtocolRelativePathDTO:
        """
        Gets source data by its composite index.

        @param lfn: The logical file name of the source data to get.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: GetSourceDataByLFNDTO
        """
        if not client_id:
            self.logger.error("Client ID cannot be None")
            return GetSourceDataByProtocolRelativePathDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client ID cannot be None",
                errorName="ClientIDNotProvided",
                errorType="ClientIDNotProvided",
            )

        if not protocol:
            self.logger.error("Protocol cannot be None")
            return GetSourceDataByProtocolRelativePathDTO(
                status=False,
                errorCode=-1,
                errorMessage="Protocol cannot be None",
                errorName="ProtocolNotProvided",
                errorType="ProtocolNotProvided",
            )

        if not relative_path:
            self.logger.error("Relative path cannot be None")
            return GetSourceDataByProtocolRelativePathDTO(
                status=False,
                errorCode=-1,
                errorMessage="Relative path cannot be None",
                errorName="RelativePathNotProvided",
                errorType="RelativePathNotProvided",
            )

        try:
            queried_source_data_list = self.session.query(SQLASourceData).filter_by(
                client_id=client_id,
                protocol=protocol,
                relative_path=relative_path,
            )

            queried_source_data = queried_source_data_list.first()

            if queried_source_data is None:
                self.logger.error(
                    f"Source Data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}> not found in the database."
                )
                return GetSourceDataByProtocolRelativePathDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Source Data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}> not found in the database.",
                    errorName="SourceDataNotFound",
                    errorType="SourceDataNotFound",
                )

            if len(queried_source_data_list.all()) > 1:
                # We should never get this, as we're using a composite index, but just in case
                self.logger.error(
                    f"FATAL: More than one source data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}> found in the database."
                )
                return GetSourceDataByProtocolRelativePathDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"More than one source data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}> found in the database.",
                    errorName="MultipleSourceDataFound",
                    errorType="MultipleSourceDataFound",
                )

            core_source_data = convert_sqla_source_data_to_core_source_data(queried_source_data)

            return GetSourceDataByProtocolRelativePathDTO(
                status=True,
                data=core_source_data,
            )

        except Exception as e:
            self.logger.error(
                f"Could not get source data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}>: {e}"
            )
            errorDTO = GetSourceDataByProtocolRelativePathDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not get source data with composite index <client_id: {client_id}, protocol: {protocol}, relative_path: {relative_path}>: {e}",
                errorName="CouldNotGetSourceDataByCompositeIndex",
                errorType="CouldNotGetSourceDataByCompositeIndex",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
