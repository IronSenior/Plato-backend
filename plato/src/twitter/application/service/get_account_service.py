from abc import ABC
from typing import List
from ....shared.domain.brand_id import BrandId
from ...domain.account.model.account_id import AccountId
from ..account_dto import AccountDTO
from ....shared.domain.user_id import UserId


class GetTwitterAccountService(ABC):

    def getAccountById(self, accountId: AccountId) -> AccountDTO:
        raise NotImplementedError()

    def getAccountByUserId(self, userId: UserId) -> List[AccountDTO]:
        raise NotImplementedError()

    def getAccountByBrandId(self, brandId: BrandId) -> AccountDTO:
        raise NotImplementedError()

    def getAllAccounts(self) -> List[AccountDTO]:
        raise NotImplementedError()
