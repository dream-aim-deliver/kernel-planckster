from lib.core.entity.models import ResearchContext, User
from lib.core.sdk.dto import BaseDTO


class GetUserDTO(BaseDTO[User]):
    """
    A DTO for getting a user

    @param data: The user
    """

    data: User | None = None

class NewUserResearchContextDTO(BaseDTO[ResearchContext]):
    """
    A DTO for whenever a new research context is created

    @param research_context_id: The id of the new research context
    @type research_context_id: int | None
    """

    research_context_id: int | None = None