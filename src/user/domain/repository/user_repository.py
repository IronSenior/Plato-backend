from abc import ABC, abstractmethod
from typing import Optional
from ..model.user import User
from ..model.user_id import UserId


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find(self, userId: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def get(self, userId: UserId) -> User:
        pass
