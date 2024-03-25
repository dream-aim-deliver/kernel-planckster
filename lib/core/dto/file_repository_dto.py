from lib.core.entity.models import ProtocolEnum, SourceData
from lib.core.sdk.dto import BaseDTO


class FilePathToSourceDataIndexDTO(BaseDTO):  # type: ignore
    """
    A DTO for whenever a file path is converted to a SourceData object.

    @param protocol: The protocol of the file.
    @type protocol: ProtocolEnum
    @param relative_path: The relative path of the file.
    @type relative_path: str
    """

    protocol: ProtocolEnum | None = None
    relative_path: str | None = None


class GetClientDataForUploadDTO(BaseDTO):  # type: ignore
    """
    A DTO for whenever a client wants to upload source data via a public upload.

    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    @type credentials: str
    """

    credentials: str | None = None


class GetClientDataForDownloadDTO(BaseDTO):  # type: ignore
    """
    A DTO for whenever source data is downloaded by the client.

    @param lfn: The logical file name of the file that was downloaded.
    @type lfn: LFN
    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    @type credentials: str
    """

    credentials: str | None = None


class SourceDataCompositeIndexExistsAsFileDTO(BaseDTO):  # type: ignore
    """
    A DTO for whenever the existence of a SourceData as an actual file is asserted.

    @param protocol: The protocol of the SourceData object in question.
    @type protocol: ProtocolEnum
    @param relative_path: The relative path of the SourceData object in the file system.
    @type relative_path: str
    @param existence: The existence of the SourceData object.
    @type existence: bool
    """

    protocol: ProtocolEnum | None = None
    relative_path: str | None = None
    existence: bool | None = None
