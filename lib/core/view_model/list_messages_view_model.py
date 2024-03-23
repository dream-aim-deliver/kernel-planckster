from typing import List, Optional

from pydantic import Field
from lib.core.entity.models import MessageBase
from lib.core.sdk.viewmodel import BaseViewModel


class ListMessagesViewModel(BaseViewModel):
    """
    View Model for the List Messages Feature. Represents all messages in the database for a given conversation.
    """

    message_list: List[str] = Field(description="List of all messages in the database for a given conversation.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message_list": [
                        {
                            "created_at": "2021-01-01T00:00:00Z",
                            "updated_at": "2021-01-01T00:00:00Z",
                            "deleted": False,
                            "deleted_at": None,
                            "timestamp": "2021-01-01T00:00:00Z",
                            "id": 1,
                            "conversation_id": 1,
                            "content": "Hello, world!",
                            "sender": "user_1",
                            "sender_type": "user",
                        },
                        {
                            "created_at": "2021-01-01T00:00:01Z",
                            "updated_at": "2021-01-01T00:00:01Z",
                            "deleted": False,
                            "deleted_at": None,
                            "timestamp": "2021-01-01T00:00:01Z",
                            "id": 2,
                            "conversation_id": 1,
                            "content": "Hi, there!",
                            "sender": "llama2",
                            "sender_type": "agent",
                        },
                    ],
                }
            ]
        }
    }
