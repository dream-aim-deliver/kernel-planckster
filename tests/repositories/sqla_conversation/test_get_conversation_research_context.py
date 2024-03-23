import random
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    GetConversationResearchContextDTO,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUser,
)


def test_get_research_context_from_conversation(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = random.choice(user_with_conv.research_contexts)
    researchContext_title = researchContext.title
    conversation = random.choice(researchContext.conversations)
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        get_conv_rc_DTO: GetConversationResearchContextDTO = conversation_repository.get_conversation_research_context(
            conversation_id=result.id
        )

    assert get_conv_rc_DTO.data is not None

    assert get_conv_rc_DTO.status == True
    assert get_conv_rc_DTO.errorCode == None
    assert get_conv_rc_DTO.data.title == researchContext_title


def test_error_get_research_context_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    get_conv_rc_DTO: GetConversationResearchContextDTO = conversation_repository.get_conversation_research_context(conversation_id=None)  # type: ignore

    assert get_conv_rc_DTO.status == False
    assert get_conv_rc_DTO.errorCode == -1
    assert get_conv_rc_DTO.errorMessage == "Conversation ID cannot be None"
    assert get_conv_rc_DTO.errorName == "Conversation ID not provided"
    assert get_conv_rc_DTO.errorType == "ConversationIdNotProvided"


def test_error_get_research_context_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    get_conv_rc_DTO: GetConversationResearchContextDTO = conversation_repository.get_conversation_research_context(
        conversation_id=irrealistic_ID
    )

    assert get_conv_rc_DTO.status == False
    assert get_conv_rc_DTO.errorCode == -1
    assert get_conv_rc_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert get_conv_rc_DTO.errorName == "Conversation not found"
    assert get_conv_rc_DTO.errorType == "ConversationNotFound"


def test_error_sqla_get_research_context_(
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
