from lib.core.dto.client_repository_dto import ListSourceDataDTO
from lib.core.ports.primary.list_source_data_primary_ports import ListSourceDataInputPort
from lib.core.usecase_models.list_source_data_usecase_models import (
    ListSourceDataError,
    ListSourceDataRequest,
    ListSourceDataResponse,
)


class ListSourceDataUseCase(ListSourceDataInputPort):
    def execute(self, request: ListSourceDataRequest) -> ListSourceDataResponse | ListSourceDataError:
        try:
            client_repository = self.client_repository
            client_id = request.client_id

            dto: ListSourceDataDTO = client_repository.list_source_data(client_id=client_id)

            if dto.status:
                return ListSourceDataResponse(source_data_list=dto.data)

            return ListSourceDataError(
                errorCode=dto.errorCode,
                errorMessage=dto.errorMessage,
                errorName=dto.errorName,
                errorType=dto.errorType,
                client_id=client_id,
            )

        except Exception as e:
            return ListSourceDataError(
                errorCode="500",
                errorMessage=f"Internal Server Error: {e}",
                errorName="Internal Server Error",
                errorType="Internal Server Error",
                client_id=client_id,
            )
