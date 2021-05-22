from abc import ABC
from typing import List, Optional
from ..model.account import Account
from ..model.account_id import AccountId
from ....shared.domain.user_id import UserId


class Accounts(ABC):

    def save(self, account: Account) -> None:
        raise NotImplementedError

    def getByUserId(self, userId: UserId) -> Optional[List[Account]]:
        raise NotImplementedError

    def getById(self, accountId: AccountId) -> Optional[Account]:
        raise NotImplementedError
