from lib.core.dto.file_repository_dto import GetClientDataForDownloadDTO
from lib.core.entity.models import LFN
from lib.core.ports.primary.get_client_data_for_download_primary_ports import GetClientDataForDownloadInputPort
from lib.core.usecase_models.get_client_data_for_download_usecase_models import (
    GetClientDataForDownloadError,
    GetClientDataForDownloadRequest,
    GetClientDataForDownloadResponse,
)


class GetClientDataForDownloadUseCase(GetClientDataForDownloadInputPort):
    def execute(
        self, request: GetClientDataForDownloadRequest
    ) -> GetClientDataForDownloadResponse | GetClientDataForDownloadError:
        file_repository = self.file_repository
        source_data_repository = self.source_data_repository

        lfn_json = request.lfn_str

        try:
            lfn = LFN.from_json(lfn_json)

        except Exception as e:
            return GetClientDataForDownloadError(
                errorCode="400",
                errorMessage=f"Invalid request parameters. Cannot parse '{lfn_json}' to an LFN. {e}",
                errorName="Invalid request parameters.",
                errorType="Invalid request parameters.",
            )

        # 1. check that the LFN is actually in the DB
        query_dto = source_data_repository.get_source_data_by_lfn(lfn)

        if not query_dto.status:
            return GetClientDataForDownloadError(
                errorCode=query_dto.errorCode,
                errorMessage=query_dto.errorMessage,
                errorName=query_dto.errorName,
                errorType=query_dto.errorType,
            )

        # 2. Get the data for download
        # TODO: this should handle all protocols and use to the correct client for each one, not just one protocol
        # IDEA: the usecase can extract the protocol and decide which repository to use ('s3_repository', 'event_repository', etc.)
        dto: GetClientDataForDownloadDTO = file_repository.get_client_data_for_download(lfn)

        if dto.status and dto.lfn and dto.credentials:
            return GetClientDataForDownloadResponse(lfn=dto.lfn, credentials=dto.credentials)

        return GetClientDataForDownloadError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
