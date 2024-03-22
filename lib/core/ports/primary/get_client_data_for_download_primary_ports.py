from abc import abstractmethod
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort
from lib.core.ports.secondary.source_data_repository import SourceDataRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.get_client_data_for_download_usecase_models import (
    GetClientDataForDownloadError,
    GetClientDataForDownloadRequest,
    GetClientDataForDownloadResponse,
)
from lib.core.view_model.get_client_data_for_download_view_model import GetClientDataForDownloadViewModel


class GetClientDataForDownloadInputPort(
    BaseUseCase[GetClientDataForDownloadRequest, GetClientDataForDownloadResponse, GetClientDataForDownloadError]
):
    def __init__(
        self, file_repository: FileRepositoryOutputPort, source_data_repository: SourceDataRepositoryOutputPort
    ) -> None:
        self._file_repository = file_repository
        self._source_data_repository = source_data_repository

    @property
    def file_repository(self) -> FileRepositoryOutputPort:
        return self._file_repository

    @property
    def source_data_repository(self) -> SourceDataRepositoryOutputPort:
        return self._source_data_repository

    @abstractmethod
    def execute(
        self, request: GetClientDataForDownloadRequest
    ) -> GetClientDataForDownloadResponse | GetClientDataForDownloadError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class GetClientDataForDownloadOutputPort(
    BasePresenter[GetClientDataForDownloadResponse, GetClientDataForDownloadError, GetClientDataForDownloadViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(
        self, response: GetClientDataForDownloadError
    ) -> GetClientDataForDownloadViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(
        self, response: GetClientDataForDownloadResponse
    ) -> GetClientDataForDownloadViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
