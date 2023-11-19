from typing import List
from lib.core.usecase_models.list_source_data_usecase_models import ListSourceDataRequest
from lib.core.view_model.list_source_data_view_model import ListSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.list_source_data_controller import (
    ListSourceDataController,
    ListSourceDataControllerParameter,
)
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAKnowledgeSource


def test_list_source_data_use_case(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_knowledge_source_with_source_data_list: List[SQLAKnowledgeSource],
) -> None:
    usecase = app_container.list_source_data_feature.usecase()
    assert usecase is not None

    knowledge_source_list = fake_knowledge_source_with_source_data_list

    with db_session() as session:
        for ks in knowledge_source_list:
            ks.save(session=session, flush=True)
        session.commit()

        request = ListSourceDataRequest()
        response = usecase.execute(request=request)

        assert response is not None


def test_list_source_data_controller(
    app_container: ApplicationContainer,
) -> None:
    controller: ListSourceDataController = app_container.list_source_data_feature.controller()
    assert controller is not None

    controller_parameters = ListSourceDataControllerParameter(knowledge_source_id=None)
    view_model: ListSourceDataViewModel | None = controller.execute(parameters=controller_parameters)

    assert view_model is not None
