from pydantic import Field
from typing import Optional
from lib.core.entity.models import SourceData
from lib.core.sdk.viewmodel import BaseViewModel


class NewSourceDataViewModel(BaseViewModel):
    """
    View Model for the New Source Data Feature.
    """

    source_data: Optional[SourceData] = Field(
        description="The source data object containing the metadata of the registered file."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": True,
                    "code": 200,
                    "source_data": {
                        "created_at": "2021-09-01T00:00:00",
                        "updated_at": "2021-09-01T00:00:00",
                        "deleted": False,
                        "deleted_at": None,
                        "id": 1,
                        "name": "Picture taken in context 123",
                        "relative_path": "wildfires/telegram/picture123.png",
                        "type": "png",
                        "protocol": "s3",
                        "status": "available",
                    },
                },
            ]
        }
    }
