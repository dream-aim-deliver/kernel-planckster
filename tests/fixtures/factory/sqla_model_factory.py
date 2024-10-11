from abc import ABC, abstractmethod
from typing import Any, Set
from faker import Faker

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    ModelBase,
    SQLAConversation,
    SQLAUserMessage,
    SQLAMessageContent,
    SQLAResearchContext,
    SQLAClient,
)
from lib.core.entity.models import MessageContentTypeEnum
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
            sqla_message_content = SQLAMessageContent(
                content=fake.text(max_nb_chars=70)[:-1] + "?",
                content_type=MessageContentTypeEnum.TEXT,
                message_base=SQLAUserMessage(
                    conversation=sqla_conversation,
                    thread_id=x,
                ),
            )

            self.session.add(sqla_message_content)
            self.session.commit()
            self.managed_sqla_model_objects.add(sqla_message_content)
        return sqla_conversation
