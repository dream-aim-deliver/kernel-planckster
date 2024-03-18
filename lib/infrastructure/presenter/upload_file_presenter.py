from lib.core.ports.primary.upload_file_primary_ports import UploadFileOutputPort
from lib.core.usecase_models.upload_file_usecase_models import UploadFileError, UploadFileResponse
from lib.core.view_model.upload_file_view_model import UploadFileViewModel


class UploadFilePresenter(UploadFileOutputPort):
    def convert_error_response_to_view_model(self, response: UploadFileError) -> UploadFileViewModel:
        return UploadFileViewModel(
            status=False,
            code=response.errorCode,
            errorCode=response.errorCode,
            errorMessage=response.errorMessage,
            errorName=response.errorName,
            errorType=response.errorType,
            lfn=None,
            signed_url="",
        )

    def convert_response_to_view_model(self, response: UploadFileResponse) -> UploadFileViewModel:
        return UploadFileViewModel(
            status=True,
            code=200,
            lfn=response.lfn,
            signed_url=response.credentials,
        )
