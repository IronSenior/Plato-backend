from dependency_injector import containers, providers
from .repository.sn_group_repository import SocialNetworkGroupRepository


class SNGroupProviders(containers.DeclarativeContainer):

    SOCIAL_NETWORK_GROUPS = providers.Singleton(SocialNetworkGroupRepository)
