from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_source_data_controller import NewSourceDataControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_source_data_to_core_source_data


def test_new_source_data_feature_is_successful(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
    fake_source_data: SQLASourceData,
) -> None:
    controller = app_container.new_source_data_feature.controller()

    assert controller is not None

    fake_sd = fake_source_data
    fake_lfn = fake_sd.lfn

    controller_parameters = NewSourceDataControllerParameters(knowledge_source_id=1, lfn=fake_lfn)

    view_model: NewSourceDataViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
