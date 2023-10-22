from faker import Faker
from lib.core.dto.conversation_repository_dto import ConversationDTO
from lib.infrastructure.config.containers import Container
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAResearchContext,
    SQLAUser,
)
from tests.conftest import conversation


def test_create_new_conversation(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    researchContext = user_with_conv.research_contexts[0]

    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=[researchContext],
    )

    conversation = fake_conversation
    conversation_title = conversation.title

    with db_session() as session:
        session.add(researchContext)
        session.commit()
        convDTO: ConversationDTO = conversation_repository.new_conversation(
            research_context_id=researchContext.id, conversation_title=conversation_title
        )
        session.commit()

    id = None
    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Conversation not found")

        id = result.id

    assert convDTO.status == True
    assert convDTO.errorCode == None
    assert isinstance(convDTO.conversation_id, int)


def test_error_new_conversation_none_research_context_id(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    convDTO: ConversationDTO = conversation_repository.new_conversation(research_context_id=None, conversation_title="test")  # type: ignore

    assert convDTO.status == False
    assert convDTO.errorCode == -1
    assert convDTO.errorMessage == "Research Context ID cannot be None"
    assert convDTO.errorName == "Research Context ID not provided"
    assert convDTO.errorType == "ResearchContextIdNotProvided"


def test_error_new_conversation_none_conversation_title(app_container: Container, db_session: TDatabaseFactory) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    convDTO: ConversationDTO = conversation_repository.new_conversation(research_context_id=1, conversation_title=None)  # type: ignore

    assert convDTO.status == False
    assert convDTO.errorCode == -1
    assert convDTO.errorMessage == "Conversation title cannot be None"
    assert convDTO.errorName == "Conversation title not provided"
    assert convDTO.errorType == "ConversationTitleNotProvided"


def test_error_new_conversation_none_sqla_research_context(
    app_container: Container, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    convDTO: ConversationDTO = conversation_repository.new_conversation(
        research_context_id=irrealistic_ID, conversation_title="test"
    )

    assert convDTO.status == False
    assert convDTO.errorCode == -1
    assert convDTO.errorMessage == f"Research Context with ID {irrealistic_ID} not found in the database."
    assert convDTO.errorName == "Research Context not found"
    assert convDTO.errorType == "ResearchContextNotFound"


def test_error_sqla_new_conversation_(
    app_container: Container,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_user_with_conversation: SQLAUser,
) -> None:
    """
    NOTE: not sure how to test the case where the error comes from SQLA
    """
    pass