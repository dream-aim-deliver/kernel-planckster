from lib.core.entity.models import LFN
from lib.core.sdk.dto import BaseDTO


class FilePathToLFNDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever a file path is converted to an LFN.

    @param lfn: The logical file name of the file.
    @type lfn: LFN
    """

    lfn: LFN | None = None


class UploadFileDTO(BaseDTO):  # type: ignore  # TODO: decide how to model these data entering core
    """
    A DTO for whenever source data is uploaded by the user.

    @param lfn: The logical file name of the file that was uploaded.
    @type lfn: LFN
    @param auth: The authentication string for the file that was uploaded.
    @type auth: str
    """

    lfn: LFN | None = None
    auth: str | None = None
