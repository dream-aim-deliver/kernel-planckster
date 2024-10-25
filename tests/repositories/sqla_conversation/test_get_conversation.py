import random
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    GetConversationDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAClient,
)


def test_get_conversation(
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
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=result.id)

    assert get_conv_DTO.status == True
    assert get_conv_DTO.errorCode == None
    assert get_conv_DTO.data is not None
    assert get_conv_DTO.data.title == conversation_title


def test_error_get_conversation_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=None)

    assert get_conv_DTO.status == False
    assert get_conv_DTO.errorCode == -1
    assert get_conv_DTO.errorMessage == "Conversation ID cannot be None"
    assert get_conv_DTO.errorName == "Conversation ID not provided"
    assert get_conv_DTO.errorType == "ConversationIdNotProvided"


def test_error_get_conversation_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=irrealistic_ID)

    assert get_conv_DTO.status == False
    assert get_conv_DTO.errorCode == -1
    assert get_conv_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert get_conv_DTO.errorName == "Conversation not found"
    assert get_conv_DTO.errorType == "ConversationNotFound"
