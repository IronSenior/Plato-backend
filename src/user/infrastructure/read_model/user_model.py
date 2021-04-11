from abc import ABC, abstractmethod
from typing import Optional
from ...domain.model.user_id import UserId
from ...domain.model.user import User
from ...domain.model.user_mail import UserMail


class UserModel(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def getById(self, userid: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        pass
