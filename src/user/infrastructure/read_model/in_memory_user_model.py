from typing import List, Optional
from ...domain.model.user import User
from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from .user_model import UserModel


class InMemoryUserModel(UserModel):

    def __init__(self):
        self.__users: List[User] = []

    def save(self, user: User) -> None:
        self.__users.append(user)

    def getById(self, userid: UserId) -> Optional[User]:
        for user in self.__users:
            if userid.value == user.userid:
                return user

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        for user in self.__users:
            if usermail.value == user.email:
                return user
