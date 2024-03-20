from typing import Dict, List
from lib.core.dto.knowledge_source_repository_dto import NewSourceDataDTO
from lib.core.entity.models import SourceData
from lib.core.ports.secondary.knowledge_source_repository import KnowledgeSourceRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource, SQLASourceData
from lib.infrastructure.repository.sqla.utils import (
    convert_core_source_data_to_sqla_source_data,
    convert_sqla_source_data_to_core_source_data,
)


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

    def new_source_data(self, knowledge_source_id: int, source_data: SourceData) -> NewSourceDataDTO:
        """
        Creates a new source data.

        @param knowledge_source_id: The ID of the knowledge source to create the source data for.
        @type knowledge_source_id: int
        @param source_data: The source data to register.
        @type source_data: SourceData
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

        if source_data is None:
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

        sqla_source_data = convert_core_source_data_to_sqla_source_data(source_data)

        try:
            # 1. First check if the lfn of the source data passed is already in the db
            sqla_lfn = sqla_source_data.lfn

            queried_source_data = self.session.query(SQLASourceData).filter_by(lfn=sqla_lfn).first()

            if queried_source_data:
                if isinstance(queried_source_data, SQLASourceData):
                    if sqla_source_data.lfn == queried_source_data.lfn:
                        self.logger.error(
                            f"Source Data with lfn\n'{sqla_lfn}'\nalready exists in the database. LFNs must be unique. Aborting."
                        )
                        errorDTO = NewSourceDataDTO(
                            status=False,
                            errorCode=-1,
                            errorMessage=f"Source Data with lfn\n'{sqla_lfn}'\nalready exists in the database. LFNs must be unique. Aborting.",
                            errorName="Source Data Already Registered",
                            errorType="SourceDataAlreadyRegistered",
                        )
                        return errorDTO

        except Exception as e:
            self.logger.error(f"Couldn't assert uniqueness of lfn in the database. Error:\n{e}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Couldn't assert uniqueness of lfn in the database. Error:\n{e}",
                errorName="Couldn't Assert LFN uniqueness",
                errorType="Couldn'tAssertLFNUniqueness",
            )
            return errorDTO

        try:
            # 2. If LFN is unique, then SD is unique, so we can commit it
            sqla_knowledge_source: SQLAKnowledgeSource | None = self.session.get(
                SQLAKnowledgeSource, knowledge_source_id
            )

            if sqla_knowledge_source is None:
                self.logger.error(
                    f"Knowledge source with ID {knowledge_source_id} not found in the database, for source data '{source_data}'."
                )
                errorDTO = NewSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Knowledge source with ID {knowledge_source_id} not found in the database, for source data '{source_data}.",
                    errorName="KnowledgeSourceNotFound",
                    errorType="KnowledgeSourceNotFound",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            sqla_knowledge_source.source_data.append(sqla_source_data)
            self.session.commit()

            sqla_sd_queried: SQLASourceData | None = self.session.get(SQLASourceData, sqla_source_data.id)

            if not sqla_sd_queried:
                self.logger.error(
                    f"Error while creating source data '{source_data}': not present in the Database after commiting changes."
                )
                errorDTO = NewSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Error while creating source data '{source_data}': not present in the Database after commiting changes.",
                    errorName="Source Data creation error",
                    errorType="SourceDataCreationError",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            try:
                new_source_data = convert_sqla_source_data_to_core_source_data(sqla_sd_queried)

            except Exception as e:
                self.logger.error(
                    f"Error while creating source data '{source_data}': {e}. The source data was created in the database, but could not be retrieved."
                )
                errorDTO = NewSourceDataDTO(
                    status=False,
                    errorCode=-1,
                    errorMessage=f"Error while creating source data '{source_data}': {e}. The source data was created in the database, but could not be retrieved.",
                    errorName="Source Data creation error",
                    errorType="SourceDataCreationError",
                )
                self.logger.error(f"{errorDTO}")
                return errorDTO

            return NewSourceDataDTO(status=True, data=new_source_data)

        except Exception as e:
            self.logger.error(f"Error while creating source data '{source_data}': {e}")
            errorDTO = NewSourceDataDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error while creating source data '{source_data}': {e}",
                errorName="Source Data creation error",
                errorType="SourceDataCreationError",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

            # TODO OLD: In the previous version (allowing for a list for source data, instead of just one): fix this: if the second element of the input list is a duplicate of the first one, the first one will be added (correct), the second one catched in the duplicates list (correct), but from the third one onwards everything will fail because SQLA had an error in the session
