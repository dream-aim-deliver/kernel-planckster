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
import lib.infrastructure.routers.demo_router as demo_router


class DemoFeature(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[demo_router])
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
        name=config.features.sum.name,
        description=config.features.sum.description,
        collection=config.tag,
        version=config.version,
        verb=config.features.sum.verb,
        endpoint=config.features.sum.endpoint,
        enabled=config.enabled and config.features.sum.enabled,
        auth=config.auth,
    )


class BaseFeature(containers.DeclarativeContainer):
    config = providers.Configuration()

    feature_descriptor = providers.Factory(
        BaseFeatureDescriptor,
        name=config.features.sum.name,
        description=config.features.sum.description,
        collection=config.name,
        version=config.version,
        verb=config.features.sum.verb,
        endpoint=config.features.sum.endpoint,
        enabled=config.enabled,
        auth=config.auth,
    )


class DemoFeatureSet(containers.DeclarativeContainer):
    config = providers.Configuration()

    demo_feature = providers.Container(
        DemoFeature,
        config=config.feature_sets.demo,
        controller=providers.Factory(
            DemoController,
            usecase=providers.Factory[DemoInputPort](DemoUseCase),
            presenter=providers.Factory[DemoOutputPort](DemoPresenter),
        ),
        feature_descriptor=providers.Factory(
            BaseFeatureDescriptor,
            name=config.features.sum.name,
            description=config.features.sum.description,
            collection=config.name,
            version=config.version,
            verb=config.verb,
            endpoint=config.endpoint,
            enabled=config.enabled,
            auth=config.auth,
        ),
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])
    demo = providers.Container(DemoFeature, config=config.feature_sets.demo)
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
