import sys
import logging.config
from dependency_injector import containers, providers
from lib.core.sdk.utils import get_all_modules
from lib.infrastructure.config.features.demo_feature_container import DemoFeatureContainer
from lib.infrastructure.config.features.get_client_data_for_download_feature_container import (
    GetClientDataForDownloadFeatureContainer,
)
from lib.infrastructure.config.features.list_conversations_feature_container import ListConversationsFeatureContainer
from lib.infrastructure.config.features.create_default_data_feature_container import CreateDefaultDataFeatureContainer
from lib.infrastructure.config.features.list_messages_feature_container import ListMessagesFeatureContainer
from lib.infrastructure.config.features.list_research_contexts_feature_container import (
    ListResearchContextsFeatureContainer,
)
from lib.infrastructure.config.features.list_source_data_feature_container import ListSourceDataFeatureContainer
from lib.infrastructure.config.features.list_source_data_for_research_context_feature_container import (
    ListSourceDataForResearchContextFeatureContainer,
)
from lib.infrastructure.config.features.new_conversation_feature_container import NewConversationFeatureContainer
from lib.infrastructure.config.features.new_message_feature_container import NewMessageFeatureContainer
from lib.infrastructure.config.features.new_research_context_feature_container import NewResearchContextFeatureContainer
from lib.infrastructure.config.features.extend_research_context_feature_container import (
    ExtendResearchContextFeatureContainer,
)
from lib.infrastructure.config.features.new_source_data_feature_container import NewSourceDataFeatureContainer
from lib.infrastructure.config.features.get_client_data_for_upload_feature_container import (
    GetClientDataForUploadFeatureContainer,
)
from lib.infrastructure.repository.minio.minio_file_repository import MinIOFileRepository
from lib.infrastructure.repository.minio.minio_object_store import MinIOObjectStore
from lib.infrastructure.repository.sqla.sqla_research_context_repository import SQLAReseachContextRepository
from lib.infrastructure.repository.sqla.sqla_source_data_repository import SQLASourceDataRepository
from lib.infrastructure.repository.sqla.sqla_client_repository import SQLAClientRepository
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

    db = providers.Factory(
        Database,
        db_host=config.rdbms.host,
        db_port=config.rdbms.port.as_int(),
        db_user=config.rdbms.username,
        db_password=config.rdbms.password,
        db_name=config.rdbms.database,
    )

    storage = providers.Factory(
        MinIOObjectStore,
        host=config.object_store.host,
        port=config.object_store.port.as_int(),
        access_key=config.object_store.access_key,
        secret_key=config.object_store.secret_key,
        secure=config.object_store.secure,
        cert_check=config.object_store.cert_check,
        signed_url_expiry=config.object_store.signed_url_expiry.as_int(),
    )

    # Repositories:
    sqla_client_repository: providers.Factory[SQLAClientRepository] = providers.Factory(
        SQLAClientRepository, session_generator_factory=db.provided.session
    )

    sqla_conversation_repository: providers.Factory[SQLAConversationRepository] = providers.Factory(
        SQLAConversationRepository,
        session_generator_factory=db.provided.session,
    )

    sqla_research_context_repository: providers.Factory[SQLAReseachContextRepository] = providers.Factory(
        SQLAReseachContextRepository,
        session_generator_factory=db.provided.session,
    )

    sqla_source_data_repository: providers.Factory[SQLASourceDataRepository] = providers.Factory(
        SQLASourceDataRepository,
        session_generator=db.provided.session,
    )

    minio_file_repository: providers.Factory[MinIOFileRepository] = providers.Factory(
        MinIOFileRepository,
        object_store=storage.provided,
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
        default_client_sub=config.features.default_data.default_client_sub,
        default_llm_name=config.features.default_data.default_llm_name,
    )

    new_source_data_feature = providers.Container(
        NewSourceDataFeatureContainer,
        config=config.features.new_source_data,
        client_repository=sqla_client_repository,
        file_repository=minio_file_repository,
    )

    list_source_data_feature = providers.Container(
        ListSourceDataFeatureContainer,
        config=config.features.list_source_data,
        client_repository=sqla_client_repository,
    )

    new_research_context_feature = providers.Container(
        NewResearchContextFeatureContainer,
        config=config.features.new_research_context,
        client_repository=sqla_client_repository,
    )

    extend_research_context_feature = providers.Container(
        ExtendResearchContextFeatureContainer,
        config=config.features.extend_research_context,
        client_repository=sqla_client_repository,
        research_context_repository=sqla_research_context_repository,
    )

    new_conversation_feature = providers.Container(
        NewConversationFeatureContainer,
        config=config.features.new_conversation,
        research_context_repository=sqla_research_context_repository,
    )

    list_research_contexts_feature = providers.Container(
        ListResearchContextsFeatureContainer,
        config=config.features.list_research_contexts,
        client_repository=sqla_client_repository,
    )

    list_source_data_for_research_context_feature = providers.Container(
        ListSourceDataForResearchContextFeatureContainer,
        config=config.features.list_source_data_for_research_context,
        research_context_repository=sqla_research_context_repository,
    )

    get_client_data_for_upload_feature = providers.Container(
        GetClientDataForUploadFeatureContainer,
        config=config.features.get_client_data_for_upload,
        client_repository=sqla_client_repository,
        file_repository=minio_file_repository,
    )

    get_client_data_for_download_feature = providers.Container(
        GetClientDataForDownloadFeatureContainer,
        config=config.features.get_client_data_for_download,
        client_repository=sqla_client_repository,
        source_data_repository=sqla_source_data_repository,
        file_repository=minio_file_repository,
    )

    list_messages_feature = providers.Container(
        ListMessagesFeatureContainer,
        config=config.features.list_messages,
        conversation_repository=sqla_conversation_repository,
    )

    new_message_feature = providers.Container(
        NewMessageFeatureContainer,
        config=config.features.new_message,
        conversation_repository=sqla_conversation_repository,
    )
