import importlib
import os
import sys
import logging.config
from types import ModuleType
from typing import List
from dependency_injector import containers, providers
from lib.infrastructure.config.demo_feature_container import DemoFeatureContainer
import lib.infrastructure.rest.endpoints as endpoints

from lib.infrastructure.repository.sqla.database import Database
from lib.infrastructure.repository.sqla.sqla_conversation_repository import SQLAConversationRepository
from pathlib import Path


class FeatureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    demo = providers.Container(DemoFeatureContainer, config=config.demo)


def get_all_modules(package: ModuleType) -> List[str]:
    package_dir = str(Path(__file__).parent.parent / "rest" / "endpoints")
    modules = []
    for filename in os.listdir(package_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove the '.py' extension
            full_module_name = f"{package.__name__}.{module_name}"
            # importlib.import_module(full_module_name)
            modules.append(full_module_name)
    return modules


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])

    # Dynamic wiring of fastapi endpoints:
    modules = get_all_modules(endpoints)
    wiring_config = containers.WiringConfiguration(
        modules=modules,
    )

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

    # Features:
    features = providers.Container(FeatureContainer, config=config.features)

    # Repositories:
    sqla_conversation_repository: providers.Factory[SQLAConversationRepository] = providers.Factory(
        SQLAConversationRepository,
        session_factory=db.provided.session,
    )

    # Gateways:

    # Domain Services:
