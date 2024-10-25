import random
from faker import Faker
from lib.core.dto.research_context_repository_dto import NewResearchContextConversationDTO

from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAClient,
)


def test_create_new_conversation(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_conversation: SQLAConversation,
    fake_client_with_conversation: SQLAClient,
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = random.choice(client_with_conv.research_contexts)

    conversation = fake_conversation
    conversation_title = conversation.title

    with db_session() as session:
        session.add(researchContext)
        session.commit()
        conv_DTO: NewResearchContextConversationDTO = research_context_repository.new_conversation(
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
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    conv_DTO: NewResearchContextConversationDTO = research_context_repository.new_conversation(
        research_context_id=None, conversation_title="test"
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Research Context ID cannot be None"
    assert conv_DTO.errorName == "Research Context ID not provided"
    assert conv_DTO.errorType == "ResearchContextIdNotProvided"


def test_error_new_conversation_none_conversation_title(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    conv_DTO: NewResearchContextConversationDTO = research_context_repository.new_conversation(
        research_context_id=1, conversation_title=None
    )

    assert conv_DTO.status == False
    assert conv_DTO.errorCode == -1
    assert conv_DTO.errorMessage == "Conversation title cannot be None"
    assert conv_DTO.errorName == "Conversation title not provided"
    assert conv_DTO.errorType == "ConversationTitleNotProvided"


def test_error_new_conversation_none_sqla_research_context(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    research_context_repository = app_initialization_container.sqla_research_context_repository()

    irrealistic_ID = 99999999
    conv_DTO: NewResearchContextConversationDTO = research_context_repository.new_conversation(
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
    fake_client_with_conversation: SQLAClient,
) -> None:
    """
    TODO: not sure how to test the case where the error comes from SQLA
    """
    pass
