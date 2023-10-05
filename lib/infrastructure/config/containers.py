# from pathlib import Path
import sys
import logging.config
from dependency_injector import containers, providers

# from myapp import Database, MyRepository, MyGateway, MyService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./config.yaml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )


#    db = providers.Singleton(
#        Database,
#        db_host=config.rdbms.host,
#        db_port=config.rdbms.port.as_int(),
#        db_user=config.rdbms.username,
#        db_password=config.rdbms.password,
#        db_name=config.rdbms.database,
#    )
#
#    # Repositories
#    my_repository = providers.Singleton(
#        MyRepository,
#        session_factory=db.provided.session,
#    )
#
#    # Gateways:
#    my_gateway = providers.Factory(
#        MyGateway,
#    )
#
#    # Services:
#    my_service = providers.Factory(
#        MyService,
#        my_repository=my_repository,
#        root_dir=config.files.root_directory.as_(Path),
#        data_dir=config.files.source_data_directory.as_(Path),
#    )
