from typing import List

from lib.core.entity.models import SourceData
from lib.core.sdk.dto import BaseDTO


class ListSourceDataDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever source data is listed
    """

    data: List[SourceData] = []


class GetSourceDataByLFNDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever source data is retrieved by LFN
    """

    data: SourceData | None = None
