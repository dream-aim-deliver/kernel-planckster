import random
import uuid
from faker import Faker
from lib.core.usecase.list_messages_usecase import ListMessagesUseCase
from lib.core.usecase_models.list_messages_usecase_models import ListMessagesRequest, ListMessagesResponse
from lib.core.view_model.list_messages_view_model import ListMessagesViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_messages_controller import (
    ListMessagesController,
    ListMessagesControllerParameters,
)
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAConversation, SQLAResearchContext, SQLAUser


def test_list_messages_usecase(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    usecase: ListMessagesUseCase = app_initialization_container.list_messages_feature.usecase()

    assert usecase is not None

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = random.choice(user_with_conv.research_contexts)
    conversation = random.choice(researchContext.conversations)
    # Make it unique to query it later
    conversation_title = f"{conversation.title}-{uuid.uuid4()}"
    conversation.title = conversation_title

    messages = conversation.messages
    message_contents = tuple([message.content for message in messages])

    with db_session() as session:
        user_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

        request = ListMessagesRequest(conversation_id=queried_conversation.id)
        response = usecase.execute(request=request)

        assert response is not None
        assert isinstance(response, ListMessagesResponse)
        assert response.message_list is not None
        assert len(response.message_list) != 0

        queried_messages_contents = [msg.content for msg in response.message_list]

        assert set(queried_messages_contents) == set(message_contents)


def test_list_messages_controller(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    controller: ListMessagesController = app_initialization_container.list_messages_feature.controller()

    assert controller is not None

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )

    researchContext = random.choice(user_with_conv.research_contexts)
    conversation = random.choice(researchContext.conversations)
    conversation_title = conversation.title

    with db_session() as session:
        user_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

    parameters = ListMessagesControllerParameters(conversation_id=queried_conversation.id)

    view_model: ListMessagesViewModel | None = controller.execute(parameters=parameters)

    assert view_model is not None
    assert view_model.message_list is not None


def test_conversation_without_messages(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
) -> None:
    controller: ListMessagesController = app_initialization_container.list_messages_feature.controller()

    assert controller is not None

    conversation_title = f"{fake.name()}-{uuid.uuid4()}"
    conv = SQLAConversation(
        title=conversation_title,
        messages=[],
    )

    rc = SQLAResearchContext(
        title=fake.name(),
        description=fake.text(),
        conversations=[conv],
    )

    user = SQLAUser(
        sid=fake.name(),
        research_contexts=[rc],
    )

    llm = SQLALLM(llm_name=fake.name(), research_contexts=user.research_contexts)

    with db_session() as session:
        user.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

        parameters = ListMessagesControllerParameters(conversation_id=queried_conversation.id)

        view_model: ListMessagesViewModel | None = controller.execute(parameters=parameters)

        assert view_model is not None
        assert len(view_model.message_list) == 0
        assert view_model.status is True
