from typing import Dict, List

from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class ListSourceDataViewModel(BaseViewModel):
    """
    View Model for the List Source Data Feature. Represents all source data in the database if no knowledge_source_id was passed, or all source data for a given knowledge_source_id if it was provided as a parameter.
    """

    lfn_list: List[Dict[str, str]] = Field(description="List of source data in the database.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "lfn_list": [
                        {
                            "protocol": "S3",
                            "tracer_id": "1234567890",
                            "job_id": "1",
                            "source": "TELEGRAM",
                            "relative_path": "path/to/file",
                        },
                        {
                            "protocol": "NAS",
                            "tracer_id": "92839",
                            "job_id": "2",
                            "source": "Twitter",
                            "relative_path": "path/to/file2",
                        },
                    ],
                }
            ]
        }
    }
