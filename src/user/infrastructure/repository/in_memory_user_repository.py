from ...domain.model.username import Username
from ...domain.model.user_mail import UserMail
from ...domain.model.user_id import UserId
from ...domain.model.user import User
from ...domain.repository.user_repository import UserRepository
from typing import List, Optional


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.__users: List[User] = []

    def save(self, user: User) -> None:
        self.__users.append(user)

    def delete(self, userId: UserId) -> None:
        user = self.getById(userId)
        self.__users.remove(user)

    def getAll(self) -> List[User]:
        return self.__users

    def getById(self, userId: UserId) -> Optional[User]:
        for user in self.__users:
            if user.userid == userId.value:
                return user

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        for user in self.__users:
            if user.email == usermail.value:
                return user

    def getByUsername(self, username: Username) -> Optional[User]:
        for user in self.__users:
            if user.username == username.value:
                return user
