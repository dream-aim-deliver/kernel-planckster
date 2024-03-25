from pydantic import Field, field_validator
from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class GetClientDataForDownloadRequest(BaseRequest):
    """
    Request model for the Download File Use Case.

    @param client_id: The ID of the client requesting the download.
    @param protocol: The protocol of the file to be downloaded. Has to be one of the supported protocols.
    @param relative_path: The relative path of the file to be downloaded.
    """

    client_id: int = Field(description="The ID of the client requesting the download.")
    protocol: str = Field(description="The protocol of the file to be downloaded.")
    relative_path: str = Field(description="The relative path of the file to be downloaded.")

    @field_validator("protocol", mode="before")
    def protocol_must_be_supported(cls, v: str) -> str:
        SourceData.protocol_validation(v)
        return v

    @field_validator("relative_path", mode="before")
    def relative_path_must_be_correctly_formatted(cls, v: str) -> str:
        SourceData.relative_path_validation(v)
        return v


class GetClientDataForDownloadResponse(BaseResponse):
    """
    Response model for the Download File Use Case.

    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    """

    credentials: str = Field(
        description="The credentials to handle the file in question. For example, the signed URL, key, auth token, etc."
    )


class GetClientDataForDownloadError(BaseErrorResponse):
    """
    Error response model for the Download File Use Case.
    """

    pass
