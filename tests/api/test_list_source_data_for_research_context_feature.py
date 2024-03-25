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
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAClient


def test_list_source_data_for_research_context_presenter(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake: Faker,
    fake_client_with_source_data_list: List[SQLAClient],
    fake_client_with_conversation: SQLAClient,
) -> None:
    presenter: ListSourceDataForResearchContextPresenter = (
        app_container.list_source_data_for_research_context_feature.presenter()
    )

    usecase: ListSourceDataForResearchContextUseCase = (
        app_container.list_source_data_for_research_context_feature.usecase()
    )

    assert usecase is not None

    sqla_client_with_conv = fake_client_with_conversation
    sqla_client_with_sd_list = fake_client_with_source_data_list

    research_context = random.choice(sqla_client_with_conv.research_contexts)

    for client_with_sd in sqla_client_with_sd_list:
        for source_datum in client_with_sd.source_data:
            research_context.source_data.append(source_datum)

    llm = SQLALLM(
        llm_name=fake.word(),
        research_contexts=sqla_client_with_conv.research_contexts,
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
