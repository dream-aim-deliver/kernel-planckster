from typing import List

from pydantic import Field
from lib.core.entity.models import SourceData
from lib.core.sdk.viewmodel import BaseViewModel


class ListSourceDataForResearchContextViewModel(BaseViewModel):
    """
    View Model for the List Source Data For Research Context Feature. Represents all source data in the database for a given research context.
    """

    source_data_list: List[SourceData] = Field(
        description="List of source data in the database for a given research context."
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "source_data_list": [
                        {
                            "id": 1,
                            "name": "file1",
                            "type": "pdf",
                            "lfn": {
                                "protocol": "s3",
                                "tracer_id": 1234567890,
                                "job_id": 1,
                                "source": "telegram",
                                "relative_path": "path/to/file",
                            },
                            "protocol": "s3",
                            "status": "available",
                        },
                        {
                            "id": 2,
                            "name": "file2",
                            "type": "pdf",
                            "lfn": {
                                "protocol": "s3",
                                "tracer_id": 1234567891,
                                "job_id": 2,
                                "source": "telegram",
                                "relative_path": "path/to/file",
                            },
                            "protocol": "s3",
                            "status": "available",
                        },
                    ],
                }
            ]
        }
    }
