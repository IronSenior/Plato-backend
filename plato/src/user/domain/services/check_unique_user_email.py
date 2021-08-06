from abc import ABC, abstractmethod
from typing import Optional
from ..model.user_mail import UserMail
from ....shared.domain.user_id import UserId


class CheckUniqueUserEmail(ABC):

    @abstractmethod
    def withUserMail(self, userMail: UserMail) -> Optional[UserId]:
        pass
