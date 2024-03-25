from lib.core.dto.client_repository_dto import GetClientDTO, ListSourceDataDTO, NewResearchContextDTO
from lib.core.ports.primary.new_research_context_primary_ports import NewResearchContextInputPort
from lib.core.usecase_models.new_research_context_usecase_models import (
    NewResearchContextError,
    NewResearchContextRequest,
    NewResearchContextResponse,
)


class NewResearchContextUseCase(NewResearchContextInputPort):
    def execute(self, request: NewResearchContextRequest) -> NewResearchContextResponse | NewResearchContextError:
        try:
            client_repository = self.client_repository

            research_context_title = request.research_context_title
            research_context_description = request.research_context_description
            client_sub = request.client_sub
            llm_name = request.llm_name
            source_data_ids_req = request.source_data_ids

            # 1. Get the client, by SUB, to then check if he has access to the source data
            client_by_sub_dto: GetClientDTO = client_repository.get_client_by_sub(client_sub=client_sub)

            if not client_by_sub_dto.status:
                return NewResearchContextError(
                    errorCode=client_by_sub_dto.errorCode,
                    errorMessage=client_by_sub_dto.errorMessage,
                    errorName=client_by_sub_dto.errorName,
                    errorType=client_by_sub_dto.errorType,
                )

            retrieved_client = client_by_sub_dto.data

            if not retrieved_client:
                return NewResearchContextError(
                    errorCode=404,
                    errorMessage=f"Client with SUB {client_sub} not found.",
                    errorName="ClientNotFound",
                    errorType="ClientNotFound",
                )

            if not retrieved_client.sub == client_sub:
                return NewResearchContextError(
                    errorCode=403,
                    errorMessage=f"Client SUB mismatch! Requested: {client_sub}, Retrieved: {retrieved_client.sub}",
                    errorName="Client SUB Mismatch",
                    errorType="ClientSubMismatch",
                )

            # 2. Check if the client has access to the source data
            client_source_data_list_dto: ListSourceDataDTO = client_repository.list_source_data(
                client_id=retrieved_client.id
            )

            if not client_source_data_list_dto.status:
                return NewResearchContextError(
                    errorCode=client_source_data_list_dto.errorCode,
                    errorMessage=client_source_data_list_dto.errorMessage,
                    errorName=client_source_data_list_dto.errorName,
                    errorType=client_source_data_list_dto.errorType,
                )

            client_source_data_list = client_source_data_list_dto.data

            if not isinstance(client_source_data_list, list):
                return NewResearchContextError(
                    errorCode=404,
                    errorMessage=f"Source Data couldn't be retrieved for client with SUB {retrieved_client.sub}.",
                    errorName="SourceDataNotRetrieved",
                    errorType="SourceDataNotRetrieved",
                )

            authorized_source_data_ids = [sd.id for sd in client_source_data_list]

            unauthorized_source_data_ids = [
                sd_id for sd_id in source_data_ids_req if sd_id not in authorized_source_data_ids
            ]

            if len(unauthorized_source_data_ids) > 0:
                return NewResearchContextError(
                    errorCode=403,
                    errorMessage=f"Client with SUB {retrieved_client.sub} is not authorized to access the following source data ids: {unauthorized_source_data_ids}",
                    errorName="UnauthorizedSourceData",
                    errorType="UnauthorizedSourceData",
                )

            # 3. Create the new research context
            dto: NewResearchContextDTO = client_repository.new_research_context(
                research_context_title=research_context_title,
                research_context_description=research_context_description,
                client_sub=client_sub,
                llm_name=llm_name,
                source_data_ids=source_data_ids_req,
            )

            if dto.status:
                return NewResearchContextResponse(research_context=dto.research_context, llm=dto.llm)

            return NewResearchContextError(
                errorCode=dto.errorCode,
                errorMessage=dto.errorMessage,
                errorName=dto.errorName,
                errorType=dto.errorType,
            )

        except Exception as e:
            return NewResearchContextError(
                errorCode="500",
                errorMessage=f"Internal Server Error: {e}",
                errorName="Internal Server Error",
                errorType="InternalServerError",
            )
