import random
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    NewConversationDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUser,
)


def test_create_new_conversation(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    rand_int_1 = random.randint(0, len(user_with_conv.research_contexts) - 1)
    researchContext = user_with_conv.research_contexts[rand_int_1]

    conversation = fake_conversation
    conversation_title = conversation.title

    with db_session() as session:
        session.add(researchContext)
        session.commit()
        conv_DTO: NewConversationDTO = conversation_repository.new_conversation(
            research_context_id=researchContext.id, conversation_title=conversation_title
        )

        new_conv = session.query(SQLAConversation).filter_by(title=conversation_title).first()
        assert new_conv is not None

    assert conv_DTO.status == True
    assert conv_DTO.errorCode == None
    assert conv_DTO.conversation_id == new_conv.id


def test_error_new_conversation_none_research_context_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: NewConversationDTO = conversation_repository.new_conversation(research_context_id=None, conversation_title="test")  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Research Context ID cannot be None"
    assert conv_DTO.errorName == "Research Context ID not provided"
    assert conv_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_new_conversation_none_conversation_title(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    conv_DTO: NewConversationDTO = conversation_repository.new_conversation(research_context_id=1, conversation_title=None)  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation title cannot be None"
    assert conv_DTO.errorName == "Conversation title not provided"
    assert conv_DTO.errorType == "ConversationTitleNotProvided"


def test_error_new_conversation_none_sqla_research_context(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    conv_DTO: NewConversationDTO = conversation_repository.new_conversation(
        research_context_id=irrealistic_ID, conversation_title="test"
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == f"Research Context with ID {irrealistic_ID} not found in the database."
    assert conv_DTO.errorName == "Research Context not found"
    assert conv_DTO.errorType == "ResearchContextNotFound"


def test_error_sqla_new_conversation_(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    """
    TODO: not sure how to test the case where the error comes from SQLA
    """
    pass
