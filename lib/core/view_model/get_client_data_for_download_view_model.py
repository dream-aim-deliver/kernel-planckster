from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class GetClientDataForDownloadViewModel(BaseViewModel):
    """
    View Model for the Download File Feature.
    """

    signed_url: str = Field(description="The signed URL to download the file.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": True,
                    "code": 200,
                    "signed_url": "auth1_string",
                }
            ]
        }
    }
