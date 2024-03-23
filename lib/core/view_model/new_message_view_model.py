from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class NewMessageViewModel(BaseViewModel):
    """
    View Model for the New Message Feature.
    """

    message_id: int = Field(description="ID of the newly created message.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message_id": 1,
                }
            ]
        }
    }
