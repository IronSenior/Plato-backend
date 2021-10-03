from ...application.service.get_account_service import GetTwitterAccountService
from ...application.account_dto import AccountDTO
from ...domain.account.model.account_id import AccountId
from ....shared.domain.user_id import UserId
from ....shared.domain.brand_id import BrandId
from typing import List
import pymongo
import os


class GetTwitterAccountMongoService(GetTwitterAccountService):

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["twitter_accounts"]

    def getAccountByUserId(self, userId: UserId) -> List[AccountDTO]:
        accounts = list(self.__db.find({"userId": str(userId.value)}))
        return accounts

    def getAccountById(self, accountId: AccountId) -> AccountDTO:
        account = self.__db.find_one({"accountId": str(accountId.value)})
        return account

    def getAccountByBrandId(self, brandId: BrandId) -> AccountDTO:
        account = self.__db.find_one({"brandId": str(brandId.value)})
        return account
