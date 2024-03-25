from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.create_default_data_controller import CreateDefaultDataControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAClient


def test_create_default_data_is_succesful(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    controller = app_container.create_default_data_feature.controller()

    assert controller is not None

    client_sub = "Test client"
    llm_name = "Test LLM"

    controller_parameters = CreateDefaultDataControllerParameters(
        client_sub=client_sub,
        llm_name=llm_name,
    )

    view_model: CreateDefaultDataViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None

    with db_session() as session:
        queried_sqla_client = session.query(SQLAClient).filter_by(sub=client_sub).first()

        queried_sqla_llm = session.query(SQLALLM).filter_by(llm_name=llm_name).first()

        assert queried_sqla_client is not None
        assert queried_sqla_llm is not None

        assert view_model.status is True
        assert view_model.client_id == queried_sqla_client.id
        assert view_model.llm_id == queried_sqla_llm.id
