import random
from lib.core.dto.file_repository_dto import SourceDataCompositeIndexExistsAsFileDTO
from lib.infrastructure.config.containers import ApplicationContainer
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLAClient, SQLASourceData
from lib.infrastructure.repository.sqla.utils import convert_sqla_client_to_core_client


def test_source_data_is_file_in_minio(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
    fake_client_with_source_data: SQLAClient,
    db_session: TDatabaseFactory,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    sqla_client = fake_client_with_source_data
    source_data = random.choice(sqla_client.source_data)

    with db_session() as session:
        session.add(sqla_client)
        session.commit()

        core_client = convert_sqla_client_to_core_client(sqla_client)
        bucket_name_raw = core_client.sub

        file_path = test_file_path

        minio_repo.store.create_bucket_if_not_exists(bucket_name_raw)

        pfn = minio_repo.store.protocol_and_relative_path_to_pfn(
            protocol=source_data.protocol,
            relative_path=source_data.relative_path,
            bucket_name=bucket_name_raw,
        )

        bucket_name = pfn.bucket_name
        minio_object = minio_repo.store.pfn_to_object_name(pfn)
        minio_repo.store.client.fput_object(minio_object.bucket_name, minio_object.object_name, file_path)

        dto: SourceDataCompositeIndexExistsAsFileDTO = minio_repo.composite_index_of_source_data_exists_as_file(
            client=core_client,
            protocol=source_data.protocol,
            relative_path=source_data.relative_path,
        )

        assert dto.status == True
        assert dto.existence == True
        assert dto.relative_path == source_data.relative_path
        assert dto.protocol == source_data.protocol


def test_obtain_working_signed_url_for_upload_inputs_are_none(
    app_initialization_container: ApplicationContainer,
    db_session: TDatabaseFactory,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    dto = minio_repo.get_client_data_for_upload(
        client=None,  # type: ignore
        protocol=None,  # type: ignore
        relative_path=None,  # type: ignore
    )

    assert dto.status == False
    assert dto.errorCode == -1
    assert dto.credentials == None
