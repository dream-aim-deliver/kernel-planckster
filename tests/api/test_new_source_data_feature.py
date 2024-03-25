from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_source_data_controller import NewSourceDataControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLASourceData


def test_new_source_data_feature_is_successful(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_source_data: SQLASourceData,
) -> None:
    controller = app_container.new_source_data_feature.controller()

    assert controller is not None

    fake_sd = fake_source_data
    fake_sd_name = fake_sd.name
    fake_protocol = fake_sd.protocol
    fake_relative_path = fake_sd.relative_path

    controller_parameters = NewSourceDataControllerParameters(
        client_id=1,
        source_data_name=fake_sd_name,
        protocol=fake_protocol,
        relative_path=fake_relative_path,
    )

    view_model: NewSourceDataViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
