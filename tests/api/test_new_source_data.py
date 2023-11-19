from lib.core.view_model.new_source_data_view_model import NewSourceDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.new_source_data_controller import NewSourceDataControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory


def test_new_source_data_feature_is_successful(
    app_container: ApplicationContainer, db_session: TDatabaseFactory
) -> None:
    controller = app_container.new_source_data_feature.controller()

    assert controller is not None

    controller_parameters = NewSourceDataControllerParameters(
        knowledge_source_id=1, source_data_lfn_list=["s3://path/to/file.extension"]
    )

    view_model: NewSourceDataViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None
