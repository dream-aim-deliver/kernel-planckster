from lib.core.entity.models import User
from lib.core.sdk.dto import BaseDTO


class GetUserDTO(BaseDTO[User]):
    """
    A DTO for getting a user

    @param data: The user
    """

    data: User | None = None
