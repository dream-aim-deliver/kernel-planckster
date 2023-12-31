from dependency_injector import containers, providers

from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor


class BaseFeatureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feature_descriptor = providers.Factory(
        BaseFeatureDescriptor,
        name=config.name,
        description=config.description,
        version=config.version,
        tags=config.tags,
        enabled=config.enabled,
        auth=config.auth,
    )
