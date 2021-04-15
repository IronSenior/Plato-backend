from ...domain.services.check_unique_user_email import CheckUniqueUserEmail
from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.repository.user_repository import UserRepository
from typing import Optional
from dependency_injector.wiring import Provide, inject


class CheckUniqueUserEmailFromReadModel(CheckUniqueUserEmail):

    @inject
    def __init__(self, userRepository: UserRepository = Provide["USERS"]):
        self.userRepository: UserRepository = userRepository

    def withUserMail(self, userMail: UserMail) -> Optional[UserId]:
        user = self.userRepository.getByEmail(userMail)
        if user is None:
            return None
        return UserId(user.userid)
