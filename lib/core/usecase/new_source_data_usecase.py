import datetime
from typing import List
from lib.core.dto.knowledge_source_repository_dto import NewSourceDataDTO
from lib.core.entity.models import ProtocolEnum, SourceData, SourceDataStatusEnum
from lib.core.ports.primary.new_source_data_primary_ports import NewSourceDataInputPort
from lib.core.usecase_models.new_source_data_usecase_models import (
    NewSourceDataError,
    NewSourceDataRequest,
    NewSourceDataResponse,
)


class NewSourceDataUseCase(NewSourceDataInputPort):
    def _get_protocol_by_value(self, protocol_value: str) -> ProtocolEnum:
        for protocol in ProtocolEnum:
            if protocol.value.lower() == protocol_value.lower():
                return protocol
        raise ValueError(f"Protocol with value {protocol_value} not found.")

    def execute(self, request: NewSourceDataRequest) -> NewSourceDataResponse | NewSourceDataError:
        knowledge_source_id = request.knowledge_source_id
        source_data_lfn_list = request.source_data_lfn_list

        # 1. Populate the source data list with the input LFNs list
        source_data_list: List[SourceData] = []

        for lfn in source_data_lfn_list:
            protocol_str = lfn.split("://")[0]
            protocol = self._get_protocol_by_value(protocol_str)

            source_datum = SourceData(
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                deleted=False,
                deleted_at=None,
                id=-1,
                name=lfn.rsplit("/", 1)[-1],
                type="default",
                lfn=lfn,
                protocol=protocol,
                status=SourceDataStatusEnum.AVAILABLE,
            )
            source_data_list.append(source_datum)

        # 2. Call the repository with the populated source data list
        dto: NewSourceDataDTO = self.knowledge_source_repository.new_source_data(
            knowledge_source_id=knowledge_source_id, source_data_list=source_data_list
        )

        if dto.status:
            return NewSourceDataResponse()

        return NewSourceDataError(
            errorType=dto.errorType,
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
        )
