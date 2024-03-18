from abc import abstractmethod
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.upload_file_usecase_models import UploadFileError, UploadFileRequest, UploadFileResponse
from lib.core.view_model.upload_file_view_model import UploadFileViewModel


class UploadFileInputPort(BaseUseCase[UploadFileRequest, UploadFileResponse, UploadFileError]):
    def __init__(self, file_repository: FileRepositoryOutputPort) -> None:
        self._file_repository = file_repository

    @property
    def file_repository(self) -> FileRepositoryOutputPort:
        return self._file_repository

    @abstractmethod
    def execute(self, request: UploadFileRequest) -> UploadFileResponse | UploadFileError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class UploadFileOutputPort(BasePresenter[UploadFileResponse, UploadFileError, UploadFileViewModel]):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: UploadFileError) -> UploadFileViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: UploadFileResponse) -> UploadFileViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
