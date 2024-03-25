from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.get_client_data_for_upload_usecase import GetClientDataForUploadUsecase
from lib.core.usecase_models.get_client_data_for_upload_usecase_models import (
    GetClientDataForUploadError,
    GetClientDataForUploadRequest,
    GetClientDataForUploadResponse,
)
from lib.core.view_model.get_client_data_for_upload_view_model import GetClientDataForUploadViewModel
from lib.infrastructure.presenter.get_client_data_for_upload_presenter import GetClientDataForUploadPresenter


class GetClientDataForUploadControllerParameters(BaseControllerParameters):
    client_id: int = Field(title="Client ID", description="The ID of the client requesting the upload.")

    protocol: str = Field(title="Protocol", description="The protocol of the file to be uploaded.")

    relative_path: str = Field(title="Relative Path", description="The relative path of the file to be uploaded.")


class GetClientDataForUploadController(
    BaseController[
        GetClientDataForUploadControllerParameters,
        GetClientDataForUploadRequest,
        GetClientDataForUploadResponse,
        GetClientDataForUploadError,
        GetClientDataForUploadViewModel,
    ]
):
    def __init__(
        self,
        usecase: GetClientDataForUploadUsecase,
        presenter: GetClientDataForUploadPresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(
        self, parameters: GetClientDataForUploadControllerParameters | None
    ) -> GetClientDataForUploadRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")

        else:
            return GetClientDataForUploadRequest(
                client_id=parameters.client_id,
                protocol=parameters.protocol,
                relative_path=parameters.relative_path,
            )
