from lib.core.dto.file_repository_dto import GetClientDataForUploadDTO
from lib.core.entity.models import ProtocolEnum, SourceData
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
        try:
            client_repository = self.client_repository
            file_repository = self.file_repository

            client_id = request.client_id

            # 1. Validate the relative path and protocol
            try:
                relative_path = SourceData.relative_path_validation(request.relative_path)
            except ValueError as e:
                return GetClientDataForUploadError(
                    errorCode=400,
                    errorMessage=f"Couldn't validate relative path: {e}",
                    errorName="Relative Path Validation Error",
                    errorType="RelativePathValidationError",
                )
            try:
                protocol = SourceData.protocol_validation(request.protocol)
            except ValueError as e:
                return GetClientDataForUploadError(
                    errorCode=400,
                    errorMessage=f"Couldn't validate protocol: {e}",
                    errorName="Protocol Validation Error",
                    errorType="ProtocolValidationError",
                )

            # 2. Check if the client exists in the database
            client_query_dto = client_repository.get_client(client_id)

            if not client_query_dto.status:
                return GetClientDataForUploadError(
                    errorCode=client_query_dto.errorCode,
                    errorMessage=client_query_dto.errorMessage,
                    errorName=client_query_dto.errorName,
                    errorType=client_query_dto.errorType,
                )

            if not client_query_dto.data:
                return GetClientDataForUploadError(
                    errorCode=404,
                    errorMessage=f"Client with id {client_id} not found.",
                    errorName="ClientNotFound",
                    errorType="ClientNotFound",
                )

            client = client_query_dto.data

            # 3. Get the credentials for upload
            dto: GetClientDataForUploadDTO = file_repository.get_client_data_for_upload(
                client=client,
                protocol=protocol,
                relative_path=relative_path,
            )

            if not dto.status:
                return GetClientDataForUploadError(
                    errorCode=dto.errorCode,
                    errorMessage=dto.errorMessage,
                    errorName=dto.errorName,
                    errorType=dto.errorType,
                )

            if not dto.credentials:
                return GetClientDataForUploadError(
                    errorCode=404,
                    errorMessage=f"Credentials not found for client with id {client_id}.",
                    errorName="CredentialsNotFound",
                    errorType="CredentialsNotFound",
                )

            return GetClientDataForUploadResponse(credentials=dto.credentials)

        except Exception as e:
            return GetClientDataForUploadError(
                errorCode=500,
                errorMessage=f"Internal Server Error: {e}",
                errorName="InternalServerError",
                errorType="InternalServerError",
            )
