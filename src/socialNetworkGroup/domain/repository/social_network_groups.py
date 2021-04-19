from abc import ABC, abstractmethod
from typing import Optional, List
from ..model.social_network_group_id import SocialNetworkGroupId
from ..model.social_network_group import SocialNetworkGroup
from ....user.domain.model.user_id import UserId


class SocialNetworkGroups(ABC):

    @abstractmethod
    def save(self, socialNetworkGroup: SocialNetworkGroup) -> None:
        raise NotImplementedError()

    @abstractmethod
    def getById(self, id: SocialNetworkGroupId) -> Optional[SocialNetworkGroup]:
        raise NotImplementedError()

    @abstractmethod
    def getByUserId(self, userId: UserId) -> Optional[List[SocialNetworkGroup]]:
        raise NotImplementedError()
