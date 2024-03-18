from abc import ABC, abstractmethod
import logging

from lib.core.dto.file_repository_dto import UploadFileDTO


class FileRepositoryOutputPort(ABC):
    """
    Abstract base class for the file repository output port.

    @cvar logger: The logger for this class
    @type logger: logging.Logger
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @abstractmethod
    def upload_file(self, file_path: str) -> UploadFileDTO:
        """
        Uploads source data.

        @param file_path: The name of the file to upload.
        @type file_path: str
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """
        raise NotImplementedError
