from datetime import datetime
import random
import uuid
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    ListConversationSourcesDTO,
    NewMessageDTO,
)
from lib.core.entity.models import MessageSenderTypeEnum
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUserMessage,
    SQLAClient,
)


def test_new_message_repository_function(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
    fake_client_with_source_data: SQLAClient,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    sqla_client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=sqla_client_with_conv.research_contexts,
    )
    researchContext = sqla_client_with_conv.research_contexts[0]

    sqla_client_with_sd = fake_client_with_source_data
    source_data = sqla_client_with_sd.source_data

    researchContext.source_data = source_data

    conversation = random.choice(researchContext.conversations)
    conversation.title = f"{conversation.title}-{uuid.uuid4()}"
    conversation_title = conversation.title

    new_message_content = fake.text()

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

        conv_id = None
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Test: Conversation not found")

        conv_id = result.id

        dto: NewMessageDTO = conversation_repository.new_message(
            conversation_id=conv_id,
            message_content=new_message_content,
            sender_type=MessageSenderTypeEnum.USER,
            timestamp=datetime.now(),
        )

        assert dto.data is not None

        dto_message_id = dto.data.id

        sqla_message = session.query(SQLAUserMessage).filter_by(id=dto_message_id).first()

        assert sqla_message is not None

        sqla_message_id = sqla_message.id

        assert dto.data is not None

        assert dto.status == True
        assert dto.errorCode == None
        assert dto.data.id == sqla_message_id
        assert dto.data.content == new_message_content


def test_error_new_message_no_conversation_id(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.new_message(
        conversation_id=None, message_content="abc", sender_type=MessageSenderTypeEnum.USER, timestamp=datetime.now()  # type: ignore
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_srcs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_srcs_DTO.errorType == "ConversationIdNotProvided"


def test_error_new_message_no_message_content(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.new_message(
        conversation_id=1, message_content=None, sender_type=MessageSenderTypeEnum.USER, timestamp=datetime.now()  # type: ignore
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Message content cannot be None"
    assert list_conv_srcs_DTO.errorName == "Message content not provided"
    assert list_conv_srcs_DTO.errorType == "MessageContentNotProvided"


def test_error_new_message_no_sqla_conversation(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.new_message(
        conversation_id=irrealistic_ID,
        message_content="abc",
        sender_type=MessageSenderTypeEnum.USER,
        timestamp=datetime.now(),
    )  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"
