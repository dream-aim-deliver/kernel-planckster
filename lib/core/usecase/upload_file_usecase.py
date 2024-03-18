from lib.core.dto.file_repository_dto import FilePathToLFNDTO, UploadFileDTO
from lib.core.ports.primary.upload_file_primary_ports import UploadFileInputPort
from lib.core.usecase_models.upload_file_usecase_models import UploadFileError, UploadFileRequest, UploadFileResponse


class UploadFileUsecase(UploadFileInputPort):
    def execute(self, request: UploadFileRequest) -> UploadFileResponse | UploadFileError:
        file_path = request.file_path

        lfn_dto: FilePathToLFNDTO = self.file_repository.file_path_to_lfn(file_path=file_path)

        if not lfn_dto.status:
            return UploadFileError(
                errorCode=lfn_dto.errorCode,
                errorMessage=lfn_dto.errorMessage,
                errorName=lfn_dto.errorName,
                errorType=lfn_dto.errorType,
            )

        lfn = lfn_dto.lfn

        if not lfn:
            return UploadFileError(
                errorCode=lfn_dto.errorCode,
                errorMessage=lfn_dto.errorMessage,
                errorName=lfn_dto.errorName,
                errorType=lfn_dto.errorType,
            )

        dto: UploadFileDTO = self.file_repository.upload_file(lfn=lfn)

        if dto.status:
            return UploadFileResponse(lfn=dto.lfn, credentials=dto.credentials)

        return UploadFileError(
            errorCode=dto.errorCode,
            errorMessage=dto.errorMessage,
            errorName=dto.errorName,
            errorType=dto.errorType,
        )
