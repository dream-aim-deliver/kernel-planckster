from typing import List
from pydantic import Field
from lib.core.entity.models import LLM, ResearchContext
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class NewResearchContextRequest(BaseRequest):
    """
    Request Model for the New Research Context Use Case.

    @param research_context_title: Title of the research context to be created.
    @param client_sub: SUB of the client for which the research context is to be created.
    @param llm_name: Name of the LLM for which the research context is to be created.
    @param source_data_ids: List of source data ids for which the research context is to be created.
    """

    research_context_title: str = Field(description="Title of the research context to be created.")
    research_context_description: str = Field(description="Description of the research context to be created.")
    client_sub: str = Field(description="SUB of the client for which the research context is to be created.")
    llm_name: str = Field(description="Name of the LLM for which the research context is to be created.")
    source_data_ids: List[int] = Field(
        description="List of source data ids for which the research context is to be created."
    )


class NewResearchContextResponse(BaseResponse):
    """
    Response Model for the New Source Data Use Case.

    @param research_context: The newly created research context.
    @param llm: The LLM of the newly created research context.
    """

    research_context: ResearchContext = Field(description="The newly created research context.")
    llm: LLM = Field(description="The LLM of the newly created research context.")


class NewResearchContextError(BaseErrorResponse):
    """
    Error Response Model for the New Source Data Use Case.
    """

    pass
