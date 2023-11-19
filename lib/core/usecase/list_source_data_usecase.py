from lib.core.dto.source_data_repository_dto import ListSourceDataDTO
from lib.core.entity.models import KnowledgeSourceEnum, ProtocolEnum
from lib.core.ports.primary.list_source_data_primary_ports import ListSourceDataInputPort
from lib.core.usecase_models.list_source_data_usecase_models import (
    ListSourceDataError,
    ListSourceDataRequest,
    ListSourceDataResponse,
)


class ListSourceDataUseCase(ListSourceDataInputPort):
    def execute(self, request: ListSourceDataRequest) -> ListSourceDataResponse | ListSourceDataError:
        knowledge_source_id = request.knowledge_source_id

        dto: ListSourceDataDTO = self.source_data_repository.list_source_data(knowledge_source_id=knowledge_source_id)

        if dto.status:
            return ListSourceDataResponse(lfn_list=dto.data)

        return ListSourceDataError(
            knowledge_source_id=knowledge_source_id,
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
