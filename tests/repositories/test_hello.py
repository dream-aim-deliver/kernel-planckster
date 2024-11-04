from lib.core.entity.models import ProtocolEnum, SourceDataStatusEnum
from lib.core.usecase_models.list_source_data_usecase_models import ListSourceDataRequest
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import Database
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData


def test_2_database_calls_to_the_same_repository_function(
    app_migrated_db: Database,
) -> None:
    session = app_migrated_db.session()
    simple_session = app_migrated_db.simple_session()
    client = SQLAClient(
        sub="test_sub",
    )
    simple_session.add(client)
    simple_session.commit()

    result = simple_session.query(SQLAClient).filter_by(sub="test_sub").first()
    assert result is not None


def test_detached_instance(
    app_migrated_db: Database,
    app_container: ApplicationContainer,
) -> None:
    sqla_client = SQLAClient(
        sub="test_sub",
    )

    sd_status = SourceDataStatusEnum.AVAILABLE

    sqla_source_data_1 = SQLASourceData(
        name="fuck",
        relative_path="something/something.fuck",
        type="",
        protocol=ProtocolEnum.S3,
        status=sd_status,
    )

    sqla_client.source_data.append(sqla_source_data_1)

    usecase = app_container.list_source_data_feature.usecase()

    with app_migrated_db.session() as session:
        sqla_client.save(session=session)
        session.commit()

        request = ListSourceDataRequest(
            client_id=sqla_client.id,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert response.status == True

        assert response.source_data_list is not None
    assert sqla_client.id == 1
    with app_migrated_db.session() as session:
        sqla_source_data_2 = SQLASourceData(
            name="fuc2",
            relative_path="something/somethisngs.fuck",
            type="",
            protocol=ProtocolEnum.S3,
            status=sd_status,
        )

        sqla_client.source_data.append(sqla_source_data_2)
        sqla_client.save(session=session)
        request = ListSourceDataRequest(
            client_id=sqla_client.id,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert response.status == True
        assert len(response.source_data_list) == 2


def test_args_error(
    app_migrated_db: Database,
    app_container: ApplicationContainer,
) -> None:
    with app_migrated_db.session() as session:
        sqla_client = SQLAClient(
            sub="test_sub",
        )

        sd_status = SourceDataStatusEnum.AVAILABLE

        sqla_source_data_1 = SQLASourceData(
            name="fuck",
            relative_path="something/something.fuck",
            type="",
            protocol=ProtocolEnum.S3,
            status=sd_status,
        )

        sqla_client.source_data.append(sqla_source_data_1)

        usecase = app_container.list_source_data_feature.usecase()

        sqla_client.save(session=session)
        session.commit()

        request = ListSourceDataRequest(
            client_id=sqla_client.id,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert response.status == True

        assert response.source_data_list is not None

        sqla_source_data_2 = SQLASourceData(
            name="fuc2",
            relative_path="something/somethisngs.fuck",
            type="",
            protocol=ProtocolEnum.S3,
            status=sd_status,
        )

        sqla_client.source_data.append(sqla_source_data_2)
        sqla_client.save(session=session)
        session.commit()
        request = ListSourceDataRequest(
            client_id=sqla_client.id,
        )
        response = usecase.execute(request=request)

        assert response is not None
        assert response.status == True
        assert len(response.source_data_list) == 2
