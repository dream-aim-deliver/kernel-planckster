from lib.core.dto.client_repository_dto import GetClientDTO, ListSourceDataDTO, NewResearchContextDTO
from lib.core.dto.research_context_repository_dto import ListSourceDataDTO as ResearchContextListSourceDataDTO
from lib.core.ports.primary.extend_research_context_primary_ports import ExtendResearchContextInputPort
from lib.core.usecase_models.extend_research_context_usecase_models import (
    ExtendResearchContextError,
    ExtendResearchContextRequest,
    ExtendResearchContextResponse,
)


class ExtendResearchContextUseCase(ExtendResearchContextInputPort):
    def execute(
        self, request: ExtendResearchContextRequest
    ) -> ExtendResearchContextResponse | ExtendResearchContextError:
        try:
            client_repository = self.client_repository
            research_context_repository = self.research_context_repository

            new_research_context_title = request.new_research_context_title
            new_research_context_description = request.new_research_context_description
            client_sub = request.client_sub
            llm_name = request.llm_name
            new_source_data_ids_req = request.new_source_data_ids
            existing_research_context_id = request.existing_research_context_id

            # 1. Get the client, by SUB, to then check if they have access to the source data
            client_by_sub_dto: GetClientDTO = client_repository.get_client_by_sub(client_sub=client_sub)

            if not client_by_sub_dto.status:
                return ExtendResearchContextError(
                    errorCode=client_by_sub_dto.errorCode,
                    errorMessage=client_by_sub_dto.errorMessage,
                    errorName=client_by_sub_dto.errorName,
                    errorType=client_by_sub_dto.errorType,
                )

            retrieved_client = client_by_sub_dto.data

            if not retrieved_client:
                return ExtendResearchContextError(
                    errorCode=404,
                    errorMessage=f"Client with SUB {client_sub} not found.",
                    errorName="ClientNotFound",
                    errorType="ClientNotFound",
                )

            if not retrieved_client.sub == client_sub:
                return ExtendResearchContextError(
                    errorCode=403,
                    errorMessage=f"Client SUB mismatch! Requested: {client_sub}, Retrieved: {retrieved_client.sub}",
                    errorName="Client SUB Mismatch",
                    errorType="ClientSubMismatch",
                )

            # 2. Check if the client has access to the source data
            new_client_source_data_list_dto: ListSourceDataDTO = client_repository.list_source_data(
                client_id=retrieved_client.id
            )

            if not new_client_source_data_list_dto.status:
                return ExtendResearchContextError(
                    errorCode=new_client_source_data_list_dto.errorCode,
                    errorMessage=new_client_source_data_list_dto.errorMessage,
                    errorName=new_client_source_data_list_dto.errorName,
                    errorType=new_client_source_data_list_dto.errorType,
                )

            new_client_source_data_list = new_client_source_data_list_dto.data

            if len(new_client_source_data_list) == 0:
                return ExtendResearchContextError(
                    errorCode=404,
                    errorMessage=f"New Source Data couldn't be retrieved for client with SUB {retrieved_client.sub}.",
                    errorName="NewSourceDataNotRetrieved",
                    errorType="NewSourceDataNotRetrieved",
                )

            authorized_new_source_data_ids = [sd.id for sd in new_client_source_data_list]

            unauthorized_new_source_data_ids = [
                sd_id for sd_id in new_source_data_ids_req if sd_id not in authorized_new_source_data_ids
            ]

            if len(unauthorized_new_source_data_ids) > 0:
                return ExtendResearchContextError(
                    errorCode=403,
                    errorMessage=f"Client with SUB {retrieved_client.sub} is not authorized to access the following source data ids: {unauthorized_new_source_data_ids}",
                    errorName="UnauthorizedSourceData",
                    errorType="UnauthorizedSourceData",
                )

            # 3. Ensure that there are actually new data sources, and deduplicate as needed

            existing_client_source_data_list_dto: ResearchContextListSourceDataDTO = (
                research_context_repository.list_source_data(research_context_id=existing_research_context_id)
            )

            existing_client_source_data_list = existing_client_source_data_list_dto.data

            if not isinstance(existing_client_source_data_list, list):
                return ExtendResearchContextError(
                    errorCode=404,
                    errorMessage=f"Source Data for existing research context couldn't be retrieved for client with SUB {retrieved_client.sub}.",
                    errorName="Existing Source Data Not Retrieved",
                    errorType="ExistingSourceDataNotRetrieved",
                )

            existing_client_source_data_ids = [sd.id for sd in existing_client_source_data_list]

            extending_client_source_data_ids = [
                sd_id for sd_id in existing_client_source_data_ids if sd_id not in authorized_new_source_data_ids
            ]

            if len(extending_client_source_data_ids) == 0:
                return ExtendResearchContextError(
                    errorCode=400,
                    errorMessage="No new source data provided! A new research context requires at least one data source not already found in the referenced existing research context.",
                    errorName="No New Source Data",
                    errorType="NoNewSourceData",
                )

            final_source_data_list = authorized_new_source_data_ids + extending_client_source_data_ids

            # 4. Create the new research context including all (deduplicated) data sources, new and old
            dto: NewResearchContextDTO = client_repository.new_research_context(
                research_context_title=new_research_context_title,
                research_context_description=new_research_context_description,
                client_sub=client_sub,
                llm_name=llm_name,
                source_data_ids=final_source_data_list,
            )

            if dto.status:
                return ExtendResearchContextResponse(research_context=dto.research_context, llm=dto.llm)

            return ExtendResearchContextError(
                errorCode=dto.errorCode,
                errorMessage=dto.errorMessage,
                errorName=dto.errorName,
                errorType=dto.errorType,
            )

        except Exception as e:
            return ExtendResearchContextError(
                errorCode="500",
                errorMessage=f"Internal Server Error: {e}",
                errorName="Internal Server Error",
                errorType="InternalServerError",
            )
