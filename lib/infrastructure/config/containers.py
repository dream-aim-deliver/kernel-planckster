import sys
import logging.config
from dependency_injector import containers, providers
from lib.infrastructure.config.demo_feature_container import DemoFeature


from lib.infrastructure.repository.sqla.database import Database
from lib.infrastructure.repository.sqla.sqla_conversation_repository import SQLAConversationRepository


class FeatureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    demo = providers.Container(DemoFeature, config=config.demo)


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])
    wiring_config = containers.WiringConfiguration(modules=[".demo_feature"])
    features = providers.Container(FeatureContainer, config=config.features)
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
