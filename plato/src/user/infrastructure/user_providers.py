from dependency_injector import containers, providers
import os
from .repository.memory_user_repository import MemoryUserRepository
from .repository.mongo_user_repository import MongoUserRepository
from .service.check_unique_user_name import CheckUniqueUserEmailFromReadModel
from dotenv import load_dotenv

load_dotenv()


class UserProviders(containers.DeclarativeContainer):

    if os.environ["ENV_MODE"] == "Test":
        USERS = providers.Singleton(MemoryUserRepository)
    else:
        USERS = providers.Factory(MongoUserRepository)

    CHECK_UNIQUE_USER_EMAIL = providers.Factory(CheckUniqueUserEmailFromReadModel)
