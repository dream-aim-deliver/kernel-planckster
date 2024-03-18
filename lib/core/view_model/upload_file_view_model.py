from typing import Optional
from pydantic import Field
from lib.core.entity.models import LFN
from lib.core.sdk.viewmodel import BaseViewModel


class UploadFileViewModel(BaseViewModel):
    """
    View Model for the Upload File Feature.
    """

    lfn: Optional[LFN] = Field(description="The Logical File Name of the uploaded file.")
    signed_url: str = Field(description="The signed URL to upload the file.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "lfn": "s3://localhost:9000/bucket1/tracer_id/user/1/file1.txt",
                    "signed_url": "auth1_string",
                }
            ]
        }
    }
