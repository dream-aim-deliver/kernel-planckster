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

    message_1 = conversation.messages[0]
    message_2 = conversation.messages[1]

    message_1_contents = message_1.message_contents
    message_2_contents = message_2.message_contents
    message_1_id = message_1.id
    message_2_id = message_2.id
    message_1_type = message_1.type
    message_2_type = message_2.type

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        conv: SQLAConversation | None = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if conv is None:
            raise Exception("Conversation not found")

        messages = conv.messages

        messages_contents = tuple([piece.content for message in messages for piece in message.message_contents])
        # index_msg_1 = messages_contents.index(message_1_contents)
        # index_msg_2 = messages_contents.index(message_2_contents)
        message_1_contents_extra = [content for content in message_1_contents if content not in messages_contents]
        message_2_contents_extra = [content for content in message_2_contents if content not in messages_contents]
        missing_content = [
            content for content in messages_contents if content not in message_1_contents + message_2_contents
        ]

        # assert message_1_contents in messages_contents
        # assert message_2_contents in messages_contents
        assert message_1_contents_extra == []
        assert message_2_contents_extra == []
        assert missing_content == []
        # assert messages[index_msg_1].type == message_1_type
        # assert messages[index_msg_2].type == message_2_type
        message_ids = [message.id for message in messages]
        assert message_1_id in message_ids
        assert message_2_id in message_ids

        # assert messages[index_msg_1].conversation.research_context.client.sub == client_sub
        assert message_1.conversation.research_context.client.sub == client_sub
