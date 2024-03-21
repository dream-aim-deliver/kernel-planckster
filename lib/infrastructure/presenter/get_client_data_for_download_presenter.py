from lib.core.ports.primary.get_client_data_for_download_primary_ports import GetClientDataForDownloadOutputPort
from lib.core.usecase_models.get_client_data_for_download_usecase_models import (
    GetClientDataForDownloadError,
    GetClientDataForDownloadResponse,
)
from lib.core.view_model.get_client_data_for_download_view_model import GetClientDataForDownloadViewModel


class GetClientDataForDownloadPresenter(GetClientDataForDownloadOutputPort):
    def convert_error_response_to_view_model(
        self, response: GetClientDataForDownloadError
    ) -> GetClientDataForDownloadViewModel:
        return GetClientDataForDownloadViewModel(
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
        self, response: GetClientDataForDownloadResponse
    ) -> GetClientDataForDownloadViewModel:
        return GetClientDataForDownloadViewModel(
            status=True,
            code=200,
            lfn=response.lfn,
            signed_url=response.credentials,
        )
