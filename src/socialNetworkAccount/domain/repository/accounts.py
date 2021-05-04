from abc import ABC
from typing import List, Optional
from ..model.social_network_account import SocialNetworkAccount
from ..model.social_network_account_id import SocialNetworkAccountId
from ....user.domain.model.user_id import UserId


class Accounts(ABC):

    def save(self, account: SocialNetworkAccount) -> None:
        raise NotImplementedError

    def getByUserId(self, userId: UserId) -> Optional[List[SocialNetworkAccount]]:
        raise NotImplementedError

    def getById(self, accountId: SocialNetworkAccountId) -> Optional[SocialNetworkAccount]:
        raise NotImplementedError
