from lib.core.entity.models import SourceData
from lib.core.sdk.dto import BaseDTO


class GetSourceDataByProtocolRelativePathDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever source data is retrieved by protocol and relative path
    """

    data: SourceData | None = None
