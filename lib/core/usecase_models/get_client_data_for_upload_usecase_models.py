from pydantic import Field, field_validator
from lib.core.entity.models import ProtocolEnum, SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class GetClientDataForUploadRequest(BaseRequest):
    """
    Request model for the Get Client Data For Upload Use Case.

    @param client_id: The ID of the client requesting the upload.
    @param protocol: The protocol of the file to be uploaded. Has to be one of the supported protocols.
    @param relative_path: The relative path of the file to be uploaded.
    """

    client_id: int = Field(description="The ID of the client requesting the upload.")
    protocol: str = Field(description="The protocol of the file to be uploaded.")
    relative_path: str = Field(description="The relative path of the file to be uploaded.")

    @field_validator("protocol")
    def protocol_must_be_supported(cls, v: str) -> str:
        SourceData.protocol_validation(v)
        return v

    @field_validator("relative_path")
    def relative_path_must_be_correctly_formatted(cls, v: str) -> str:
        SourceData.relative_path_validation(v)
        return v


class GetClientDataForUploadResponse(BaseResponse):
    """
    Response model for the Get Client Data For Upload Use Case.

    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    """

    credentials: str = Field(
        description="The credentials to handle the file in question. For example, the signed URL, key, auth token, etc."
    )


class GetClientDataForUploadError(BaseErrorResponse):
    """
    Error response model for the Get Client Data For Upload Use Case.
    """

    pass
