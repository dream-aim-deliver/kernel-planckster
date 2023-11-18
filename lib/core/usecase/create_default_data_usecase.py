import logging
from typing import Any, Dict, List, Literal
from lib.core.entity.models import KnowledgeSourceEnum
from lib.core.ports.primary.create_default_data_primary_ports import CreateDefaultDataInputPort
from lib.core.usecase_models.create_default_data_usecase_models import (
    CreateDefaultDataError,
    CreateDefaultDataRequest,
    CreateDefaultDataResponse,
)
from lib.infrastructure.repository.sqla.database import TDatabaseFactory
from lib.infrastructure.repository.sqla.models import SQLALLM, SQLAKnowledgeSource, SQLAUser


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

    def _create_default_knowledge_sources(self) -> Dict[str, int] | CreateDefaultDataError:
        ks_enum_members: List[Any] = list(KnowledgeSourceEnum.__members__.keys())

        successful_ks: Dict[str, int] = {}

        for ks_enum in ks_enum_members:
            queried_sqla_ks = self.session.query(SQLAKnowledgeSource).filter_by(source=ks_enum).first()

            if queried_sqla_ks is not None:
                successful_ks[f"{queried_sqla_ks.source.name}"] = queried_sqla_ks.id
                continue

            sqla_ks_alpha = SQLAKnowledgeSource(
                source=ks_enum,
                content_metadata=self._default_parameters["ks_metadata"],
            )

            try:
                sqla_ks_alpha.save(session=self.session)
                self.session.commit()

                queried_sqla_ks = self.session.query(SQLAKnowledgeSource).filter_by(source=ks_enum).first()

                if queried_sqla_ks is None:
                    self.logger.error(f"Error while getting default knowledge source for {ks_enum}")
                    errorResponse = CreateDefaultDataError(
                        errorCode=-1,
                        errorMessage=f"Error while getting default knowledge source for {ks_enum}",
                        errorName="Error while getting default knowledge source",
                        errorType="ErrorWhileGettingDefaultKnowledgeSource",
                    )
                    self.logger.error(f"{errorResponse}")
                    return errorResponse

                successful_ks[f"{queried_sqla_ks.source.name}"] = queried_sqla_ks.id

            except Exception as e:
                self.logger.error(f"Error while creating new knowledge source: {e}")
                errorResponse = CreateDefaultDataError(
                    errorCode=-1,
                    errorMessage=f"Error while creating new knowledge source: {e}",
                    errorName="Error while creating new knowledge source",
                    errorType="ErrorWhileCreatingNewKnowledgeSource",
                )
                self.logger.error(f"{errorResponse}")
                return errorResponse

        return successful_ks

    def _create_defaut_user(self, request_user_sid: str) -> int | CreateDefaultDataError:
        sqla_user_alpha = SQLAUser(
            sid=request_user_sid,
        )

        try:
            sqla_user_alpha.save(session=self.session)
            self.session.commit()
            queried_sqla_user = self.session.query(SQLAUser).filter_by(sid=request_user_sid).first()

            if queried_sqla_user is None:
                self.logger.error(f"Error while getting default user")
                errorResponse = CreateDefaultDataError(
                    errorCode=-1,
                    errorMessage=f"Error while getting default user",
                    errorName="Error while getting default user",
                    errorType="ErrorWhileGettingDefaultUser",
                )
                self.logger.error(f"{errorResponse}")
                return errorResponse

            return queried_sqla_user.id

        except Exception as e:
            self.logger.error(f"Error while creating new user: {e}")
            errorResponse = CreateDefaultDataError(
                errorCode=-1,
                errorMessage=f"Error while creating new user: {e}",
                errorName="Error while creating new user",
                errorType="ErrorWhileCreatingNewUser",
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
        request_user_sid = request.user_sid
        request_llm_name = request.llm_name

        create_default_knowledge_sources_result = self._create_default_knowledge_sources()

        if isinstance(create_default_knowledge_sources_result, CreateDefaultDataError):
            return create_default_knowledge_sources_result

        queried_sqla_user: SQLAUser | None = self.session.query(SQLAUser).filter_by(sid=request_user_sid).first()

        queried_sqla_llm: SQLALLM | None = self.session.query(SQLALLM).filter_by(llm_name=request_llm_name).first()

        if queried_sqla_user is not None:
            if queried_sqla_llm is not None:
                return CreateDefaultDataResponse(
                    knowledge_sources_dict=create_default_knowledge_sources_result,
                    user_id=queried_sqla_user.id,
                    llm_id=queried_sqla_llm.id,
                )
            else:
                create_default_llm_result = self._create_defaut_llm(request_llm_name=request_llm_name)

                if isinstance(create_default_llm_result, CreateDefaultDataError):
                    return create_default_llm_result

                return CreateDefaultDataResponse(
                    knowledge_sources_dict=create_default_knowledge_sources_result,
                    user_id=queried_sqla_user.id,
                    llm_id=create_default_llm_result,
                )

        else:
            if queried_sqla_llm is not None:
                create_default_user_result = self._create_defaut_user(request_user_sid=request_user_sid)

                if isinstance(create_default_user_result, CreateDefaultDataError):
                    return create_default_user_result

                return CreateDefaultDataResponse(
                    knowledge_sources_dict=create_default_knowledge_sources_result,
                    user_id=create_default_user_result,
                    llm_id=queried_sqla_llm.id,
                )
            else:
                create_default_user_result = self._create_defaut_user(request_user_sid=request_user_sid)

                if isinstance(create_default_user_result, CreateDefaultDataError):
                    return create_default_user_result

                create_default_llm_result = self._create_defaut_llm(request_llm_name=request_llm_name)

                if isinstance(create_default_llm_result, CreateDefaultDataError):
                    return create_default_llm_result

                return CreateDefaultDataResponse(
                    knowledge_sources_dict=create_default_knowledge_sources_result,
                    user_id=create_default_user_result,
                    llm_id=create_default_llm_result,
                )


# sqla_user_query: SQLAUser | None = self.session.get(SQLAUser, alpha_parameters["user_sid"])

# if sqla_user_query is not None:
# return AlphaInitUserDTO(status=True, user_id=sqla_user_query.id)

# sqla_research_context_alpha = SQLAResearchContext(
# title=alpha_parameters["research_context"],
# source_data=[],
# )

# sqla_llm_alpha = SQLALLM(
# llm_name=alpha_parameters["llm_name"],
# research_contexts=[sqla_research_context_alpha],
# )

# sqla_user_alpha = SQLAUser(
# sid=alpha_parameters["user_sid"],
# research_contexts=[sqla_research_context_alpha],
# )

# try:
# sqla_research_context_alpha.save(session=self.session)
# self.session.commit()

# return AlphaInitUserDTO(status=True, user_id=sqla_research_context_alpha.user_id)

# except Exception as e:
# self.logger.error(f"Error while creating new user: {e}")
# errorDTO = AlphaInitUserDTO(
# status=False,
# errorCode=-1,
# errorMessage=f"Error while creating new user: {e}",
# errorName="Error while creating new user",
# errorType="ErrorWhileCreatingNewUser",
# )
# self.logger.error(f"{errorDTO}")
# return errorDTO
