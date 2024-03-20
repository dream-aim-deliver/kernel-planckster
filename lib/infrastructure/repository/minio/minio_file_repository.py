from datetime import datetime
import os
from lib.core.dto.file_repository_dto import (
    GetClientDataForDownloadDTO,
    FilePathToLFNDTO,
    LFNExistsDTO,
    GetClientDataForUploadDTO,
)
from lib.core.entity.models import LFN, KnowledgeSourceEnum, ProtocolEnum
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort

from lib.infrastructure.repository.minio.minio_object_store import MinIOObjectStore


class MinIOFileRepository(FileRepositoryOutputPort):
    """
    A MinIO implementation of the file repository.
    """

    def __init__(self, object_store: MinIOObjectStore) -> None:
        super().__init__()

        self._store = object_store

    @property
    def store(self) -> MinIOObjectStore:
        return self._store

    def file_path_to_lfn(self, file_path: str) -> FilePathToLFNDTO:
        """
        Converts a local file path to a logical file name.

        @param file_path: The path to the file.
        @type file_path: str
        @return: A DTO containing the result of the operation.
        @rtype: FilePathToLFNDTO
        """

        if file_path is None:
            self.logger.error("File path cannot be None")
            return FilePathToLFNDTO(
                lfn=None,
                status=False,
                errorCode=-1,
                errorMessage="File path cannot be None",
                errorName="FilePathNotProvided",
                errorType="FilePathNotProvided",
            )

        try:
            self.store.initialize_store()

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            int_ts = int(timestamp)

            base_name = os.path.basename(file_path)

            lfn = LFN(
                protocol=ProtocolEnum.S3,
                tracer_id="user_uploads",
                source=KnowledgeSourceEnum.USER,
                job_id=int_ts,
                relative_path=base_name,
            )

            return FilePathToLFNDTO(status=True, lfn=lfn)

        except Exception as e:
            self.logger.error(f"Could not convert file path to LFN: {e}")
            return FilePathToLFNDTO(
                lfn=None,
                status=False,
                errorCode=-1,
                errorMessage=f"Could not convert file path to LFN: {e}",
                errorName="CouldNotConvertFilePathToLFN",
                errorType="CouldNotConvertFilePathToLFN",
            )

    def get_client_data_for_upload(self, lfn: LFN) -> GetClientDataForUploadDTO:
        """
        Uploads a user source data file to a bucket in MinIO S3 Repository.

        @param file_path: The name of the file to upload.
        @type file_path: str
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """

        if lfn is None:
            self.logger.error("LFN cannot be None")
            return GetClientDataForUploadDTO(
                status=False,
                errorCode=-1,
                errorMessage="LFN cannot be None",
                errorName="LFNNotProvided",
                errorType="LFNNotProvided",
            )

        try:
            self.store.initialize_store()

            pfn = self.store.lfn_to_pfn(lfn)
            object_name = self.store.pfn_to_object_name(pfn)

            url = self.store.get_signed_url_for_file_upload(self.store.bucket, object_name)

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
            lfn=lfn,
            credentials=url,
        )

    def get_client_data_for_download(self, lfn: LFN) -> GetClientDataForDownloadDTO:
        """
        Downloads source data.

        @param lfn: The logical file name of the file to download.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: DownloadSourceDataDTO
        """

        if lfn is None:
            self.logger.error("LFN cannot be None")
            return GetClientDataForDownloadDTO(
                status=False,
                errorCode=-1,
                errorMessage="LFN cannot be None",
                errorName="LFNNotProvided",
                errorType="LFNNotProvided",
            )

        try:
            self.store.initialize_store()

            pfn = self.store.lfn_to_pfn(lfn)
            object_name = self.store.pfn_to_object_name(pfn)

            url = self.store.get_signed_url_for_file_download(self.store.bucket, object_name)

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
            lfn=lfn,
            credentials=url,
        )

    def lfn_exists(self, lfn: LFN) -> LFNExistsDTO:
        """
        Asserts the existence of an LFN as an actual file.

        @param lfn: The logical file name to assert the existence of.
        @type lfn: LFN
        @return: A DTO containing the result of the operation.
        @rtype: LFNExistsDTO
        """

        if lfn is None:
            self.logger.error("LFN cannot be None")
            return LFNExistsDTO(
                lfn=None,
                existence=None,
                status=False,
                errorCode=-1,
                errorMessage="LFN cannot be None",
                errorName="LFNNotProvided",
                errorType="LFNNotProvided",
            )

        try:
            self.store.initialize_store()

            # Turn lfn to object_name
            pfn = self.store.lfn_to_pfn(lfn)
            object_name = self.store.pfn_to_object_name(pfn)

            existence = self.store.object_exists(object_name)

        except Exception as e:
            self.logger.error(f"Could not assert the existence of the file in MinIO Repository: {e}")
            return LFNExistsDTO(
                lfn=lfn,
                existence=None,
                status=False,
                errorCode=-1,
                errorMessage=f"Could not assert the existence of the file in MinIO Repository: {e}",
                errorName="CouldNotAssertExistence",
                errorType="CouldNotAssertExistence",
            )

        return LFNExistsDTO(
            lfn=lfn,
            existence=existence,
            status=True,
        )
