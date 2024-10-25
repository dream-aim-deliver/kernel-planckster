import random
import uuid
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    ListConversationMessagesDTO,
)
from lib.core.entity.models import TMessageBase
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAClient,
)


def test_list_conversation_messages(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = random.choice(client_with_conv.research_contexts)
    conversation = random.choice(researchContext.conversations)
    # Make it unique to query it later
    conversation_title = f"{conversation.title}-{uuid.uuid4()}"
    conversation.title = conversation_title

    messages = conversation.messages
    messages_contents = tuple([piece.content for message in messages for piece in message.message_contents])

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        list_conv_msgs_DTO: ListConversationMessagesDTO[TMessageBase] = (  # type: ignore
            conversation_repository.list_conversation_messages(conversation_id=result.id)
        )

    assert list_conv_msgs_DTO.data is not None

    assert list_conv_msgs_DTO.status == True
    assert list_conv_msgs_DTO.errorCode == None
    assert isinstance(list_conv_msgs_DTO.data, list)

    for message in list_conv_msgs_DTO.data:
        assert message is not None
        message_contents = message.message_contents
        assert message_contents is not None

        for piece in message_contents:
            assert piece.content in messages_contents


def test_error_list_conversation_messages_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    list_conv_msgs_DTO: ListConversationMessagesDTO = conversation_repository.list_conversation_messages(conversation_id=None)  # type: ignore

    assert list_conv_msgs_DTO.status == False
    assert list_conv_msgs_DTO.errorCode == -1
    assert list_conv_msgs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_msgs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_msgs_DTO.errorType == "ConversationIdNotProvided"


def test_error_list_conversation_messages_conversation_id_not_found(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_msgs_DTO: ListConversationMessagesDTO = conversation_repository.list_conversation_messages(conversation_id=irrealistic_ID)  # type: ignore

    assert list_conv_msgs_DTO.status == False
    assert list_conv_msgs_DTO.errorCode == -1
    assert list_conv_msgs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_msgs_DTO.errorName == "Conversation not found"
    assert list_conv_msgs_DTO.errorType == "ConversationNotFound"
