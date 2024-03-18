from fastapi import HTTPException
from pydantic import Field
from lib.core.sdk.controller import BaseController, BaseControllerParameters
from lib.core.usecase.upload_file_usecase import UploadFileUsecase
from lib.core.usecase_models.upload_file_usecase_models import UploadFileError, UploadFileRequest, UploadFileResponse
from lib.core.view_model.upload_file_view_model import UploadFileViewModel
from lib.infrastructure.presenter.upload_file_presenter import UploadFilePresenter


class UploadFileControllerParameters(BaseControllerParameters):
    file_path: str = Field(
        name="File Path",
        description="The path to the file to be uploaded.",
    )


class UploadFileController(
    BaseController[
        UploadFileControllerParameters,
        UploadFileRequest,
        UploadFileResponse,
        UploadFileError,
        UploadFileViewModel,
    ]
):
    def __init__(
        self,
        usecase: UploadFileUsecase,
        presenter: UploadFilePresenter,
    ) -> None:
        super().__init__(usecase=usecase, presenter=presenter)

    def create_request(self, parameters: UploadFileControllerParameters | None) -> UploadFileRequest:
        if parameters is None:
            raise HTTPException(status_code=400, detail="Invalid request parameters.")

        else:
            return UploadFileRequest(file_path=parameters.file_path)
