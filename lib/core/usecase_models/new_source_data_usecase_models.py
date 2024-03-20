from typing import List
from pydantic import Field
from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewSourceDataRequest(BaseRequest):
    """
    Request Model for the New Source Data Use Case.
    """

    knowledge_source_id: int = Field(description="Research context id for which the source data is to be registered.")
    lfn: str = Field(
        description="LFN of the source data to be registered. Must be already present as a file in the file storage."
    )


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
