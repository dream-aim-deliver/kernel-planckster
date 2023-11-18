from abc import ABC, abstractmethod
import logging

from lib.core.dto.user_repository_dto import GetUserDTO


class UserRepositoryOutputPort(ABC):
    """
    Abstract base class for the user repository.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def get_user(self, user_id: int) -> GetUserDTO:
        """
        Gets a user by ID.

        @param user_id: The ID of the user to get.
        @type user_id: int
        @return: A DTO containing the result of the operation.
        @rtype: GetUserDTO
        """
        raise NotImplementedError
