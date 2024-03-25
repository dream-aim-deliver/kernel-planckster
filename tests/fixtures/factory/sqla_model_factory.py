from abc import ABC, abstractmethod
from typing import Any, Set
from faker import Faker

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    ModelBase,
    SQLAConversation,
    SQLAUserMessage,
    SQLAResearchContext,
    SQLAClient,
)
from sqlalchemy.orm import Session


class SQLATemporaryModelFactory:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.managed_sqla_model_objects: Set[ModelBase] = set()

    def __enter__(self) -> Any:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        for obj in self.managed_sqla_model_objects:
            self.session.delete(obj)
        self.session.commit()
        self.managed_sqla_model_objects.clear()

    def make_conversation(self, n_messages: int) -> SQLAConversation:
        fake = Faker().unique
        client_name = fake.name()
        research_context_name = f"Research Context {client_name} {fake.name()}"
        research_context_description = fake.text()
        conversation_name = f"Conversation {client_name} {fake.name()}"
        sqla_client = SQLAClient(sub=client_name)
        sqla_research_context = SQLAResearchContext(
            title=research_context_name,
            description=research_context_description,
            client=sqla_client,
        )
        llm = SQLALLM(
            llm_name=fake.name(),
            research_contexts=[sqla_research_context],
        )

        sqla_conversation = SQLAConversation(
            title=conversation_name,
            research_context=sqla_research_context,
        )
        for x in range(n_messages):
            dt1 = fake.date_time_between(start_date="-8y", end_date="-1m")
            sqla_client_message = SQLAUserMessage(
                content=fake.text(max_nb_chars=70)[:-1] + "?",
                timestamp=dt1,
                conversation=sqla_conversation,
            )
            self.session.add(sqla_client_message)
            self.session.commit()
            self.managed_sqla_model_objects.add(sqla_client_message)
        return sqla_conversation
