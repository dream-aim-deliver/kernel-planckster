from typing import Any, List
from lib.core.entity.models import KnowledgeSourceEnum
from lib.core.view_model.create_default_data_view_model import CreateDefaultDataViewModel
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.controller.create_default_data_controller import CreateDefaultDataControllerParameters
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAKnowledgeSource, SQLAUser


def test_create_default_data_is_succesful(
    app_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    controller = app_container.create_default_data_feature.controller()

    assert controller is not None

    user_sid = "Test user"
    llm_name = "Test LLM"

    ks_enum_members: List[Any] = [str(ks_enum).lower() for ks_enum in KnowledgeSourceEnum.__members__.keys()]

    controller_parameters = CreateDefaultDataControllerParameters(
        user_sid=user_sid,
        llm_name=llm_name,
    )

    view_model: CreateDefaultDataViewModel = controller.execute(parameters=controller_parameters)

    assert view_model is not None

    with db_session() as session:
        queried_sqla_user = session.query(SQLAUser).filter_by(sid=user_sid).first()

        queried_sqla_llm = session.query(SQLALLM).filter_by(llm_name=llm_name).first()

        assert queried_sqla_user is not None
        assert queried_sqla_llm is not None

        queried_knowledge_sources = session.query(SQLAKnowledgeSource).all()

        assert queried_knowledge_sources is not None
        assert len(queried_knowledge_sources) != 0

        queried_ks_enums = [str(ks.source.name).lower() for ks in queried_knowledge_sources]

        assert view_model.status is True
        assert view_model.user_id == queried_sqla_user.id
        assert view_model.llm_id == queried_sqla_llm.id

        view_model_ks_enums = [
            str(key).lower().replace("knowledgesourceenum.", "") for key in view_model.knowledge_sources_dict.keys()
        ]

        for view_model_ks_enum in view_model_ks_enums:
            assert view_model_ks_enum in ks_enum_members
            assert view_model_ks_enum in queried_ks_enums
