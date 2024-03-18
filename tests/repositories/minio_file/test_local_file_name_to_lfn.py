from lib.core.entity.models import LFN
from lib.infrastructure.config.containers import ApplicationContainer


def test_obtain_lfn_from_local_file_name(
    app_initialization_container: ApplicationContainer,
    test_file_path: str,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    file_path = test_file_path

    dto = minio_repo.file_path_to_lfn(file_path=file_path)

    assert dto.status == True
    assert dto.lfn
    assert isinstance(dto.lfn, LFN)


def test_obtain_lfn_from_local_file_name_handle_special_characters(
    app_initialization_container: ApplicationContainer,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    base_path = "/path/to"
    normal_chars = "this_file_name_that_contains_a_lot_of_special_characters"
    special_chars = "!@#$%^&*()_+{}|:<>?`-=[]\;',.~\""
    file_path = f"{base_path}/{normal_chars}_{special_chars}.txt"

    dto = minio_repo.file_path_to_lfn(file_path=file_path)

    assert dto.status == True
    assert dto.lfn
    assert isinstance(dto.lfn, LFN)
    assert normal_chars in dto.lfn.relative_path
    assert special_chars not in dto.lfn.relative_path


def test_error_obtain_lfn_from_local_file_name_none_file_path(
    app_initialization_container: ApplicationContainer,
) -> None:
    minio_repo = app_initialization_container.minio_file_repository()

    file_path = None

    dto = minio_repo.file_path_to_lfn(file_path=file_path)  # type: ignore

    assert dto.status == False
    assert dto.lfn == None
    assert dto.errorCode == -1
    assert dto.errorMessage == "File path cannot be None"
    assert dto.errorName == "FilePathNotProvided"
    assert dto.errorType == "FilePathNotProvided"
