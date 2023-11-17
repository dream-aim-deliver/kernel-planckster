from lib.core.entity.models import Conversation, ResearchContext
from lib.infrastructure.repository.sqla.models import SQLAConversation, SQLAResearchContext


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
