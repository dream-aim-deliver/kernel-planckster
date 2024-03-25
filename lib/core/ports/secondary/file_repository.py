from abc import ABC, abstractmethod
import logging


from lib.core.dto.file_repository_dto import (
    GetClientDataForDownloadDTO,
    SourceDataCompositeIndexExistsAsFileDTO,
    GetClientDataForUploadDTO,
)
from lib.core.entity.models import Client, ProtocolEnum, SourceData


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

    # @abstractmethod
    # def file_path_to_source_data_composite_index(self, file_path: str) -> FilePathToSourceDataIndexDTO:
    # """
    # Converts a local file path to a unique identifier for a SourceData object.

    # @param file_path: The path to the file.
    # @type file_path: str
    # @return: A DTO containing the result of the operation.
    # @rtype: FilePathToLFNDTO
    # """
    # raise NotImplementedError

    @abstractmethod
    def get_client_data_for_upload(
        self, client: Client, protocol: ProtocolEnum, relative_path: str
    ) -> GetClientDataForUploadDTO:
        """
        Gets the file manager client data for uploading a file.

        @param client: The client uploading the file.
        @type client: Client
        @param protocol: The protocol of the file to upload.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the file to upload.
        @type relative_path: str
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """
        raise NotImplementedError

    @abstractmethod
    def get_client_data_for_download(self, client: Client, source_data: SourceData) -> GetClientDataForDownloadDTO:
        """
        Gets the file manager client data for downloading a file.

        @param client: The client downloading the file.
        @type client: Client
        @param source_data: The source data to download.
        @type source_data: SourceData
        @return: A DTO containing the result of the operation.
        @rtype: DownloadSourceDataDTO
        """
        raise NotImplementedError

    @abstractmethod
    def composite_index_of_source_data_exists_as_file(
        self, client: Client, protocol: ProtocolEnum, relative_path: str
    ) -> SourceDataCompositeIndexExistsAsFileDTO:
        """
        Asserts the existence of a composite index of source data as a file.

        @param client: The client asserting the existence of the source data.
        @type client: Client
        @param protocol: The protocol of the source data.
        @type protocol: ProtocolEnum
        @param relative_path: The relative path of the source data.
        @type relative_path: str
        @return: A DTO containing the result of the operation.
        @rtype: LFNExistsDTO
        """
        raise NotImplementedError
