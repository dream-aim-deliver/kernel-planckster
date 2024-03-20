from typing import Optional
from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.viewmodel import BaseViewModel


class GetClientDataForUploadViewModel(BaseViewModel):
    """
    View Model for the Get Client Data For Upload Feature.
    """

    lfn: Optional[LFN] = Field(description="The Logical File Name of the file that can be uploaded.")
    signed_url: str = Field(description="The signed URL to upload the file.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "lfn": '{"protocol":"s3", "tracer_id":"user_uploads", "job_id":20240318212314, "source":"user", "relative_path":"test_file-22af0b93dcb943d8b7105126ef1b1229-sdamarker.txt"}',
                    "signed_url": "auth1_string",
                }
            ]
        }
    }
