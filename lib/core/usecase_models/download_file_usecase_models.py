from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class DownloadFileRequest(BaseRequest):
    """
    Request model for the Download File Use Case.

    @param lfn: The Logical File Name of the file to be downloaded.
    """

    lfn_json: str = Field(
        description="The Logical File Name of the file to be downloaded in JSON format, passed as a string."
    )


class DownloadFileResponse(BaseResponse):
    """
    Response model for the Download File Use Case.

    @param file_path: The path of the downloaded file.
    """

    lfn: LFN = Field(description="The Logical File Name of the file to be downloaded.")
    credentials: str = Field(
        description="The credentials to handle the file in question. For example, the signed URL, key, auth token, etc."
    )


class DownloadFileError(BaseErrorResponse):
    """
    Error response model for the Download File Use Case.
    """

    pass
