from ...domain.services.check_unique_user_email import CheckUniqueUserEmail
from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from typing import Optional
from dependency_injector.wiring import Provide, inject
from ..read_model.user_model import UserModel


class CheckUniqueUserEmailFromReadModel(CheckUniqueUserEmail):

    @inject
    def __init__(self, userModel: UserModel = Provide["USER_MODEL"]):
        self.userModel: UserModel = userModel

    def withUserMail(self, userMail: UserMail) -> Optional[UserId]:
        user = self.userModel.getByEmail(userMail)
        if user is None:
            return None
        return UserId(user.userid)
