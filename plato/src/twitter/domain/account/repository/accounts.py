from abc import ABC
from typing import Optional
from ..model.account import Account
from ..model.account_id import AccountId


class Accounts(ABC):

    def save(self, account: Account) -> None:
        raise NotImplementedError

    def getById(self, accountId: AccountId) -> Optional[Account]:
        raise NotImplementedError
