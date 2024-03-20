from lib.core.dto.file_repository_dto import FilePathToLFNDTO, GetClientDataForUploadDTO
from lib.core.entity.models import LFN
from lib.core.ports.primary.get_client_data_for_upload_primary_ports import GetClientDataForUploadInputPort
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadError,
    GetClientDataForUploadRequest,
    GetClientDataForUploadResponse,
)


class GetClientDataForUploadUsecase(GetClientDataForUploadInputPort):
    def execute(
        self, request: GetClientDataForUploadRequest
    ) -> GetClientDataForUploadResponse | GetClientDataForUploadError:
        lfn_str = request.lfn_str

        try:
            core_lfn = LFN.from_json(lfn_str)
        except Exception as e:
            return GetClientDataForUploadError(
                errorType="Invalid LFN",
                errorCode=400,
                errorMessage=f"The lfn '{lfn_str}' is invalid. Please provide a valid lfn. It should be a JSON object with the following fields: 'protocol', 'tracer_id', 'source', 'job_id', 'relative_path'. Example: {{'protocol': 's3', 'tracer_id': 'user_uploads', 'source': 'user', 'job_id': 1234567890, 'relative_path': 'path/to/file'}}. Ideally, it should be one provided by Kernel Planckster, for example when asking to upload a file. Error:\n{e}",
                errorName="InvalidLFN",
            )

        dto: GetClientDataForUploadDTO = self.file_repository.get_client_data_for_upload(lfn=core_lfn)

        if dto.status:
            return GetClientDataForUploadResponse(lfn=dto.lfn, credentials=dto.credentials)

        return GetClientDataForUploadError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
