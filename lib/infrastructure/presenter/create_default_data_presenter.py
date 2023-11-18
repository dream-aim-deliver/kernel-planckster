from lib.core.ports.primary.create_default_data_primary_ports import CreateDefaultDataOutputPort
from lib.core.usecase_models.create_default_data_usecase_models import CreateDefaultDataError, CreateDefaultDataResponse
from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel


class CreateDefaultDataPresenter(CreateDefaultDataOutputPort):
    def convert_error_response_to_view_model(self, response: CreateDefaultDataError) -> CreateDefaultDataViewModel:
        return CreateDefaultDataViewModel(
            status=False,
            knowledge_sources_dict={"null": -1},
            user_id=-1,
            llm_id=-1,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(self, response: CreateDefaultDataResponse) -> CreateDefaultDataViewModel:
        return CreateDefaultDataViewModel(
            status=True,
            knowledge_sources_dict=response.knowledge_sources_dict,
            user_id=response.user_id,
            llm_id=response.llm_id,
            code=200,
        )
