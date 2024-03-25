from lib.core.dto.client_repository_dto import NewSourceDataDTO
from lib.core.entity.models import ProtocolEnum, SourceData
from lib.core.ports.primary.new_source_data_primary_ports import NewSourceDataInputPort
from lib.core.usecase_models.new_source_data_usecase_models import (
    NewSourceDataError,
    NewSourceDataRequest,
    NewSourceDataResponse,
)


class NewSourceDataUseCase(NewSourceDataInputPort):
    def execute(self, request: NewSourceDataRequest) -> NewSourceDataResponse | NewSourceDataError:
        try:
            client_repository = self.client_repository
            file_repository = self.file_repository

            client_id = request.client_id

            # 1. First validate fields
            try:
                relative_path = SourceData.relative_path_validation(request.relative_path)
            except Exception as e:
                return NewSourceDataError(
                    errorCode=400,
                    errorMessage=f"Coudn't validate the relative path: {e}",
                    errorName="Relative Path Validation Error",
                    errorType="RelativePathValidationError",
                )

            try:
                protocol = SourceData.protocol_validation(request.protocol)
            except Exception as e:
                return NewSourceDataError(
                    errorCode=400,
                    errorMessage=f"Coudn't validate the protocol: {e}",
                    errorName="Protocol Validation Error",
                    errorType="ProtocolValidationError",
                )

            try:
                source_data_name = SourceData.name_validation(request.source_data_name)
            except Exception as e:
                return NewSourceDataError(
                    errorCode=400,
                    errorMessage=f"Coudn't validate the source data name: {e}",
                    errorName="Source Data Name Validation Error",
                    errorType="SourceDataNameValidationError",
                )

            # 2. Then get the client from the database
            client_query_dto = client_repository.get_client(client_id)

            if not client_query_dto.status:
                return NewSourceDataError(
                    errorType=client_query_dto.errorType,
                    errorCode=client_query_dto.errorCode,
                    errorMessage=client_query_dto.errorMessage,
                    errorName=client_query_dto.errorName,
                )

            if not client_query_dto.data:
                return NewSourceDataError(
                    errorType="Client Not Found",
                    errorCode=404,
                    errorMessage=f"Client with id {client_id} not found.",
                    errorName="ClientNotFound",
                )

            client = client_query_dto.data

            # 3. Then check if the is present as a file in the file storage
            # NOTE: handle different protocols here, whenever the need arises
            if protocol == ProtocolEnum.S3:
                existence_dto = file_repository.composite_index_of_source_data_exists_as_file(
                    client=client,
                    protocol=protocol,
                    relative_path=relative_path,
                )

                if not existence_dto.status:
                    return NewSourceDataError(
                        errorType=existence_dto.errorType,
                        errorCode=existence_dto.errorCode,
                        errorMessage=existence_dto.errorMessage,
                        errorName=existence_dto.errorName,
                    )

                if existence_dto.existence == False:
                    return NewSourceDataError(
                        errorCode=404,
                        errorMessage=f"Source data with protocol '{protocol}', and relative path '{relative_path}' doesn't exist in the file storage for client '{client.sub}'.",
                        errorName="Source Data Not Found In File Storage",
                        errorType="SourceDataNotFoundInFileStorage",
                    )
            else:
                return NewSourceDataError(
                    errorCode=501,
                    errorMessage=f"Protocol '{protocol}' is not supported.",
                    errorName="ProtocolNotSupported",
                    errorType="ProtocolNotSupported",
                )

            # 4. Register the source data in the database
            dto: NewSourceDataDTO = client_repository.new_source_data(
                client_id=client_id,
                source_data_name=source_data_name,
                protocol=protocol,
                relative_path=relative_path,
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

        except Exception as e:
            return NewSourceDataError(
                errorCode=500,
                errorMessage=f"Internal Server Error: {e}",
                errorName="Internal Server Error",
                errorType="InternalServerError",
            )
