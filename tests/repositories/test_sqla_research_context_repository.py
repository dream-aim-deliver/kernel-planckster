from faker import Faker
from lib.core.dto.research_context_repository_dto import ListResearchContextConversationsDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAResearchContext, SQLAUser


def test_list_conversations_in_research_context(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_user_with_conversation: SQLAUser,
) -> None:
    sqla_research_context_repository = app_container.sqla_research_context_repository()

    user_with_conv = fake_user_with_conversation
    llm = SQLALLM(
        llm_name=fake.name(),
        research_contexts=user_with_conv.research_contexts,
    )
    research_context_title = user_with_conv.research_contexts[0].title

    conversations = user_with_conv.research_contexts[0].conversations
    conversation_titles = [conversation.title for conversation in conversations]

    with db_session() as session:
        user_with_conv.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()
        assert research_context is not None
        list_convs_DTO: ListResearchContextConversationsDTO = sqla_research_context_repository.list_conversations(
            research_context.id
        )
        assert list_convs_DTO is not None
        assert list_convs_DTO.status == True
        assert list_convs_DTO.data is not None

        sql_convs_titles = [conversation.title for conversation in list_convs_DTO.data]

        for title in conversation_titles:
            assert title in sql_convs_titles
