from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from faker import Faker
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUser,
)


def test_add_conversation_to_research_context(
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    user_with_conv = fake_user_with_conversation
    user_sid = user_with_conv.sid
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    message_1 = conversation.messages[0]
    message_2 = conversation.messages[1]

    message_1_content = message_1.content
    message_2_content = message_2.content
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

        messages_contents = tuple([message.content for message in messages])
        index_msg_1 = messages_contents.index(message_1_content)
        index_msg_2 = messages_contents.index(message_2_content)

        assert message_1_content in messages_contents
        assert message_2_content in messages_contents
        assert messages[index_msg_1].type == message_1_type
        assert messages[index_msg_2].type == message_2_type

        assert messages[index_msg_1].conversation.research_context.user.sid == user_sid
