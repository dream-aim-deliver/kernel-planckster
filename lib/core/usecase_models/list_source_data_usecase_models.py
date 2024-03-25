from typing import List

from lib.core.entity.models import SourceData
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class ListSourceDataRequest(BaseRequest):
    """
    Request Model for the List Source Data Use Case.

    @param client_id: The ID of the client requesting the list of source data.
    """

    client_id: int


class ListSourceDataResponse(BaseResponse):
    """
    Response Model for the List Source Data Use Case.

    @param source_data_list: The list of source data.
    """

    source_data_list: List[SourceData]


class ListSourceDataError(BaseErrorResponse):
    """
    Error Response Model for the List Source Data Use Case.

    @param client_id: The ID of the client requesting the list of source data.
    """

    client_id: int | None = None
