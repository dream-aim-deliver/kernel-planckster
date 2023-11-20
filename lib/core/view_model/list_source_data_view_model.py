from typing import List

from pydantic import BaseModel, Field
from lib.core.sdk.viewmodel import BaseViewModel


class MPIScraperLFNViewModel(BaseModel):
    """
    Model for the LFNs scraped by the MPI Scraper. Contains the additional field "source_data_id" which is the ID of the source data coming from the database, and the "source_data_lfn" which is the lfn of the source data in the database.
    """

    source_data_id: int
    source_data_lfn: str
    protocol: str
    tracer_key: str
    job_id: int
    source: str
    relative_path: str


class ListSourceDataViewModel(BaseViewModel):
    """
    View Model for the List Source Data Feature. Represents all source data in the database if no knowledge_source_id was passed, or all source data for a given knowledge_source_id if it was provided as a parameter.
    """

    lfn_list: List[MPIScraperLFNViewModel] = Field(description="List of source data in the database.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "lfn_list": [
                        {
                            "source_data_id": 1,
                            "protocol": "s3",
                            "tracer_id": 1234567890,
                            "job_id": 1,
                            "source": "telegram",
                            "relative_path": "path/to/file",
                        },
                        {
                            "source_data_id": 2,
                            "protocol": "nas",
                            "tracer_id": 92839,
                            "job_id": 2,
                            "source": "twitter",
                            "relative_path": "path/to/file2",
                        },
                    ],
                }
            ]
        }
    }
