from lib.infrastructure.config.containers import ApplicationContainer


def test_lfn_is_file_in_minio(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    file_path = test_file_path

    lfn = minio_repo.file_path_to_lfn(file_path).lfn
    assert lfn

    pfn = minio_repo.store.lfn_to_pfn(lfn)
    object_name = minio_repo.store.pfn_to_object_name(pfn)
    bucket_name = minio_repo.store.bucket
    minio_repo.store.client.fput_object(bucket_name, object_name, file_path)

    dto = minio_repo.lfn_exists(lfn)

    assert dto.status == True
    assert dto.existence == True
    assert dto.lfn == lfn
