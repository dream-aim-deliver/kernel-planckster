from collections.abc import Generator
from typing import Callable
from contextlib import _GeneratorContextManager
from lib.core.dto.source_data_repository_dto import GetSourceDataByProtocolRelativePathDTO
from lib.core.entity.models import ProtocolEnum
from lib.core.ports.secondary.source_data_repository import SourceDataRepositoryOutputPort

from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLASourceData
from lib.infrastructure.repository.sqla.utils import (
    convert_sqla_source_data_to_core_source_data,
    session_context,
    sexy_decorator_pipipi,
)


class SQLASourceDataRepository(SourceDataRepositoryOutputPort[Session]):
    """
    A SQLAlchemy implementation of the source data repository.
    """

    def __init__(
        self,
        session_generator_factory: Generator[Callable[[], _GeneratorContextManager[Session]], None, None],
    ) -> None:
        super().__init__()
        self._session_generator = session_generator_factory()

    @property
    def session_generator(self) -> Generator[Callable[[], _GeneratorContextManager[Session]], None, None]:
        return self._session_generator

    @sexy_decorator_pipipi()
    def get_source_data_by_composite_index(
        self,
        session: Session,
        client_id: int,
        protocol: ProtocolEnum,
        relative_path: str,
    ) -> GetSourceDataByProtocolRelativePathDTO:
        """
        Gets source data by its composite index.

        @param session: An open session provided by the context manager.
        @type session: Optional[Session]
        @param client_id: The ID of the client to get.
        @type client_id: int
        @param protocol: The protocol of the source data.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the source data.
        @type relative_path: str
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
            queried_source_data_list = session.query(SQLASourceData).filter_by(
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
