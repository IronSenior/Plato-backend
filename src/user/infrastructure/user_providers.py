from dependency_injector import containers, providers
from .repository.memory_user_repository import MemoryUserRepository
from .service.check_unique_user_name import CheckUniqueUserEmailFromReadModel


class UserProviders(containers.DeclarativeContainer):

    USERS = providers.Factory(MemoryUserRepository)
    CHECK_UNIQUE_USER_EMAIL = providers.Factory(CheckUniqueUserEmailFromReadModel)
