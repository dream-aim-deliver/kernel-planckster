from typing import List

from lib.core.entity.models import LFN, KnowledgeSourceEnum
from lib.core.ports.primary.list_source_data_primary_ports import ListSourceDataOutputPort
from lib.core.usecase_models.list_source_data_usecase_models import ListSourceDataError, ListSourceDataResponse
from lib.core.view_model.list_source_data_view_model import ListSourceDataViewModel


class ListSourceDataPresenter(ListSourceDataOutputPort):
    def convert_error_response_to_view_model(self, response: ListSourceDataError) -> ListSourceDataViewModel:
        return ListSourceDataViewModel(
            status=False,
            source_data_list=[],
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
        )

    def convert_response_to_view_model(self, response: ListSourceDataResponse) -> ListSourceDataViewModel:
        return ListSourceDataViewModel(
            status=True,
            code=200,
            source_data_list=response.source_data_list,
        )
