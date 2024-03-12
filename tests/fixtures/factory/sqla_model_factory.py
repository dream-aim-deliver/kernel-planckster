from abc import ABC, abstractmethod
from typing import Any, Set
from faker import Faker

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    ModelBase,
    SQLAConversation,
    SQLAMessageQuery,
    SQLAResearchContext,
    SQLAUser,
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
        user_name = fake.name()
        research_context_name = f"Research Context {user_name} {fake.name()}"
        research_context_description = fake.text()
        conversation_name = f"Conversation {user_name} {fake.name()}"
        sqla_user = SQLAUser(sid=user_name)
        sqla_research_context = SQLAResearchContext(
            title=research_context_name,
            description=research_context_description,
            user=sqla_user,
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
            sqla_message_query = SQLAMessageQuery(
                content=fake.text(max_nb_chars=70)[:-1] + "?",
                timestamp=dt1,
                conversation=sqla_conversation,
            )
            self.session.add(sqla_message_query)
            self.session.commit()
            self.managed_sqla_model_objects.add(sqla_message_query)
        return sqla_conversation
