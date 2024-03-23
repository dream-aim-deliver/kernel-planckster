import datetime
import os
from typing import List
from lib.core.dto.knowledge_source_repository_dto import NewSourceDataDTO
from lib.core.entity.models import LFN, ProtocolEnum, SourceData, SourceDataStatusEnum
from lib.core.ports.primary.new_source_data_primary_ports import NewSourceDataInputPort
from lib.core.usecase_models.new_source_data_usecase_models import (
    NewSourceDataError,
    NewSourceDataRequest,
    NewSourceDataResponse,
)


class NewSourceDataUseCase(NewSourceDataInputPort):
    def execute(self, request: NewSourceDataRequest) -> NewSourceDataResponse | NewSourceDataError:
        knowledge_source_repository = self.knowledge_source_repository
        file_repository = self.file_repository

        knowledge_source_id = request.knowledge_source_id
        req_lfn = request.lfn
        req_source_data_name = request.source_data_name

        # 1. First check if the lfn passed is valid
        try:
            core_lfn = LFN.from_json(req_lfn)
        except Exception as e:
            return NewSourceDataError(
                errorType="Invalid LFN",
                errorCode=400,
                errorMessage=f"The lfn '{req_lfn}' is invalid. Please provide a valid lfn. It should be a JSON object with the following fields: 'protocol', 'tracer_id', 'source', 'job_id', 'relative_path'. Example: {{'protocol': 's3', 'tracer_id': 'user_uploads', 'source': 'user', 'job_id': 1234567890, 'relative_path': 'path/to/file'}}. Ideally, it should be one provided by Kernel Planckster, for example when asking to upload a file. Error:\n{e}",
                errorName="InvalidLFN",
            )

        # 2. Then check if the lfn is present as a file in the file storage
        existence_dto = file_repository.lfn_exists(core_lfn)

        if not existence_dto.status:
            return NewSourceDataError(
                errorType=existence_dto.errorType,
                errorCode=existence_dto.errorCode,
                errorMessage=existence_dto.errorMessage,
                errorName=existence_dto.errorName,
            )

        if not existence_dto.existence:
            return NewSourceDataError(
                errorType="File Not Found",
                errorCode=404,
                errorMessage=f"The lfn '{core_lfn}' doesn't exist as a file in the file storage. Please upload your file before attempting to register its lfn.",
                errorName="FileNotFound",
            )

        # 3. Populate a core source data object
        status = SourceDataStatusEnum.AVAILABLE
        type = os.path.splitext(core_lfn.relative_path)[1].replace(".", "")

        core_source_data = SourceData(
            name=req_source_data_name,
            type=type,
            lfn=core_lfn,
            status=status,
            # The fields below will be ignored by the repository
            # and handled automatically by SQLA
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            deleted=False,
            deleted_at=None,
            id=-1,
        )

        # 4. Register the source data in the database
        dto: NewSourceDataDTO = knowledge_source_repository.new_source_data(
            knowledge_source_id=knowledge_source_id,
            source_data=core_source_data,
        )

        if dto.status:
            if dto.data:
                return NewSourceDataResponse(
                    source_data=dto.data,
                )

            else:
                return NewSourceDataError(
                    errorType="Registered Source Data Not Found",
                    errorCode=404,
                    errorMessage="The new source data seems to have been registered in the database, but it couldn't be retrieved. Please contact the system administrator.",
                    errorName="RegisteredSourceDataNotFound",
                )

        return NewSourceDataError(
            errorType=dto.errorType,
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
        )
