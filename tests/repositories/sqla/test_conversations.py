from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from faker import Faker
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAClient,
)


def test_add_conversation_to_research_context(
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    client_with_conv = fake_client_with_conversation
    client_sub = client_with_conv.sub
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = client_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    assert len(conversation.messages) >= 2
    messages = conversation.messages[:2]
    assert set(messages) != {None}

    messages_contents = [piece.content for message in messages for piece in message.message_contents]
    messages_ids = [message.id for message in messages if message.id is not None]
    assert len(messages_ids) == 2

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        conv: SQLAConversation | None = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if conv is None:
            raise Exception("Conversation not found")

        queried_messages = [message for message in conv.messages if message.id in messages_ids]

        assert set(messages_ids) == set([message.id for message in queried_messages])

        queried_messages_contents = [
            piece.content for message in queried_messages for piece in message.message_contents
        ]

        assert set(messages_contents) == set(queried_messages_contents)

        assert queried_messages[0].conversation.research_context.client.sub == client_sub
