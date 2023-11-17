import sys
import logging.config
from typing import List
from dependency_injector import containers, providers
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.features.demo_feature_container import DemoFeatureContainer
from lib.infrastructure.config.features.list_conversations_feature_container import ListConversationsFeatureContainer
from lib.infrastructure.repository.sqla.sqla_research_context_repository import SQLAReseachContextRepository
import lib.infrastructure.rest.endpoints as endpoints

from lib.infrastructure.repository.sqla.database import Database
from lib.infrastructure.repository.sqla.sqla_conversation_repository import SQLAConversationRepository
from pathlib import Path


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])

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

    sqla_research_context_repository: providers.Factory[SQLAReseachContextRepository] = providers.Factory(
        SQLAReseachContextRepository,
        session_factory=db.provided.session,
    )

    # Dynamic wiring of fastapi endpoints:
    modules = get_all_modules(
        package=endpoints, relative_package_dir=Path(__file__).parent.parent / "rest" / "endpoints"
    )
    wiring_config = containers.WiringConfiguration(
        modules=modules,
    )

    # Features:
    demo_feature = providers.Container(DemoFeatureContainer, config=config.features.demo)
    list_conversations_feature = providers.Container(
        ListConversationsFeatureContainer,
        config=config.features.list_conversations,
        research_context_repository=sqla_research_context_repository,
    )
