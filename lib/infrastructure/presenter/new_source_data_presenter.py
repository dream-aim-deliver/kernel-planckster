from lib.core.ports.primary.new_source_data_primary_ports import NewSourceDataOutputPort
from lib.core.usecase_models.new_source_data_usecase_models import NewSourceDataError, NewSourceDataResponse
from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel


class NewSourceDataPresenter(NewSourceDataOutputPort):
    def convert_error_response_to_view_model(self, error: NewSourceDataError) -> NewSourceDataViewModel:
        return NewSourceDataViewModel(
            status=False,
            code=error.errorCode,
            errorCode=error.errorCode,
            errorMessage=error.errorMessage,
            errorName=error.errorName,
            errorType=error.errorType,
            source_data=None,
        )

    def convert_response_to_view_model(self, response: NewSourceDataResponse) -> NewSourceDataViewModel:
        return NewSourceDataViewModel(
            status=True,
            code=200,
            source_data=response.source_data,
        )
