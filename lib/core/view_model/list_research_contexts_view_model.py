from typing import List

from pydantic import Field
from lib.core.entity.models import ResearchContext
from lib.core.sdk.viewmodel import BaseViewModel


class ListResearchContextsViewModel(BaseViewModel):
    user_id: int = Field(description="User ID for which the research contexts are to be listed.")
    research_contexts: List[ResearchContext] = Field(description="List of research contexts for the user.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "research_contexts": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "name": "Research Context 1",
                            "description": "Research Context 1 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                        },
                        {
                            "id": 2,
                            "user_id": 1,
                            "name": "Research Context 2",
                            "description": "Research Context 2 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                        },
                    ],
                }
            ]
        }
    }
