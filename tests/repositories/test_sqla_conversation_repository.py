import random
from typing import List
from faker import Faker
from lib.core.dto.conversation_repository_dto import (
    GetConversationDTO,
    GetConversationResearchContextDTO,
    ListConversationMessagesDTO,
    ListConversationSourcesDTO,
    NewConversationDTO,
    SendMessageToConversationDTO,
    UpdateConversationDTO,
)
from lib.core.entity.models import MessageBase
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory

from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLACitation,
    SQLAConversation,
    SQLAKnowledgeSource,
    SQLAMessageQuery,
    SQLAUser,
)
from tests.conftest import conversation, source_data


############
# New Conversation Feature
############


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

    researchContext = user_with_conv.research_contexts[0]

    conversation = fake_conversation
    conversation_title = conversation.title

    with db_session() as session:
        session.add(researchContext)
        session.commit()
        conv_DTO: NewConversationDTO = conversation_repository.new_conversation(
            research_context_id=researchContext.id, conversation_title=conversation_title
        )

    assert conv_DTO.status == True
    assert conv_DTO.errorCode == None
    assert isinstance(conv_DTO.conversation_id, int)


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


############
# Get Conversation Feature
############


def test_get_conversation(
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

    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        assert result is not None

        get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=result.id)

    assert get_conv_DTO.status == True
    assert get_conv_DTO.errorCode == None
    assert get_conv_DTO.data is not None
    assert get_conv_DTO.data.title == conversation_title


def test_error_get_conversation_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=None)  # type: ignore

    assert get_conv_DTO.status == False
    assert get_conv_DTO.errorCode == -1
    assert get_conv_DTO.errorMessage == "Conversation ID cannot be None"
    assert get_conv_DTO.errorName == "Conversation ID not provided"
    assert get_conv_DTO.errorType == "ConversationIdNotProvided"


def test_error_get_conversation_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    get_conv_DTO: GetConversationDTO = conversation_repository.get_conversation(conversation_id=irrealistic_ID)

    assert get_conv_DTO.status == False
    assert get_conv_DTO.errorCode == -1
    assert get_conv_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert get_conv_DTO.errorName == "Conversation not found"
    assert get_conv_DTO.errorType == "ConversationNotFound"


############
# Get Conversation Research Context Feature
############


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


############
# List Conversation Messages Feature
############


