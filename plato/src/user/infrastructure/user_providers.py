from dependency_injector import containers, providers
from .repository.mongo_user_repository import MongoUserRepository
from .service.check_unique_user_name import CheckUniqueUserEmailFromReadModel
from dotenv import load_dotenv

load_dotenv()


class UserProviders(containers.DeclarativeContainer):

    USERS = providers.Factory(MongoUserRepository)
    CHECK_UNIQUE_USER_EMAIL = providers.Factory(CheckUniqueUserEmailFromReadModel)
