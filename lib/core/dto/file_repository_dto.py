from lib.core.entity.models import LFN
from lib.core.sdk.dto import BaseDTO


class FilePathToLFNDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever a file path is converted to an LFN.

    @param lfn: The logical file name of the file.
    @type lfn: LFN
    """

    lfn: LFN | None = None


class GetClientDataForUploadDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever a user wants to upload source data via a public upload.

    @param lfn: The logical file name of the file that was uploaded.
    @type lfn: LFN
    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    @type credentials: str
    """

    lfn: LFN | None = None
    credentials: str | None = None


class GetClientDataForDownloadDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever source data is downloaded by the user.

    @param lfn: The logical file name of the file that was downloaded.
    @type lfn: LFN
    @param credentials: The credentials to handle the file in question. For example, the signed URL, key, auth token, etc.
    @type credentials: str
    """

    lfn: LFN | None = None
    credentials: str | None = None


class LFNExistsDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever the existence of an LFN as an actual file is asserted.

    @param lfn: The logical file name to assert the existence of.
    @type lfn: LFN
    """

    lfn: LFN | None = None
    existence: bool | None = None
