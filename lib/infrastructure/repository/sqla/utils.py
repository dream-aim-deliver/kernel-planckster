from lib.core.entity.models import (
    LLM,
    Conversation,
    UserMessage,
    AgentMessage,
    MessageContent,
    ResearchContext,
    SourceData,
    Client,
)
from lib.infrastructure.repository.sqla.models import (
    SQLALLM,
    SQLAConversation,
    SQLAUserMessage,
    SQLAAgentMessage,
    SQLAMessageContent,
    SQLAResearchContext,
    SQLASourceData,
    SQLAClient,
)


def convert_sqla_client_to_core_client(sqla_client: SQLAClient) -> Client:
    """
    Converts a SQLAClient to a (core) Client

    @param sqla_client: The SQLAClient to convert
    @type sqla_client: SQLAClient
    @return: The converted Client
    @rtype: Client
    """
    return Client(
        created_at=sqla_client.created_at,
        updated_at=sqla_client.updated_at,
        deleted=sqla_client.deleted,
        deleted_at=sqla_client.deleted_at,
        id=sqla_client.id,
        sub=sqla_client.sub,
    )


def convert_sqla_research_context_to_core_research_context(
    sqla_research_context: SQLAResearchContext,
) -> ResearchContext:
    """
    Converts a SQLAResearchContext to a (core) ResearchContext

    @param sqla_research_context: The SQLAResearchContext to convert
    @type sqla_research_context: SQLAResearchContext
    @return: The converted ResearchContext
    @rtype: ResearchContext
    """
    return ResearchContext(
        created_at=sqla_research_context.created_at,
        updated_at=sqla_research_context.updated_at,
        deleted=sqla_research_context.deleted,
        deleted_at=sqla_research_context.deleted_at,
        id=sqla_research_context.id,
        title=sqla_research_context.title,
        description=sqla_research_context.description,
    )


def convert_sqla_conversation_to_core_conversation(sqla_conversation: SQLAConversation) -> Conversation:
    """
    Converts a SQLAConversation to a (core) Conversation

    @param sqla_conversation: The SQLAConversation to convert
    @type sqla_conversation: SQLAConversation
    @return: The converted Conversation
    @rtype: Conversation
    """
    return Conversation(
        created_at=sqla_conversation.created_at,
        updated_at=sqla_conversation.updated_at,
        deleted=sqla_conversation.deleted,
        deleted_at=sqla_conversation.deleted_at,
        id=sqla_conversation.id,
        title=sqla_conversation.title,
    )


def convert_sqla_client_message_to_core_user_message(
    sqla_client_message: SQLAUserMessage,
) -> UserMessage:
    """
    Converts a SQLAUserMessage to a (core) UserMessage

    @param sqla_client_message: The SQLAUserMessage to convert
    @type sqla_client_message: SQLAUserMessage
    @return: The converted UserMessage
    @rtype: UserMessage
    """
    sender = sqla_client_message.conversation.research_context.client.sub

    message_contents = [
        MessageContent(
            created_at=sqla_client_message.created_at,
            updated_at=sqla_client_message.updated_at,
            deleted=sqla_client_message.deleted,
            deleted_at=sqla_client_message.deleted_at,
            id=piece.id,
            content=piece.content,
            message_id=sqla_client_message.id,
        )
        for piece in sqla_client_message.message_contents
    ]

    return UserMessage(
        created_at=sqla_client_message.created_at,
        updated_at=sqla_client_message.updated_at,
        deleted=sqla_client_message.deleted,
        deleted_at=sqla_client_message.deleted_at,
        id=sqla_client_message.id,
        message_contents=message_contents,
        timestamp=sqla_client_message.timestamp,
        thread_id=sqla_client_message.thread_id,
        sender=sender,
    )


