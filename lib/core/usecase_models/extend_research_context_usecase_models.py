from typing import List
from pydantic import Field
from lib.core.entity.models import LLM, ResearchContext
from lib.core.sdk.usecase_models import BaseErrorResponse, BaseRequest, BaseResponse


class ExtendResearchContextRequest(BaseRequest):
    """
    Request Model for the Use Case where a Research Context is Extended beyond its original data sources.

    @param new_research_context_title: Title of the new research context to be created to include new data sources.
    @param client_sub: SUB of the client for which the research context is to be created.
    @param llm_name: Name of the LLM for which the research context is to be created.
    @param new_source_data_ids: List of additional source data ids beyond those in the original research context.
    @param existing_research_context_id: ID of the existing research context to be extended.
    """

    new_research_context_title: str = Field(
        description="Title of the new research context to be created to include new data sources."
    )
    new_research_context_description: str = Field(description="Description of the research context to be created.")
    client_sub: str = Field(description="SUB of the client for which the research context is to be created.")
    llm_name: str = Field(description="Name of the LLM for which the research context is to be created.")
    new_source_data_ids: List[int] = Field(
        description="List of additional source data ids beyond those in the original research context."
    )
    existing_research_context_id: int = Field(description="ID of the existing research context to be extended.")
    external_id: str = Field(
        description="The UUID that is used to trace vector stores and agents in the externally managed databases."
    )


class ExtendResearchContextResponse(BaseResponse):
    """
    Response Model for the Use Case where a Research Context is Extended beyond its original data sources.

    @param research_context: The newly created research context.
    @param llm: The LLM of the newly created research context.
    """

    research_context: ResearchContext = Field(description="The newly created research context.")
    llm: LLM = Field(description="The LLM of the newly created research context.")


class ExtendResearchContextError(BaseErrorResponse):
    """
    Error Response Model for the Use Case where a Research Context is Extended beyond its original data sources.
    """

    pass
