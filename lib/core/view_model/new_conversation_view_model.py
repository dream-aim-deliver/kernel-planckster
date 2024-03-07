from pydantic import Field
from lib.core.sdk.viewmodel import BaseViewModel


class NewConversationViewModel(BaseViewModel):
    """
    View Model for the New Conversation Feature.
    """

    conversation_id: int = Field(description="ID of the newly created conversation.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": 1,
                }
            ]
        }
    }
