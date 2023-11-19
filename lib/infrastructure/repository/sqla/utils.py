from lib.core.entity.models import Conversation, MessageQuery, MessageResponse, ResearchContext, SourceData, User
from lib.infrastructure.repository.sqla.models import (
    SQLAConversation,
    SQLAMessageQuery,
    SQLAMessageResponse,
    SQLAResearchContext,
    SQLASourceData,
    SQLAUser,
)


def convert_sqla_user_to_core_user(sqla_user: SQLAUser) -> User:
    """
    Converts a SQLAUser to a (core) User

    @param sqla_user: The SQLAUser to convert
    @type sqla_user: SQLAUser
    @return: The converted User
    @rtype: User
    """
    return User(
        created_at=sqla_user.created_at,
        updated_at=sqla_user.updated_at,
        deleted=sqla_user.deleted,
        deleted_at=sqla_user.deleted_at,
        id=sqla_user.id,
        sid=sqla_user.sid,
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


def convert_sqla_message_query_to_core_message_query(sqla_message_query: SQLAMessageQuery) -> MessageQuery:
    """
    Converts a SQLAMessageQuery to a (core) MessageQuery

    @param sqla_message_query: The SQLAMessageQuery to convert
    @type sqla_message_query: SQLAMessageQuery
    @return: The converted MessageQuery
    @rtype: MessageQuery
    """
    return MessageQuery(
        created_at=sqla_message_query.created_at,
        updated_at=sqla_message_query.updated_at,
        deleted=sqla_message_query.deleted,
        deleted_at=sqla_message_query.deleted_at,
        id=sqla_message_query.id,
        content=sqla_message_query.content,
        timestamp=sqla_message_query.timestamp,
    )


def convert_sqla_message_response_to_core_message_response(
    sqla_message_response: SQLAMessageResponse,
) -> MessageResponse:
    """
    Converts a SQLAMessageResponse to a (core) MessageResponse

    @param sqla_message_response: The SQLAMessageResponse to convert
    @type sqla_message_response: SQLAMessageResponse
    @return: The converted MessageResponse
    @rtype: MessageResponse
    """
    return MessageResponse(
        created_at=sqla_message_response.created_at,
        updated_at=sqla_message_response.updated_at,
        deleted=sqla_message_response.deleted,
        deleted_at=sqla_message_response.deleted_at,
        id=sqla_message_response.id,
        content=sqla_message_response.content,
        timestamp=sqla_message_response.timestamp,
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
        type=sqla_source_data.type,
        lfn=sqla_source_data.lfn,
        protocol=sqla_source_data.protocol,
        status=sqla_source_data.status,
    )
