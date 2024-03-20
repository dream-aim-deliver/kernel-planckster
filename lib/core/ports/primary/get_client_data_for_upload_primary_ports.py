from abc import abstractmethod
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort
from lib.core.sdk.presenter import BasePresenter
from lib.core.sdk.usecase import BaseUseCase
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadError,
    GetClientDataForUploadRequest,
    GetClientDataForUploadResponse,
)
from lib.core.view_model.get_client_data_for_upload_view_model import GetClientDataForUploadViewModel


class GetClientDataForUploadInputPort(
    BaseUseCase[GetClientDataForUploadRequest, GetClientDataForUploadResponse, GetClientDataForUploadError]
):
    def __init__(self, file_repository: FileRepositoryOutputPort) -> None:
        self._file_repository = file_repository

    @property
    def file_repository(self) -> FileRepositoryOutputPort:
        return self._file_repository

    @abstractmethod
    def execute(
        self, request: GetClientDataForUploadRequest
    ) -> GetClientDataForUploadResponse | GetClientDataForUploadError:
        raise NotImplementedError("This method must be implemented by the usecase.")


class GetClientDataForUploadOutputPort(
    BasePresenter[GetClientDataForUploadResponse, GetClientDataForUploadError, GetClientDataForUploadViewModel]
):
    @abstractmethod
    def convert_error_response_to_view_model(
        self, response: GetClientDataForUploadError
    ) -> GetClientDataForUploadViewModel:
        raise NotImplementedError(
            "You must implement the convert_error_response_to_view_model method in your presenter"
        )

    @abstractmethod
    def convert_response_to_view_model(
        self, response: GetClientDataForUploadResponse
    ) -> GetClientDataForUploadViewModel:
        raise NotImplementedError("You must implement the convert_response_to_view_model method in your presenter")
