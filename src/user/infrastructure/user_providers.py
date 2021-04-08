from dependency_injector import containers, providers
from .repository.in_memory_user_repository import InMemoryUserRepository


class UserProviders(containers.DeclarativeContainer):

    USERS = providers.Singleton(InMemoryUserRepository)
