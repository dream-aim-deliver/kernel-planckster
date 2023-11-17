from dependency_injector import containers, providers

from lib.core.sdk.feature_descriptor import BaseFeatureDescriptor


class BaseFeatureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    feature_descriptor = providers.Factory(
        BaseFeatureDescriptor,
        name=config.name,
        description=config.description,
        version=config.version,
        verb=config.verb,
        tags=config.tags,
        endpoint=config.endpoint,
        enabled=config.enabled,
        auth=config.auth,
    )
