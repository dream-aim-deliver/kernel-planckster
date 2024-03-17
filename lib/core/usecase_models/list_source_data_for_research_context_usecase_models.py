from typing import List
from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class ListSourceDataForResearchContextRequest(BaseRequest):
    """
    Request Model for the List Source Data For Research Context Use Case.
    """

    research_context_id: int


class ListSourceDataForResearchContextResponse(BaseResponse):
    """
    Response Model for the List Source Data For Research Context Use Case.
    """

    source_data_list: List[SourceData]


class ListSourceDataForResearchContextError(BaseErrorResponse):
    """
    Error Response Model for the List Source Data For Research Context Use Case.
    """

    research_context_id: int
