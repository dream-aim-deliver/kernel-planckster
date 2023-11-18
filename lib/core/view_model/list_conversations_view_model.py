from typing import List

from pydantic import Field
from lib.core.entity.models import Conversation
from lib.core.sdk.viewmodel import BaseViewModel


class ListConversationsViewModel(BaseViewModel):
    """
    View Model for the List Conversations Feature. Represents all conversations in a given research context.
    """

    research_context_id: int = Field(description="Research context id for which the conversations are to be listed.")
    conversations: List[Conversation] = Field(description="List of conversations in the research context.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "research_context_id": 1,
                    "conversations": [
                        {
                            "id": 1,
                            "research_context_id": 1,
                            "name": "Conversation 1",
                            "description": "Conversation 1 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                        },
                        {
                            "id": 2,
                            "research_context_id": 1,
                            "name": "Conversation 2",
                            "description": "Conversation 2 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                        },
                    ],
                }
            ]
        }
    }
