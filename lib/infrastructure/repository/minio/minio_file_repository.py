from lib.core.dto.file_repository_dto import (
    GetClientDataForDownloadDTO,
    SourceDataCompositeIndexExistsAsFileDTO,
    GetClientDataForUploadDTO,
)
from lib.core.entity.models import Client, ProtocolEnum, SourceData
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort

from lib.infrastructure.repository.minio.minio_object_store import MinIOObjectStore


class MinIOFileRepository(FileRepositoryOutputPort):
    """
    A MinIO implementation of the file repository.

    @ivar store: The MinIO object store.
    @type store: MinIOObjectStore
    """

    def __init__(self, object_store: MinIOObjectStore) -> None:
        super().__init__()

        self._store = object_store

    @property
    def store(self) -> MinIOObjectStore:
        return self._store

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
        if client is None:
            self.logger.error("Client cannot be None")
            return GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client cannot be None",
                errorName="ClientNotProvided",
                errorType="ClientNotProvided",
            )

        if protocol is None:
            self.logger.error("Protocol cannot be None")
            return GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Protocol cannot be None",
                errorName="ProtocolNotProvided",
                errorType="ProtocolNotProvided",
            )

        if relative_path is None:
            self.logger.error("Relative path cannot be None")
            return GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Relative path cannot be None",
                errorName="RelativePathNotProvided",
                errorType="RelativePathNotProvided",
            )

        try:
            pfn = self.store.protocol_and_relative_path_to_pfn(
                protocol=protocol, relative_path=relative_path, bucket_name=client.sub
            )

            minio_object = self.store.pfn_to_object_name(pfn)

            url = self.store.get_signed_url_for_file_upload(minio_object)

        except Exception as e:
            self.logger.error(f"Could not get signed URL to upload the file to MinIO Repository: {e}")
            errorDTO = GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not upload the file to MinIO Repository: {e}",
                errorName="CouldNotGetClientDataForUpload",
                errorType="CouldNotGetClientDataForUpload",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if url is None:
            self.logger.error("Could not get signed URL to upload the file to MinIO Repository: URL is 'None'")
            errorDTO = GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Could not get signed URL to upload the file to MinIO Repository: URL is 'None'",
                errorName="SignedURLIsNone",
                errorType="SignedURLIsNone",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        return GetClientDataForUploadDTO(
            status=True,
            credentials=url,
        )

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

        if client is None:
            self.logger.error("Client cannot be None")
            return GetClientDataForDownloadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Client cannot be None",
                errorName="ClientNotProvided",
                errorType="ClientNotProvided",
            )

        if source_data is None:
            self.logger.error("Source data cannot be None")
            return GetClientDataForDownloadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Source data cannot be None",
                errorName="SourceDataNotProvided",
                errorType="SourceDataNotProvided",
            )

        try:
            pfn = self.store.protocol_and_relative_path_to_pfn(
                protocol=source_data.protocol, relative_path=source_data.relative_path, bucket_name=client.sub
            )

            minio_object = self.store.pfn_to_object_name(pfn)

            url = self.store.get_signed_url_for_file_download(minio_object)

        except Exception as e:
            self.logger.error(f"Could not get signed URL to download the file from MinIO Repository: {e}")
            errorDTO = GetClientDataForDownloadDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not download the file from MinIO Repository: {e}",
                errorName="CouldNotGetClientDataForDownload",
                errorType="CouldNotGetClientDataForDownload",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if url is None:
            self.logger.error("Could not get signed URL to download the file from MinIO Repository: URL is 'None'")
            errorDTO = GetClientDataForDownloadDTO(
                status=False,
                errorCode=-1,
                errorMessage="Could not get signed URL to download the file from MinIO Repository: URL is 'None'",
                errorName="SignedURLIsNone",
                errorType="SignedURLIsNone",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        return GetClientDataForDownloadDTO(
            status=True,
            credentials=url,
        )

    def composite_index_of_source_data_exists_as_file(
        self, client: Client, protocol: ProtocolEnum, relative_path: str
    ) -> SourceDataCompositeIndexExistsAsFileDTO:
        """
        Asserts the existence of a SourceData object as an actual file.

        @param client: The client asserting the existence of the source data.
        @type client: Client
        @param lfn: The logical file name to assert the existence of.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: LFNExistsDTO
        """
        if protocol is None:
            self.logger.error("Protocol cannot be None")
            return SourceDataCompositeIndexExistsAsFileDTO(
                existence=None,
                status=False,
                errorCode=-1,
                errorMessage="Protocol cannot be None",
                errorName="ProtocolNotProvided",
                errorType="ProtocolNotProvided",
            )

        if relative_path is None:
            self.logger.error("Relative path cannot be None")
            return SourceDataCompositeIndexExistsAsFileDTO(
                existence=None,
                status=False,
                errorCode=-1,
                errorMessage="Relative path cannot be None",
                errorName="RelativePathNotProvided",
                errorType="RelativePathNotProvided",
            )

        try:
            pfn = self.store.protocol_and_relative_path_to_pfn(
                protocol=protocol, relative_path=relative_path, bucket_name=client.sub
            )

            minio_object = self.store.pfn_to_object_name(pfn)

            existence = self.store.object_exists(minio_object)

        except Exception as e:
            self.logger.error(f"Could not assert the existence of the file in MinIO Repository: {e}")
            return SourceDataCompositeIndexExistsAsFileDTO(
                existence=None,
                status=False,
                errorCode=-1,
                errorMessage=f"Could not assert the existence of the file in MinIO Repository: {e}",
                errorName="CouldNotAssertExistence",
                errorType="CouldNotAssertExistence",
            )

        return SourceDataCompositeIndexExistsAsFileDTO(
            status=True,
            existence=existence,
            protocol=pfn.protocol,
            relative_path=pfn.relative_path,
        )
