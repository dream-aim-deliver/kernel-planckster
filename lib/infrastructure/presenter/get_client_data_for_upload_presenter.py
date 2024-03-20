from lib.core.ports.primary.get_client_data_for_upload_primary_ports import GetClientDataForUploadOutputPort
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadError,
    GetClientDataForUploadResponse,
)
from lib.core.view_model.get_client_data_for_upload_view_model import GetClientDataForUploadViewModel


class GetClientDataForUploadPresenter(GetClientDataForUploadOutputPort):
    def convert_error_response_to_view_model(
        self, response: GetClientDataForUploadError
    ) -> GetClientDataForUploadViewModel:
        return GetClientDataForUploadViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            lfn=None,
            signed_url="",
        )

    def convert_response_to_view_model(
        self, response: GetClientDataForUploadResponse
    ) -> GetClientDataForUploadViewModel:
        return GetClientDataForUploadViewModel(
            status=True,
            code=200,
            lfn=response.lfn,
            signed_url=response.credentials,
        )
