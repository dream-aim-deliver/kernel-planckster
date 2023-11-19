import sys
import logging.config
from typing import List
from dependency_injector import containers, providers
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.features.demo_feature_container import DemoFeatureContainer
from lib.infrastructure.config.features.list_conversations_feature_container import ListConversationsFeatureContainer
from lib.infrastructure.config.features.create_default_data_feature_container import CreateDefaultDataFeatureContainer
from lib.infrastructure.config.features.new_source_data_feature_container import NewSourceDataFeatureContainer
from lib.infrastructure.repository.sqla.sqla_knowledge_source_repository import SQLAKnowledgeSourceRepository
from lib.infrastructure.repository.sqla.sqla_research_context_repository import SQLAReseachContextRepository
from lib.infrastructure.repository.sqla.sqla_source_data_repository import SQLASourceDataRepository
from lib.infrastructure.repository.sqla.sqla_user_repository import SQLAUserRepository
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
    sqla_user_repository: providers.Factory[SQLAUserRepository] = providers.Factory(
        SQLAUserRepository, session_factory=db.provided.session
    )

    sqla_conversation_repository: providers.Factory[SQLAConversationRepository] = providers.Factory(
        SQLAConversationRepository,
        session_factory=db.provided.session,
    )

    sqla_research_context_repository: providers.Factory[SQLAReseachContextRepository] = providers.Factory(
        SQLAReseachContextRepository,
        session_factory=db.provided.session,
    )

    sqla_knowledge_source_repository: providers.Factory[SQLAKnowledgeSourceRepository] = providers.Factory(
        SQLAKnowledgeSourceRepository,
        session_factory=db.provided.session,
    )

    sqla_source_data_repository: providers.Factory[SQLASourceDataRepository] = providers.Factory(
        SQLASourceDataRepository,
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

    create_default_data_feature = providers.Container(
        CreateDefaultDataFeatureContainer,
        config=config.features.create_default_data,
        session_factory=db.provided.session,
    )

    new_source_data_feature = providers.Container(
        NewSourceDataFeatureContainer,
        config=config.features.new_source_data,
        knowledge_source_repository=sqla_knowledge_source_repository,
    )
