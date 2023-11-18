from lib.core.dto.user_repository_dto import GetUserDTO
from lib.core.entity.models import User
from lib.core.ports.secondary.user_repository import UserRepositoryOutputPort
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLAUser
from lib.infrastructure.repository.sqla.utils import convert_sqla_user_to_core_user


class SQLAUserRepository(UserRepositoryOutputPort):
    """
    A SQLAlchemy implementation of the user repository.
    """

    def __init__(self, session_factory: TDatabaseFactory) -> None:
        super().__init__()
        with session_factory() as session:
            self._session = session

    @property
    def session(self) -> Session:
        return self._session

    def get_user(self, user_id: int) -> GetUserDTO:
        """
        Gets a user by ID.

        @param user_id: The ID of the user to get.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetUserDTO
        """

        if user_id is None:
            self.logger.error("User ID cannot be None")
            errorDTO = GetUserDTO(
                status=False,
                errorCode=-1,
                errorMessage="User ID cannot be None",
                errorName="User ID not provided",
                errorType="UserIdNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        sqla_user: SQLAUser | None = self.session.get(SQLAUser, user_id)

        if sqla_user is None:
            self.logger.error(f"User with ID {user_id} not found in the database")
            errorDTO = GetUserDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"User with ID {user_id} not found in the database",
                errorName="User not found",
                errorType="UserNotFound",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        core_user: User = convert_sqla_user_to_core_user(sqla_user)

        return GetUserDTO(status=True, data=core_user)
