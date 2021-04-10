from abc import ABC, abstractmethod
from typing import Optional, List
from ..model.user import User
from ..model.user_id import UserId
from ..model.user_mail import UserMail
from ..model.username import Username


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, userId: UserId) -> None:
        pass

    @abstractmethod
    def getAll(self) -> List[User]:
        pass

    @abstractmethod
    def getById(self, userId: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        pass

    @abstractmethod
    def getByUsername(self, username: Username) -> Optional[User]:
        pass
