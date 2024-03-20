from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class GetClientDataForUploadRequest(BaseRequest):
    """
    Request model for the Get Client Data For Upload Use Case.

    @param file_path: The path of the file to be uploaded.
    """

    lfn_str: str = Field(description="The lfn of the file to be uploaded.")


class GetClientDataForUploadResponse(BaseResponse):
    """
    Response model for the Get Client Data For Upload Use Case.

    @param lfn: The Logical File Name of the uploaded file.
    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    """

    lfn: LFN = Field(description="The Logical File Name of the file that can be uploaded.")
    credentials: str = Field(
        description="The credentials to handle the file in question. For example, the signed URL, key, auth token, etc."
    )


class GetClientDataForUploadError(BaseErrorResponse):
    """
    Error response model for the Get Client Data For Upload Use Case.
    """

    pass
