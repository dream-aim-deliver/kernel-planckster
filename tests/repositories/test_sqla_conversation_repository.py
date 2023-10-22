from faker import Faker
from lib.core.dto.conversation_repository_dto import ConversationDTO, GetConversationResearchContextDTO
from lib.infrastructure.config.containers import Container
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAResearchContext,
    SQLAUser,
)
from tests.conftest import conversation


############
# New Conversation Feature
############


def test_create_new_conversation(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = user_with_conv.research_contexts[0]

    conversation = fake_conversation
    conversation_title = conversation.title

    with db_session() as session:
        session.add(researchContext)
        session.commit()
        conv_DTO: ConversationDTO = conversation_repository.new_conversation(
            research_context_id=researchContext.id, conversation_title=conversation_title
        )
        session.commit()

    assert conv_DTO.status == True
    assert conv_DTO.errorCode == None
    assert isinstance(conv_DTO.conversation_id, int)


def test_error_new_conversation_none_research_context_id(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    conv_DTO: ConversationDTO = conversation_repository.new_conversation(research_context_id=None, conversation_title="test")  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Research Context ID cannot be None"
    assert conv_DTO.errorName == "Research Context ID not provided"
    assert conv_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_new_conversation_none_conversation_title(app_container: Container, db_session: TDatabaseFactory) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    conv_DTO: ConversationDTO = conversation_repository.new_conversation(research_context_id=1, conversation_title=None)  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation title cannot be None"
    assert conv_DTO.errorName == "Conversation title not provided"
    assert conv_DTO.errorType == "ConversationTitleNotProvided"


def test_error_new_conversation_none_sqla_research_context(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    conv_DTO: ConversationDTO = conversation_repository.new_conversation(
        research_context_id=irrealistic_ID, conversation_title="test"
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == f"Research Context with ID {irrealistic_ID} not found in the database."
    assert conv_DTO.errorName == "Research Context not found"
    assert conv_DTO.errorType == "ResearchContextNotFound"


def test_error_sqla_new_conversation_(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    """
    TODO: not sure how to test the case where the error comes from SQLA
    """
    pass


############
# Get Conversation Research Context Feature
############


def test_get_research_context_from_conversation(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = user_with_conv.research_contexts[0]
    researchContext_title = researchContext.title

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Conversation not found")

        get_conv_rc_DTO: GetConversationResearchContextDTO = conversation_repository.get_conversation_research_context(
            conversation_id=result.id
        )

    if get_conv_rc_DTO.data is None:
        raise Exception("Research Context of Conversation not found")

    assert get_conv_rc_DTO.status == True
    assert get_conv_rc_DTO.errorCode == None
    assert get_conv_rc_DTO.data.title == researchContext_title


def test_error_get_research_context_none_conversation_id(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    conv_DTO: ConversationDTO = conversation_repository.get_conversation_research_context(conversation_id=None)  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation ID cannot be None"
    assert conv_DTO.errorName == "Conversation ID not provided"
    assert conv_DTO.errorType == "ConversationIdNotProvided"


def test_error_get_research_context_none_sqla_conversation(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    conv_DTO: ConversationDTO = conversation_repository.get_conversation_research_context(conversation_id=irrealistic_ID)  # type: ignore

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert conv_DTO.errorName == "Conversation not found"
    assert conv_DTO.errorType == "ConversationNotFound"


def test_error_sqla_get_research_context_(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    """
    TODO: not sure how to test the case where the error comes from SQLA
    """
    pass
