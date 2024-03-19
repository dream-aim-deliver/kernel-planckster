from abc import abstractmethod
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.download_file_usecase_models import (
    DownloadFileError,
    DownloadFileRequest,
    DownloadFileResponse,
)
from lib.core.view_model.download_file_view_model import DownloadFileViewModel


class DownloadFileInputPort(BaseUseCase[DownloadFileRequest, DownloadFileResponse, DownloadFileError]):
    def __init__(self, file_repository: FileRepositoryOutputPort) -> None:
        self._file_repository = file_repository

    @property
    def file_repository(self) -> FileRepositoryOutputPort:
        return self._file_repository

    @abstractmethod
    def execute(self, request: DownloadFileRequest) -> DownloadFileResponse | DownloadFileError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class DownloadFileOutputPort(BasePresenter[DownloadFileResponse, DownloadFileError, DownloadFileViewModel]):
    @abstractmethod
    def convert_error_response_to_view_model(self, response: DownloadFileError) -> DownloadFileViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(self, response: DownloadFileResponse) -> DownloadFileViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
