import random
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    UpdateConversationDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAClient,
)


def test_update_conversation(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
    fake_conversation: SQLAConversation,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    id = None
    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
        session.commit()

        researchContext = random.choice(client_with_conv.research_contexts)
        conversation = random.choice(researchContext.conversations)
        conversation_id = conversation.id
        conversation_title = conversation.title

    with db_session() as session:
        new_conversation_title = fake.name()

        # result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        # assert result is not None

        # id = result.id
        conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
            conversation_id=conversation_id, conversation_title=new_conversation_title
        )
        assert conv_DTO.status == True
        assert conv_DTO.conversation_id == conversation_id

    with db_session() as session:
        queried_conversation = session.get(SQLAConversation, conversation_id)
        assert queried_conversation is not None

        assert queried_conversation.title == new_conversation_title
        assert queried_conversation.title != conversation_title
        assert queried_conversation.id == conversation_id


def test_error_update_conversation_none_research_context_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
        conversation_id=None, conversation_title="test"
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation ID cannot be None"
    assert conv_DTO.errorName == "Conversation ID not provided"
    assert conv_DTO.errorType == "ConversationIdNotProvided"


def test_error_update_conversation_none_conversation_title(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
        conversation_id=1, conversation_title=None
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation title cannot be None"
    assert conv_DTO.errorName == "Conversation title not provided"
    assert conv_DTO.errorType == "ConversationTitleNotProvided"


def test_error_update_conversation_conversation_id_not_found(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
        conversation_id=irrealistic_ID, conversation_title="test"
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert conv_DTO.errorName == "Conversation not found"
    assert conv_DTO.errorType == "ConversationNotFound"
