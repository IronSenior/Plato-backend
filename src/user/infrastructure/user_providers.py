from dependency_injector import containers, providers
from .event_store.user_event_store import UserEventStore
from .service.check_unique_user_name import CheckUniqueUserEmailFromReadModel
from .read_model.in_memory_user_model import InMemoryUserModel


class UserProviders(containers.DeclarativeContainer):

    USERS = providers.Factory(UserEventStore)
    USER_MODEL = providers.Singleton(InMemoryUserModel)
    CHECK_UNIQUE_USER_EMAIL = providers.Factory(CheckUniqueUserEmailFromReadModel)
