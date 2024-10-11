from datetime import datetime
import random
import uuid
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    ListConversationSourcesDTO,
    NewMessageDTO,
    NewMessageContentDTO,
)
from lib.core.entity.models import BaseMessageContent, MessageSenderTypeEnum
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUserMessage,
    SQLAMessageBase,
    SQLAMessageContent,
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
            message_contents=[new_message_content],
            sender_type=MessageSenderTypeEnum.USER,
            thread_id=None,
        )

        assert dto.data is not None

        dto_message_id = dto.data.id

        sqla_message = session.query(SQLAUserMessage).filter_by(id=dto_message_id).first()

        assert sqla_message is not None

        sqla_message_id = sqla_message.id

        assert dto.status == True
        assert dto.errorCode == None
        assert dto.data.id == sqla_message_id

        dto_thread_id = dto.data.thread_id
        sqla_thread_id = sqla_message.thread_id

        assert dto_thread_id is not None
        assert dto_thread_id == sqla_thread_id

        dto_message_contents = dto.data.message_contents
        dto_message_content_id = dto_message_contents[0].id

        sqla_message_content = session.query(SQLAMessageContent).filter_by(id=dto_message_content_id).first()

        assert sqla_message_content is not None

        sqla_message_content_id = sqla_message_content.id

        assert dto_message_content_id == sqla_message_content_id
        assert dto_message_contents[0].content == sqla_message_content.content


def test_error_new_message_no_conversation_id(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.new_message(
        conversation_id=None,  # type: ignore
        message_contents=[BaseMessageContent(content="abc", content_type="text")],
        sender_type=MessageSenderTypeEnum.USER,
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
        conversation_id=1,
        message_contents=None,  # type: ignore
        sender_type=MessageSenderTypeEnum.USER,
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Message contents must be a list with at least one item"
    assert list_conv_srcs_DTO.errorName == "Message contents not provided"
    assert list_conv_srcs_DTO.errorType == "MessageContentsNotProvided"


def test_error_new_message_no_sqla_conversation(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.new_message(  # type: ignore
        conversation_id=irrealistic_ID,
        message_contents=[BaseMessageContent(content="abc", content_type="text")],
        sender_type=MessageSenderTypeEnum.USER,
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"
