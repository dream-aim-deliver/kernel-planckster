from datetime import datetime
import random
import uuid
from faker import Faker
from lib.core.entity.models import MessageSenderTypeEnum
from lib.core.usecase.new_message_usecase import NewMessageUseCase
from lib.core.usecase_models.new_message_usecase_models import NewMessageRequest, NewMessageResponse
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_message_controller import NewMessageController, NewMessageControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAAgentMessage,
    SQLAConversation,
    SQLAMessageBase,
    SQLAClient,
    SQLAUserMessage,
)


def test_new_message_usecase(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    usecase: NewMessageUseCase = app_initialization_container.new_message_feature.usecase()

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

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

        message_content = f"{fake.text()}-{uuid.uuid4()}"
        timestamp = fake.unix_time()
        sender_type = random.choice([p.value for p in MessageSenderTypeEnum])

        request = NewMessageRequest(
            conversation_id=queried_conversation.id,
            message_content=message_content,
            sender_type=sender_type,
            unix_timestamp=timestamp,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert isinstance(response, NewMessageResponse)

        assert response.message_id is not None

        queried_message = session.get(SQLAMessageBase, response.message_id)

        assert queried_message is not None
        assert queried_message.content == message_content
        assert queried_message.timestamp == datetime.fromtimestamp(timestamp)

        if isinstance(queried_message, SQLAAgentMessage):
            assert sender_type == MessageSenderTypeEnum.AGENT.value
        elif isinstance(queried_message, SQLAUserMessage):
            assert sender_type == MessageSenderTypeEnum.USER.value
        else:
            assert False


def test_new_message_controller(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_conversation: SQLAClient,
) -> None:
    controller: NewMessageController = app_initialization_container.new_message_feature.controller()

    assert controller is not None

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

    with db_session() as session:
        client_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        queried_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert queried_conversation is not None

        message_content = f"{fake.text()}-{uuid.uuid4()}"
        timestamp = fake.unix_time()
        sender_type = random.choice([p.value for p in MessageSenderTypeEnum])

        controller_parameters = NewMessageControllerParameters(
            conversation_id=queried_conversation.id,
            message_content=message_content,
            sender_type=sender_type,
            unix_timestamp=timestamp,
        )

        view_model = controller.execute(parameters=controller_parameters)

        assert view_model is not None
        assert view_model.message_id is not None

        queried_message = session.get(SQLAMessageBase, view_model.message_id)

        assert queried_message is not None
        assert queried_message.content == message_content
        assert queried_message.timestamp == datetime.fromtimestamp(timestamp)

        if isinstance(queried_message, SQLAAgentMessage):
            assert sender_type == MessageSenderTypeEnum.AGENT.value
        elif isinstance(queried_message, SQLAUserMessage):
            assert sender_type == MessageSenderTypeEnum.USER.value
        else:
            assert False
