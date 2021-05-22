from dependency_injector import containers, providers
from .repository.memory_account_repository import MemoryAccountRepository


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Singleton(MemoryAccountRepository)
