from abc import ABC, abstractmethod
import logging

from lib.core.dto.file_repository_dto import FilePathToLFNDTO, UploadFileDTO
from lib.core.entity.models import LFN


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
    def file_path_to_lfn(self, file_path: str) -> FilePathToLFNDTO:
        """
        Converts a local file path to a logical file name.

        @param file_path: The path to the file.
        @type file_path: str
        @return: A DTO containing the result of the operation.
        @rtype: FilePathToLFNDTO
        """
        raise NotImplementedError

    @abstractmethod
    def upload_file(self, lfn: LFN) -> UploadFileDTO:
        """
        Uploads source data.

        @param lfn: The logical file name of the file to upload.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """
        raise NotImplementedError
