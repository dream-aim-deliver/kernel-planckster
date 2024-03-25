from pydantic import Field, field_validator
from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewSourceDataRequest(BaseRequest):
    """
    Request Model for the New Source Data Use Case.
    """

    client_id: int = Field(description="Knowledge source id for which the source data is to be registered.")
    source_data_name: str = Field(
        description="Name of the source data to be registered. Should be a meaningful non-empty string that can be shown to end users. No constraints are put on the format of the name and will be stored as-is, but it will only be stored as meta data, not passed to the storage system."
    )
    protocol: str = Field(description="The protocol used to access the source data.")
    relative_path: str = Field(description="The relative path to the source data.")

    @field_validator("source_data_name")
    def source_data_name_must_be_correctly_formatted(cls, v: str) -> str:
        SourceData.name_validation(v)
        return v

    @field_validator("protocol")
    def protocol_must_be_supported(cls, v: str) -> str:
        SourceData.protocol_validation(v)
        return v

    @field_validator("relative_path")
    def relative_path_must_be_correctly_formatted(cls, v: str) -> str:
        SourceData.relative_path_validation(v)
        return v


class NewSourceDataResponse(BaseResponse):
    """
    Response Model for the New Source Data Use Case.
    """

    source_data: SourceData = Field(description="The source data registered in the database.")


class NewSourceDataError(BaseErrorResponse):
    """
    Error Response Model for the New Source Data Use Case.
    """

    pass
