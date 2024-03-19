from lib.core.dto.file_repository_dto import DownloadFileDTO
from lib.core.entity.models import LFN
from lib.core.ports.primary.download_file_primary_ports import DownloadFileInputPort
from lib.core.usecase_models.download_file_usecase_models import (
    DownloadFileError,
    DownloadFileRequest,
    DownloadFileResponse,
)


class DownloadFileUseCase(DownloadFileInputPort):
    def execute(self, request: DownloadFileRequest) -> DownloadFileResponse | DownloadFileError:
        lfn_json = request.lfn_json

        try:
            lfn = LFN.model_validate(lfn_json)

        except Exception as e:
            return DownloadFileError(
                errorCode="400",
                errorMessage=f"Invalid request parameters. Cannot parse '{lfn_json}' to an LFN. {e}",
                errorName="Invalid request parameters.",
                errorType="Invalid request parameters.",
            )

        # TODO: check that the LFN is actually in the DB

        dto: DownloadFileDTO = self.file_repository.download_file(lfn)

        if dto.status and dto.lfn and dto.credentials:
            return DownloadFileResponse(lfn=dto.lfn, credentials=dto.credentials)

        return DownloadFileError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
