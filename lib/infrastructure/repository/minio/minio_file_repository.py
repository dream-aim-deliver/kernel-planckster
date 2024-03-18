from lib.core.dto.file_repository_dto import UploadFileDTO
from lib.core.ports.secondary.file_repository import FileRepositoryOutputPort

from lib.infrastructure.repository.minio.object_store import ObjectStore


class MinIOFileRepository(FileRepositoryOutputPort):
    """
    A MinIO implementation of the file repository.
    """

    def __init__(self, object_store: ObjectStore) -> None:
        super().__init__()

        self._store = object_store

    @property
    def store(self) -> ObjectStore:
        return self._store

    def upload_file(self, file_path: str) -> UploadFileDTO:
        """
        Uploads a user source data file to a bucket in MinIO S3 Repository.

        @param file_path: The name of the file to upload.
        @type file_path: str
        @return: A DTO containing the result of the operation.
        @rtype: UploadSourceDataDTO
        """

        if file_path is None:
            self.logger.error("File path cannot be None")
            errorDTO = UploadFileDTO(
                status=False,
                errorCode=-1,
                errorMessage="File path cannot be None",
                errorName="FilePathNotProvided",
                errorType="FilePathNotProvided",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        try:
            lfn = self.store.file_path_to_lfn(file_path)
            pfn = self.store.lfn_to_pfn(lfn)
            object_name = self.store.pfn_to_object_name(pfn)

            url = self.store.get_signed_url_for_file_upload(self.store.bucket, object_name)

        except Exception as e:
            self.logger.error(f"Could not get signed URL to upload the file to MinIO Repository: {e}")
            errorDTO = UploadFileDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Could not upload the file to MinIO Repository: {e}",
                errorName="CouldNotUploadFile",
                errorType="CouldNotUploadFile",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if url is None:
            self.logger.error("Could not get signed URL to upload the file to MinIO Repository: URL is 'None'")
            errorDTO = UploadFileDTO(
                status=False,
                errorCode=-1,
                errorMessage="Could not get signed URL to upload the file to MinIO Repository: URL is 'None'",
                errorName="SignedURLIsNone",
                errorType="SignedURLIsNone",
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO

        return UploadFileDTO(
            status=True,
            lfn=lfn,
            auth=url,
        )
