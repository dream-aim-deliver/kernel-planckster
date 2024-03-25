from typing import List
from pydantic import Field
from lib.core.entity.models import ResearchContext
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class ListResearchContextsRequest(BaseRequest):
    """
    Request Model for the List Research Contexts Use Case.
    """

    client_id: int = Field(description="Client ID for which the research contexts are to be listed.")


class ListResearchContextsResponse(BaseResponse):
    """
    Response Model for the List Research Contexts Use Case.
    """

    client_id: int = Field(description="Client ID for which the research contexts are to be listed.")
    research_contexts: List[ResearchContext] = Field(description="List of research contexts for the client.")


class ListResearchContextsError(BaseErrorResponse):
    """
    Error Response Model for the List Research Contexts Use Case.
    """

    client_id: int = Field(description="Client ID that was passed in the request.")
