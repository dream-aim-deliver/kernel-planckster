from typing import List
from pydantic import Field
from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewSourceDataRequest(BaseRequest):
    """
    Request Model for the New Source Data Use Case.
    """

    knowledge_source_id: int = Field(description="Research context id for which the source data is to be created.")
    source_data_lfn_list: List[str] = Field(description="List of LFNs of the source data to be created.")


class NewSourceDataResponse(BaseResponse):
    """
    Response Model for the New Source Data Use Case.
    """

    pass


class NewSourceDataError(BaseErrorResponse):
    """
    Error Response Model for the New Source Data Use Case.
    """

    pass
