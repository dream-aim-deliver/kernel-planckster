import random
from typing import List

from faker import Faker
from lib.core.entity.models import LLM
from lib.core.usecase.list_source_data_for_research_context_usecase import ListSourceDataForResearchContextUseCase
from lib.core.usecase_models.list_source_data_for_research_context_usecase_models import (
    ListSourceDataForResearchContextRequest,
    ListSourceDataForResearchContextResponse,
)
from lib.core.view_model.list_source_data_for_research_context_view_model import (
    ListSourceDataForResearchContextViewModel,
)
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.presenter.list_source_data_for_research_context_presenter import (
    ListSourceDataForResearchContextPresenter,
)
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAKnowledgeSource, SQLAUser


def test_list_source_data_for_research_context_presenter(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
    fake_user_with_conversation: SQLAUser,
) -> None:
    presenter: ListSourceDataForResearchContextPresenter = (
        app_container.list_source_data_for_research_context_feature.presenter()
    )

    usecase: ListSourceDataForResearchContextUseCase = (
        app_container.list_source_data_for_research_context_feature.usecase()
    )

    assert usecase is not None

    user = fake_user_with_conversation
    ks_list = fake_knowledge_source_with_source_data_list

    rand_int_1 = random.randint(0, len(user.research_contexts) - 1)
    research_context = user.research_contexts[rand_int_1]

    for ks in ks_list:
        for source_datum in ks.source_data:
            research_context.source_data.append(source_datum)

    source_data = research_context.source_data
    lfns = [source_datum.lfn for source_datum in source_data]

    llm = SQLALLM(
        llm_name=fake.word(),
        research_contexts=user.research_contexts,
    )

    with db_session() as session:
        session.add(research_context)
        session.commit()

        request = ListSourceDataForResearchContextRequest(research_context_id=research_context.id)
        response = usecase.execute(request=request)

        assert response is not None
        assert isinstance(response, ListSourceDataForResearchContextResponse)

        view_model: ListSourceDataForResearchContextViewModel | None = presenter.convert_response_to_view_model(
            response=response
        )

        assert view_model is not None

        assert view_model.status == True
