import logging
from lib.core.ports.primary.create_default_data_primary_ports import CreateDefaultDataInputPort
from lib.core.usecase_models.create_default_data_usecase_models import (
    CreateDefaultDataError,
    CreateDefaultDataRequest,
    CreateDefaultDataResponse,
)
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAClient


class CreateDefaultDataUseCase(CreateDefaultDataInputPort):
    _default_parameters = {
        "ks_metadata": "default",
    }

    def __init__(self, session_factory: TDatabaseFactory) -> None:
        """
        These usually go in the repositories
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()

        with session_factory() as session:
            self.session = session

    def _create_defaut_client(self, request_client_sub: str) -> int | CreateDefaultDataError:
        sqla_client_alpha = SQLAClient(
            sub=request_client_sub,
        )

        try:
            sqla_client_alpha.save(session=self.session)
            self.session.commit()
            queried_sqla_client = self.session.query(SQLAClient).filter_by(sub=request_client_sub).first()

            if queried_sqla_client is None:
                self.logger.error(f"Error while getting default client")
                errorResponse = CreateDefaultDataError(
                    errorCode=-1,
                    errorMessage=f"Error while getting default client",
                    errorName="Error while getting default client",
                    errorType="ErrorWhileGettingDefaultClient",
                )
                self.logger.error(f"{errorResponse}")
                return errorResponse

            return queried_sqla_client.id

        except Exception as e:
            self.logger.error(f"Error while creating new client: {e}")
            errorResponse = CreateDefaultDataError(
                errorCode=-1,
                errorMessage=f"Error while creating new client: {e}",
                errorName="Error while creating new client",
                errorType="ErrorWhileCreatingNewClient",
            )
            self.logger.error(f"{errorResponse}")
            return errorResponse

    def _create_defaut_llm(self, request_llm_name: str) -> int | CreateDefaultDataError:
        sqla_llm_alpha = SQLALLM(
            llm_name=request_llm_name,
        )

        try:
            sqla_llm_alpha.save(session=self.session)
            self.session.commit()
            queried_sqla_llm = self.session.query(SQLALLM).filter_by(llm_name=request_llm_name).first()

            if queried_sqla_llm is None:
                self.logger.error(f"Error while getting default llm")
                errorResponse = CreateDefaultDataError(
                    errorCode=-1,
                    errorMessage=f"Error while getting default llm",
                    errorName="Error while getting default llm",
                    errorType="ErrorWhileGettingDefaultLLM",
                )
                self.logger.error(f"{errorResponse}")
                return errorResponse

            return queried_sqla_llm.id

        except Exception as e:
            self.logger.error(f"Error while creating new llm: {e}")
            errorResponse = CreateDefaultDataError(
                errorCode=-1,
                errorMessage=f"Error while creating new llm: {e}",
                errorName="Error while creating new llm",
                errorType="ErrorWhileCreatingNewLLM",
            )
            self.logger.error(f"{errorResponse}")
            return errorResponse

    def execute(self, request: CreateDefaultDataRequest) -> CreateDefaultDataResponse | CreateDefaultDataError:
        request_client_sub = request.client_sub
        request_llm_name = request.llm_name

        queried_sqla_client: SQLAClient | None = (
            self.session.query(SQLAClient).filter_by(sub=request_client_sub).first()
        )

        queried_sqla_llm: SQLALLM | None = self.session.query(SQLALLM).filter_by(llm_name=request_llm_name).first()

        if queried_sqla_client is not None:
            if queried_sqla_llm is not None:
                return CreateDefaultDataResponse(
                    client_id=queried_sqla_client.id,
                    llm_id=queried_sqla_llm.id,
                )

            else:
                create_default_llm_result = self._create_defaut_llm(request_llm_name=request_llm_name)

                if isinstance(create_default_llm_result, CreateDefaultDataError):
                    return create_default_llm_result

                return CreateDefaultDataResponse(
                    client_id=queried_sqla_client.id,
                    llm_id=create_default_llm_result,
                )

        else:
            if queried_sqla_llm is not None:
                create_default_client_result = self._create_defaut_client(request_client_sub=request_client_sub)

                if isinstance(create_default_client_result, CreateDefaultDataError):
                    return create_default_client_result

                return CreateDefaultDataResponse(
                    client_id=create_default_client_result,
                    llm_id=queried_sqla_llm.id,
                )
            else:
                create_default_client_result = self._create_defaut_client(request_client_sub=request_client_sub)

                if isinstance(create_default_client_result, CreateDefaultDataError):
                    return create_default_client_result

                create_default_llm_result = self._create_defaut_llm(request_llm_name=request_llm_name)

                if isinstance(create_default_llm_result, CreateDefaultDataError):
                    return create_default_llm_result

                return CreateDefaultDataResponse(
                    client_id=create_default_client_result,
                    llm_id=create_default_llm_result,
                )
