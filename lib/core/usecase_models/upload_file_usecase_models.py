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
    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    """

    lfn: LFN = Field(description="The Logical File Name of the uploaded file.")
    credentials: str = Field(
        description="The credentials to handle the file in question. For example, the signed URL, key, auth token, etc."
    )


class UploadFileError(BaseErrorResponse):
    """
    Error response model for the Upload File Use Case.
    """

    pass
