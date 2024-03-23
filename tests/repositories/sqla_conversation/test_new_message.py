from datetime import datetime
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
    SQLAKnowledgeSource,
    SQLAUserMessage,
    SQLAUser,
)


def test_new_message_repository_function(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )
    researchContext = user_with_conv.research_contexts[0]

    ks_with_sd = fake_knowledge_source_with_source_data
    source_data = ks_with_sd.source_data
    source_data_names = tuple(source.name for source in source_data)
    source_data_lfns = tuple(source.lfn for source in source_data)

    researchContext.source_data = source_data

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    new_message_content = fake.text()

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    id = None
    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Test: Conversation not found")

        id = result.id

        send_msg_to_conv_DTO: NewMessageDTO = conversation_repository.new_message(
            conversation_id=id,
            message_content=new_message_content,
            sender_type=MessageSenderTypeEnum.USER,
            timestamp=datetime.now(),
        )

        assert send_msg_to_conv_DTO.data is not None

        dto_user_message_id = send_msg_to_conv_DTO.data.id

        sqla_user_message = session.query(SQLAUserMessage).filter_by(id=dto_user_message_id).first()

        assert sqla_user_message is not None

        sqla_user_message_id = sqla_user_message.id

    assert send_msg_to_conv_DTO.data is not None

    assert send_msg_to_conv_DTO.status == True
    assert send_msg_to_conv_DTO.errorCode == None
    assert send_msg_to_conv_DTO.data.id == sqla_user_message_id
    assert send_msg_to_conv_DTO.data.content == new_message_content


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
