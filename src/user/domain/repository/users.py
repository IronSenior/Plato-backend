from abc import ABC, abstractmethod
from typing import Optional
from ..model.user import User
from ..model.user_id import UserId
from ..model.user_mail import UserMail


class Users(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getById(self, userid: UserId) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        raise NotImplementedError()
