from typing import List
from lib.core.entity.models import SourceData
from lib.core.sdk.dto import BaseDTO


class NewSourceDataDTO(BaseDTO[SourceData]):
    """
    A DTO for whenever new source data is registered in the database.

    @param data: The source data that was registered.
    @type data: SourceData | None = None
    """

    data: SourceData | None = None
