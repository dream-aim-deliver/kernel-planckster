from typing import List
from lib.core.entity.models import LLM, ResearchContext, Client, SourceData
from lib.core.sdk.dto import BaseDTO


class GetClientDTO(BaseDTO[Client]):
    """
    A DTO for getting a client

    @param data: The client
    """

    data: Client | None = None


class NewResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for whenever a new research context is created

    @param research_context_id: The id of the new research context
    @type research_context_id: int | None
    """

    research_context: ResearchContext | None = None
    llm: LLM | None = None


class ListResearchContextsDTO(BaseDTO[ResearchContext]):
    """
    A DTO for listing the research contexts of a client

    @param data: The research contexts
    @type data: List[ResearchContext] | None
    """

    data: list[ResearchContext] | None = None


class NewSourceDataDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever new source data is registered in the database.

    @param data: The source data that was registered.
    @type data: SourceData | None = None
    """

    data: SourceData | None = None


class ListSourceDataDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever source data is listed

    @param data: The source data
    @type data: List[SourceData]
    """

    data: List[SourceData] = []
