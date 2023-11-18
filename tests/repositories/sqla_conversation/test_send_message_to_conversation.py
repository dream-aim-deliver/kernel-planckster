from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    ListConversationSourcesDTO,
    SendMessageToConversationDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAKnowledgeSource,
    SQLAMessageQuery,
    SQLAUser,
)


def test_send_message_to_conversation(
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

        send_msg_to_conv_DTO: SendMessageToConversationDTO = conversation_repository.send_message_to_conversation(
            conversation_id=id, message_content=new_message_content
        )

        assert send_msg_to_conv_DTO.data is not None

        dto_message_query_id = send_msg_to_conv_DTO.data.id

        sqla_message_query = session.query(SQLAMessageQuery).filter_by(id=dto_message_query_id).first()

        assert sqla_message_query is not None

        sqla_message_query_id = sqla_message_query.id

    assert send_msg_to_conv_DTO.data is not None

    assert send_msg_to_conv_DTO.status == True
    assert send_msg_to_conv_DTO.errorCode == None
    assert send_msg_to_conv_DTO.data.id == sqla_message_query_id
    assert send_msg_to_conv_DTO.data.content == new_message_content


def test_error_send_message_to_conversation_no_conversation_id(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=None, message_content="abc")  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_srcs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_srcs_DTO.errorType == "ConversationIdNotProvided"


def test_error_send_message_to_conversation_no_message_content(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=1, message_content=None)  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Message content cannot be None"
    assert list_conv_srcs_DTO.errorName == "Message content not provided"
    assert list_conv_srcs_DTO.errorType == "MessageContentNotProvided"


def test_error_send_message_to_conversation_no_sqla_conversation(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=irrealistic_ID, message_content="abc")  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"