def test_list_conversation_messages(
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

    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    messages = conversation.messages
    message_contents = tuple([message.content for message in messages])

    with db_session() as session:
        user_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Conversation not found")

        list_conv_msgs_DTO: ListConversationMessagesDTO[
            MessageBase
        ] = conversation_repository.list_conversation_messages(conversation_id=result.id)

    if list_conv_msgs_DTO.data is None:
        raise Exception("Messages of Conversation not found")

    assert list_conv_msgs_DTO.status == True
    assert list_conv_msgs_DTO.errorCode == None
    assert isinstance(list_conv_msgs_DTO.data, list)

    for message in list_conv_msgs_DTO.data:
        if message is None:
            raise Exception("Message of Conversation not found")

        assert message.content in message_contents


def test_error_list_conversation_messages_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    list_conv_msgs_DTO: ListConversationMessagesDTO = conversation_repository.list_conversation_messages(conversation_id=None)  # type: ignore

    assert list_conv_msgs_DTO.status == False
    assert list_conv_msgs_DTO.errorCode == -1
    assert list_conv_msgs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_msgs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_msgs_DTO.errorType == "ConversationIdNotProvided"


def test_error_list_conversation_messages_conversation_id_not_found(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_msgs_DTO: ListConversationMessagesDTO = conversation_repository.list_conversation_messages(conversation_id=irrealistic_ID)  # type: ignore

    assert list_conv_msgs_DTO.status == False
    assert list_conv_msgs_DTO.errorCode == -1
    assert list_conv_msgs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_msgs_DTO.errorName == "Conversation not found"
    assert list_conv_msgs_DTO.errorType == "ConversationNotFound"


############
# Update Conversation Feature
############


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

    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    new_conversation_title = fake.name()

    id = None
    with db_session() as session:
        user_with_conv.save(session=session, flush=True)

        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Conversation not found")

        id = result.id
        conv_DTO: UpdateConversationDTO = conversation_repository.update_conversation(
            conversation_id=id, conversation_title=new_conversation_title
        )

        old_conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()

    if conv_DTO.conversation_id is None:
        raise Exception("Conversation not found")

    assert old_conversation == None
    assert conv_DTO.status == True
    assert conv_DTO.errorCode == None
    assert conv_DTO.conversation_id == id


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


############
# List Conversation Sources Feature
############


def test_list_conversation_sources(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
    fake_citations: List[SQLACitation],
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )
    researchContext = user_with_conv.research_contexts[0]

    ks_with_sd = fake_knowledge_source_with_source_data
    source_data = ks_with_sd.source_data

    researchContext.source_data = source_data

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    citations = fake_citations

    source_data_names_used = []
    source_data_lfns_used = []
    for message in conversation.messages:
        if message.type == "message_response":
            citation = random.choice(citations)
            random_source_datum = random.choice(source_data)
            random_source_datum.citations.append(citation)
            source_data_names_used.append(random_source_datum.name)
            source_data_lfns_used.append(random_source_datum.lfn)
            message.citations.append(citation)
            citations.remove(citation)

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    id = None
    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Conversation not found")

        id = result.id

        list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
            conversation_id=id
        )

    if list_conv_srcs_DTO.data is None:
        raise Exception("Source Data of Conversation not found")

    sql_srcs_names = tuple(source.name for source in list_conv_srcs_DTO.data)
    sql_srcs_lfns = tuple(source.lfn for source in list_conv_srcs_DTO.data)

    assert list_conv_srcs_DTO.status == True
    assert list_conv_srcs_DTO.errorCode == None
    assert isinstance(list_conv_srcs_DTO.data, list)

    for name in source_data_names_used:
        assert name in sql_srcs_names

    for lfn in source_data_lfns_used:
        assert lfn in sql_srcs_lfns


def test_error_list_conversation_sources_none_conversation_id(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(conversation_id=None)  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_srcs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_srcs_DTO.errorType == "ConversationIdNotProvided"


def test_error_list_conversation_sources_none_sqla_conversation(
    app_initialization_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_initialization_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
        conversation_id=irrealistic_ID
    )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"


def test_error_list_conversation_sources_research_context_no_source_data(
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
    researchContext = user_with_conv.research_contexts[0]

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    conv_id = None
    with db_session() as session:
        conv_sqla_query = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if conv_sqla_query is None:
            raise Exception("Conversation not found")

        conv_id = conv_sqla_query.id
        messages = conv_sqla_query.messages
        message_responses = [message for message in messages if message.type == "message_response"]
        message_responses_ids = [message.id for message in message_responses]

        list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.list_conversation_sources(
            conversation_id=conv_id
        )

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Message Responses with ID {message_responses_ids} have no source data."
    assert list_conv_srcs_DTO.errorName == "Message Responses have no source data"
    assert list_conv_srcs_DTO.errorType == "MessageResponsesHaveNoSourceData"


############
# Send Message to Conversation Feature
############


def test_send_message_to_conversation(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
    fake_knowledge_source_with_source_data: SQLAKnowledgeSource,
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )
    researchContext = user_with_conv.research_contexts[0]

    ks_with_sd = fake_knowledge_source_with_source_data
    source_data = ks_with_sd.source_data
    source_data_names = tuple(source.name for source in source_data)
    source_data_lfns = tuple(source.lfn for source in source_data)

    researchContext.source_data = source_data

    conversation = researchContext.conversations[0]
    conversation_title = conversation.title

    new_message_content = fake.text()

    with db_session() as session:
        researchContext.save(session=session, flush=True)
        session.commit()

    id = None
    with db_session() as session:
        result = session.query(SQLAConversation).filter_by(title=conversation_title).first()

        if result is None:
            raise Exception("Test: Conversation not found")

        id = result.id

        send_msg_to_conv_DTO: SendMessageToConversationDTO = conversation_repository.send_message_to_conversation(
            conversation_id=id, message_content=new_message_content
        )

        assert send_msg_to_conv_DTO.data is not None

        dto_message_query_id = send_msg_to_conv_DTO.data.id

        sqla_message_query = session.query(SQLAMessageQuery).filter_by(id=dto_message_query_id).first()

        assert sqla_message_query is not None

        sqla_message_query_id = sqla_message_query.id

    assert send_msg_to_conv_DTO.data is not None

    assert send_msg_to_conv_DTO.status == True
    assert send_msg_to_conv_DTO.errorCode == None
    assert send_msg_to_conv_DTO.data.id == sqla_message_query_id
    assert send_msg_to_conv_DTO.data.content == new_message_content


def test_error_send_message_to_conversation_no_conversation_id(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=None, message_content="abc")  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Conversation ID cannot be None"
    assert list_conv_srcs_DTO.errorName == "Conversation ID not provided"
    assert list_conv_srcs_DTO.errorType == "ConversationIdNotProvided"


def test_error_send_message_to_conversation_no_message_content(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=1, message_content=None)  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == "Message content cannot be None"
    assert list_conv_srcs_DTO.errorName == "Message content not provided"
    assert list_conv_srcs_DTO.errorType == "MessageContentNotProvided"


def test_error_send_message_to_conversation_no_sqla_conversation(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    conversation_repository = app_container.sqla_conversation_repository()

    irrealistic_ID = 99999999
    list_conv_srcs_DTO: ListConversationSourcesDTO = conversation_repository.send_message_to_conversation(conversation_id=irrealistic_ID, message_content="abc")  # type: ignore

    assert list_conv_srcs_DTO.status == False
    assert list_conv_srcs_DTO.errorCode == -1
    assert list_conv_srcs_DTO.errorMessage == f"Conversation with ID {irrealistic_ID} not found in the database."
    assert list_conv_srcs_DTO.errorName == "Conversation not found"
    assert list_conv_srcs_DTO.errorType == "ConversationNotFound"
