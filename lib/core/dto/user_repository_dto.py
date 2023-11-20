from lib.core.entity.models import LLM, ResearchContext, User
from lib.core.sdk.dto import BaseDTO


class GetUserDTO(BaseDTO[User]):
    """
    A DTO for getting a user

    @param data: The user
    """

    data: User | None = None


class NewResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for whenever a new research context is created

    @param research_context_id: The id of the new research context
    @type research_context_id: int | None
    """

    research_context: ResearchContext | None = None
    llm: LLM | None = None


class ListUserResearchContextsDTO(BaseDTO[ResearchContext]):
    """
    A DTO for listing the research contexts of a user

    @param data: The research contexts
    @type data: List[ResearchContext] | None
    """

    data: list[ResearchContext] | None = None
