import sys
import logging.config
from dependency_injector import containers, providers
from lib.core.ports.primary.demo_ports import DemoInputPort, DemoOutputPort
from lib.core.sdk.feature import BaseFeatureDescriptor
from lib.core.usecase.demo_usecase import DemoUseCase
from lib.infrastructure.controller.demo_controller import DemoController
from lib.infrastructure.presenter.demo_presenter import DemoPresenter


from lib.infrastructure.repository.sqla.database import Database
from lib.infrastructure.repository.sqla.sqla_conversation_repository import SQLAConversationRepository


class DemoFeature(containers.DeclarativeContainer):
    config = providers.Configuration()

    presenter = providers.Factory[DemoOutputPort](
        DemoPresenter,
    )

    usecase = providers.Factory[DemoInputPort](
        DemoUseCase,
    )

    controller = providers.Factory(
        DemoController,
        usecase=usecase,
        presenter=presenter,
    )

    feature_descriptor = providers.Factory(
        BaseFeatureDescriptor,
        name=config.name,
        description=config.description,
        version=config.version,
        verb=config.verb,
        endpoint=config.endpoint,
        enabled=config.enabled,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])
    demo = providers.Container(DemoFeature, config=config.feature_demo)
    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    db = providers.Singleton(
        Database,
        db_host=config.rdbms.host,
        db_port=config.rdbms.port.as_int(),
        db_user=config.rdbms.username,
        db_password=config.rdbms.password,
        db_name=config.rdbms.database,
    )

    # Repositories:
    sqla_conversation_repository: providers.Factory[SQLAConversationRepository] = providers.Factory(
        SQLAConversationRepository,
        session_factory=db.provided.session,
    )

    # Gateways:

    # Domain Services:
