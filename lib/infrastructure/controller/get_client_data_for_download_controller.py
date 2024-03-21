from fastapi import HTTPException
from pydantic import Field
from lib.core.entity.models import LFN
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
    lfn_str: str = Field(
        title="Logical File Name",
        description="The Logical File Name of the file to be downloaded, in JSON format.",
    )


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
            return GetClientDataForDownloadRequest(lfn_str=parameters.lfn_str)
