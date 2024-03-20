from pydantic import Field
from typing import Optional
from lib.core.entity.models import LFN, SourceData
from lib.core.sdk.viewmodel import BaseViewModel


class NewSourceDataViewModel(BaseViewModel):
    """
    View Model for the New Source Data Feature.
    """

    source_data: Optional[SourceData] = Field(description="The Logical File Name of the registered file.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": True,
                },
            ]
        }
    }