def convert_sqla_agent_message_to_core_agent_message(
    sqla_agent_message: SQLAAgentMessage,
) -> AgentMessage:
    """
    Converts a SQLAAgentMessage to a (core) AgentMessage

    @param sqla_agent_message: The SQLAAgentMessage to convert
    @type sqla_agent_message: SQLAAgentMessage
    @return: The converted AgentMessage
    @rtype: AgentMessage
    """
    sender = sqla_agent_message.conversation.research_context.llm.llm_name

    message_contents = [
        MessageContent(
            created_at=sqla_agent_message.created_at,
            updated_at=sqla_agent_message.updated_at,
            deleted=sqla_agent_message.deleted,
            deleted_at=sqla_agent_message.deleted_at,
            id=piece.id,
            content=piece.content,
            message_id=sqla_agent_message.id,
        )
        for piece in sqla_agent_message.message_contents
    ]

    return AgentMessage(
        created_at=sqla_agent_message.created_at,
        updated_at=sqla_agent_message.updated_at,
        deleted=sqla_agent_message.deleted,
        deleted_at=sqla_agent_message.deleted_at,
        id=sqla_agent_message.id,
        message_contents=message_contents,
        timestamp=sqla_agent_message.timestamp,
        thread_id=sqla_agent_message.thread_id,
        sender=sender,
    )


def convert_sqla_message_content_to_core_message_content(
    sqla_message_content: SQLAMessageContent,
) -> MessageContent:
    """
    Converts a SQLAMessageContent to a (core) MessageContent

    @param sqla_message_content: The SQLAMessageContent to convert
    @type sqla_source_data: SQLAMessageContent
    @return: The converted MessageContent
    @rtype: MessageContent
    """
    return MessageContent(
        created_at=sqla_message_content.created_at,
        updated_at=sqla_message_content.updated_at,
        deleted=sqla_message_content.deleted,
        deleted_at=sqla_message_content.deleted_at,
        id=sqla_message_content.id,
        content=sqla_message_content.content,
    )


def convert_sqla_source_data_to_core_source_data(sqla_source_data: SQLASourceData) -> SourceData:
    """
    Converts a SQLASourceData to a (core) SourceData

    @param sqla_source_data: The SQLASourceData to convert
    @type sqla_source_data: SQLASourceData
    @return: The converted SourceData
    @rtype: SourceData
    """
    return SourceData(
        created_at=sqla_source_data.created_at,
        updated_at=sqla_source_data.updated_at,
        deleted=sqla_source_data.deleted,
        deleted_at=sqla_source_data.deleted_at,
        id=sqla_source_data.id,
        name=sqla_source_data.name,
        relative_path=sqla_source_data.relative_path,
        type=sqla_source_data.type,
        protocol=sqla_source_data.protocol,
        status=sqla_source_data.status,
    )


def convert_core_source_data_to_sqla_source_data(core_source_data: SourceData) -> SQLASourceData:
    """
    Converts a (core) SourceData to a SQLASourceData

    @param core_source_data: The SourceData to convert
    @type core_source_data: SourceData
    @return: The converted SQLASourceData
    @rtype: SQLASourceData
    """
    return SQLASourceData(
        created_at=core_source_data.created_at,
        updated_at=core_source_data.updated_at,
        deleted=core_source_data.deleted,
        deleted_at=core_source_data.deleted_at,
        id=core_source_data.id,
        name=core_source_data.name,
        relative_path=core_source_data.relative_path,
        type=core_source_data.type,
        protocol=core_source_data.protocol,
        status=core_source_data.status,
    )


def convert_sqla_LLM_to_core_LLM(sqla_llm: SQLALLM) -> LLM:
    """
    Converts a SQLALLM to a (core) LLM

    @param sqla_llm: The SQLALLM to convert
    @type sqla_llm: SQLALLM
    @return: The converted LLM
    @rtype: LLM
    """
    return LLM(
        created_at=sqla_llm.created_at,
        updated_at=sqla_llm.updated_at,
        deleted=sqla_llm.deleted,
        deleted_at=sqla_llm.deleted_at,
        id=sqla_llm.id,
        llm_name=sqla_llm.llm_name,
    )
