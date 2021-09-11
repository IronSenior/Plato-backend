from abc import ABC
from typing import List
from ...domain.account.model.account_id import AccountId
from ..account_dto import AccountDTO
from ....shared.domain.user_id import UserId


class GetTwitterAccountService(ABC):

    def getAccountById(self, accountId: AccountId) -> AccountDTO:
        raise NotImplementedError()

    def getAccountByUserId(self, userId: UserId) -> List[AccountDTO]:
        raise NotImplementedError()
