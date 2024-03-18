from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class UploadFileRequest(BaseRequest):
    """
    Request model for the Upload File Use Case.

    @param file_path: The path of the file to be uploaded.
    """

    file_path: str = Field(description="The path of the file to be uploaded.")


class UploadFileResponse(BaseResponse):
    """
    Response model for the Upload File Use Case.

    @param lfn: The Logical File Name of the uploaded file.
    @param auth: The authorization string to handle the uploaded file.
    """

    lfn: LFN = Field(description="The Logical File Name of the uploaded file.")
    auth: str = Field(description="The authorization string to handle the uploaded file.")


class UploadFileError(BaseErrorResponse):
    """
    Error response model for the Upload File Use Case.
    """

    pass
