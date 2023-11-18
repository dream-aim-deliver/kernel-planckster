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
    SQLAUser,
)


def test_update_conversation(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
    fake_conversation: SQLAConversation,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    rand_int_1 = random.randint(0, len(user_with_conv.research_contexts) - 1)
    researchContext = user_with_conv.research_contexts[rand_int_1]

    rand_int_2 = random.randint(0, len(researchContext.conversations) - 1)
    conversation = researchContext.conversations[rand_int_2]
    conversation_title = conversation.title

    new_conversation_title = fake.name()

    id = None
    with db_session() as session:
        user_with_conv.save(session=session, flush=True)

        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        id = result.id
        conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
            conversation_id=id, conversation_title=new_conversation_title
        )

        old_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        new_conversation = session.query(SQLAConversation).filter_by(id=conv_DTO.conversation_id).first()

        assert new_conversation is not None

    assert conv_DTO.conversation_id is not None

    assert old_conversation == None
    assert conv_DTO.status == True
    assert conv_DTO.errorCode == None
    assert conv_DTO.conversation_id == id
    assert new_conversation.title == new_conversation_title


def test_error_update_conversation_none_research_context_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(conversation_id=None, conversation_title="test")  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation ID cannot be None"
    assert conv_DTO.errorName == "Conversation ID not provided"
    assert conv_DTO.errorType == "ConversationIdNotProvided"


def test_error_update_conversation_none_conversation_title(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(conversation_id=1, conversation_title=None)  # type: ignore

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
