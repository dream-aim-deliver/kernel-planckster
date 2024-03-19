from lib.core.ports.primary.download_file_primary_ports import DownloadFileOutputPort
from lib.core.usecase_models.download_file_usecase_models import DownloadFileError, DownloadFileResponse
from lib.core.view_model.download_file_view_model import DownloadFileViewModel


class DownloadFilePresenter(DownloadFileOutputPort):
    def convert_error_response_to_view_model(self, response: DownloadFileError) -> DownloadFileViewModel:
        return DownloadFileViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            lfn=None,
            signed_url="",
        )

    def convert_response_to_view_model(self, response: DownloadFileResponse) -> DownloadFileViewModel:
        return DownloadFileViewModel(
            status=True,
            code=200,
            lfn=response.lfn,
            signed_url=response.credentials,
        )
