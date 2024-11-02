from typing import List

from pydantic import Field
from lib.core.entity.models import ResearchContext
from lib.core.sdk.viewmodel import BaseViewModel


class ListResearchContextsViewModel(BaseViewModel):
    client_id: int = Field(description="Client ID for which the research contexts are to be listed.")
    research_contexts: List[ResearchContext] = Field(description="List of research contexts for the client.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "client_id": 1,
                    "research_contexts": [
                        {
                            "id": 1,
                            "client_id": 1,
                            "name": "Research Context 1",
                            "description": "Research Context 1 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                            "external_id": "b52761eb-4e00-4431-b676-133bc02d6c77",
                        },
                        {
                            "id": 2,
                            "client_id": 1,
                            "name": "Research Context 2",
                            "description": "Research Context 2 Description",
                            "created_at": "2021-05-01T00:00:00",
                            "updated_at": "2021-05-01T00:00:00",
                            "external_id": "b52761eb-4e00-4431-b676-133bc02d6c77",
                        },
                    ],
                }
            ]
        }
    }
