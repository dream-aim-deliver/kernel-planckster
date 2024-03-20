from abc import ABC, abstractmethod
import logging

from lib.core.dto.file_repository_dto import (
    GetClientDataForDownloadDTO,
    FilePathToLFNDTO,
    LFNExistsDTO,
    GetClientDataForUploadDTO,
)
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
    def get_client_data_for_upload(self, lfn: LFN) -> GetClientDataForUploadDTO:
        """
        Gets client data for uploading a file.

        @param lfn: The logical file name of the file to upload.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """
        raise NotImplementedError

    @abstractmethod
    def get_client_data_for_download(self, lfn: LFN) -> GetClientDataForDownloadDTO:
        """
        Gets client data for downloading a file.

        @param lfn: The logical file name of the file to download.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: DownloadSourceDataDTO
        """
        raise NotImplementedError

    @abstractmethod
    def lfn_exists(self, lfn: LFN) -> LFNExistsDTO:
        """
        Asserts the existence of an LFN as an actual file.

        @param lfn: The logical file name to assert the existence of.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: LFNExistsDTO
        """
        raise NotImplementedError
