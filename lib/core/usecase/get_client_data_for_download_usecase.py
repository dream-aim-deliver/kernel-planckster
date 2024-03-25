from lib.core.dto.file_repository_dto import GetClientDataForDownloadDTO
from lib.core.entity.models import ProtocolEnum, SourceData
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
        try:
            client_repository = self.client_repository
            source_data_repository = self.source_data_repository
            file_repository = self.file_repository

            client_id = request.client_id

            # 1. First validate protocol and relative path
            try:
                relative_path = SourceData.relative_path_validation(request.relative_path)
            except Exception as e:
                return GetClientDataForDownloadError(
                    errorCode=400,
                    errorMessage=f"Couldn't validate the relative path: {e}",
                    errorName="Relative Path Validation Error",
                    errorType="RelativePathValidationError",
                )

            try:
                protocol = SourceData.protocol_validation(request.protocol)
            except Exception as e:
                return GetClientDataForDownloadError(
                    errorCode=400,
                    errorMessage=f"Couldn't validate the protocol: {e}",
                    errorName="Protocol Validation Error",
                    errorType="ProtocolValidationError",
                )

            # 2. Check that the client exists in the DB
            client_query_dto = client_repository.get_client(client_id)

            if not client_query_dto.status:
                return GetClientDataForDownloadError(
                    errorCode=client_query_dto.errorCode,
                    errorMessage=client_query_dto.errorMessage,
                    errorName=client_query_dto.errorName,
                    errorType=client_query_dto.errorType,
                )

            client = client_query_dto.data

            if not client:
                return GetClientDataForDownloadError(
                    errorCode=404,
                    errorMessage=f"Client with ID {client_id} not found.",
                    errorName="ClientNotFound",
                    errorType="ClientNotFound",
                )

            # 3. Check that the composite index exists in the DB as a SourceData
            client_source_data_query_dto = source_data_repository.get_source_data_by_composite_index(
                client_id=client.id,
                protocol=protocol,
                relative_path=relative_path,
            )

            if not client_source_data_query_dto.status:
                return GetClientDataForDownloadError(
                    errorCode=client_source_data_query_dto.errorCode,
                    errorMessage=client_source_data_query_dto.errorMessage,
                    errorName=client_source_data_query_dto.errorName,
                    errorType=client_source_data_query_dto.errorType,
                )

            source_data = client_source_data_query_dto.data

            if not source_data:
                return GetClientDataForDownloadError(
                    errorCode=404,
                    errorMessage=f"No source data found for client with id {client_id}, with protocol '{protocol}' and relative path '{relative_path}'. No download possible.",
                    errorName="SourceDataNotFound",
                    errorType="SourceDataNotFound",
                )

            # 3. Get the data for download
            # NOTE: handle protocols here
            if protocol == ProtocolEnum.S3:
                dto: GetClientDataForDownloadDTO = file_repository.get_client_data_for_download(
                    client=client,
                    source_data=source_data,
                )

                if dto.status:
                    if dto.credentials:
                        return GetClientDataForDownloadResponse(credentials=dto.credentials)
                    else:
                        return GetClientDataForDownloadError(
                            errorCode=500,
                            errorMessage=f"Repository reports success but no credentials were found for sourrce data with protocol '{protocol}' and relative path '{relative_path}' for client {client.sub}. No download possible.",
                            errorName="Credentials Not Found",
                            errorType="CredentialsNotFound",
                        )

            else:
                return GetClientDataForDownloadError(
                    errorCode=400,
                    errorMessage=f"Protocol '{protocol}' not supported for download.",
                    errorName="Protocol Not Supported",
                    errorType="ProtocolNotSupported",
                )

            return GetClientDataForDownloadError(
                errorCode=dto.errorCode,
                errorMessage=dto.errorMessage,
                errorName=dto.errorName,
                errorType=dto.errorType,
            )

        except Exception as e:
            return GetClientDataForDownloadError(
                errorType="Internal Server Error",
                errorCode=500,
                errorMessage=f"An unexpected error occurred while trying to get the client data for download. Error:\n{e}",
                errorName="UnexpectedError",
            )
