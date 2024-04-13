from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.get_client_data_for_download_usecase import GetClientDataForDownloadUseCase
from lib.core.usecase_models.get_client_data_for_download_usecase_models import (
    GetClientDataForDownloadError,
    GetClientDataForDownloadRequest,
    GetClientDataForDownloadResponse,
)
from lib.core.view_model.get_client_data_for_download_view_model import GetClientDataForDownloadViewModel
from lib.infrastructure.presenter.get_client_data_for_download_presenter import GetClientDataForDownloadPresenter


class GetClientDataForDownloadControllerParameters(BaseControllerParameters):
    client_id: int = Field(title="Client ID", description="The ID of the client requesting the download.")

    protocol: str = Field(title="Protocol", description="The protocol of the file to be downloaded.")

    relative_path: str = Field(title="Relative Path", description="The relative path of the file to be downloaded.")


class GetClientDataForDownloadController(
    BaseController[
        GetClientDataForDownloadControllerParameters,
        GetClientDataForDownloadRequest,
        GetClientDataForDownloadResponse,
        GetClientDataForDownloadError,
        GetClientDataForDownloadViewModel,
    ]
):
    def __init__(
        self,
        usecase: GetClientDataForDownloadUseCase,
        presenter: GetClientDataForDownloadPresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(
        self, parameters: GetClientDataForDownloadControllerParameters | None
    ) -> GetClientDataForDownloadRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")

        else:
            return GetClientDataForDownloadRequest(
                client_id=parameters.client_id,
                protocol=parameters.protocol,
                relative_path=parameters.relative_path,
            )
