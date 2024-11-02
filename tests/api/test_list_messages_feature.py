import random
from typing import Tuple
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
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAAgentMessage,
    SQLAConversation,
    SQLAResearchContext,
    SQLAClient,
    SQLAUserMessage,
)


def test_list_messages_usecase(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
    fake_message_pair: Tuple[SQLAUserMessage, SQLAAgentMessage],
) -> None:
    usecase: ListMessagesUseCase = app_initialization_container.list_messages_feature.usecase()

    assert usecase is not None

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = random.choice(client_with_conv.research_contexts)
    conversation = random.choice(researchContext.conversations)
    # Make it unique to query it later
    conversation_title = f"{conversation.title}-{uuid.uuid4()}"
    conversation.title = conversation_title

    messages = conversation.messages
    messages_contents = tuple([piece.content for message in messages for piece in message.message_contents])

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
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

        queried_messages_contents = [piece.content for msg in response.message_list for piece in msg.message_contents]

        assert set(queried_messages_contents) == set(messages_contents)

    with db_session() as session:
        conv = session.query(SQLAConversation).filter_by(title=conversation_title).first()
        assert conv is not None

        new_messages = fake_message_pair
        new_messages_contents = tuple([piece.content for message in new_messages for piece in message.message_contents])
        messages_contents += new_messages_contents

        for new_message in new_messages:
            conv.messages.append(new_message)

        conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conv = session.query(SQLAConversation).filter_by(title=conversation_title).first()
        assert queried_conv is not None

        request = ListMessagesRequest(conversation_id=queried_conv.id)
        response = usecase.execute(request=request)

        assert response is not None

        assert isinstance(response, ListMessagesResponse)
        assert response.message_list is not None
        assert len(response.message_list) != 0

        queried_messages_contents = [piece.content for msg in response.message_list for piece in msg.message_contents]

        assert set(queried_messages_contents) == set(messages_contents)


def test_list_messages_controller(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    controller: ListMessagesController = app_initialization_container.list_messages_feature.controller()

    assert controller is not None

    client_with_conv = fake_client_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=client_with_conv.research_contexts,
    )

    researchContext = random.choice(client_with_conv.research_contexts)
    conversation = random.choice(researchContext.conversations)
    conversation_title = conversation.title

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
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
        external_id=str(uuid.uuid4()),
        conversations=[conv],
    )

    client = SQLAClient(
        sub=fake.name(),
        research_contexts=[rc],
    )

    llm = SQLALLM(llm_name=fake.name(), research_contexts=client.research_contexts)

    with db_session() as session:
        client.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

        parameters = ListMessagesControllerParameters(conversation_id=queried_conversation.id)

        view_model: ListMessagesViewModel | None = controller.execute(parameters=parameters)

        assert view_model is not None
        assert len(view_model.message_list) == 0
        assert view_model.status is True
