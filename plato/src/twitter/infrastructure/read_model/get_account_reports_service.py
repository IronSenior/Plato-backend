from ...application.service.get_account_report_service import GetAccountReportsService
from ...domain.account.model.account_id import AccountId
import pymongo
import os


class GetAccountReportsMongoService(GetAccountReportsService):

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["account_reports"]

    def getAccountReportsByAccount(self, accountId: AccountId, afterDate: int, beforeDate: int):
        reports = self.__db.find({
            "accountId": str(accountId.value),
            "reportDate": {"$gt": afterDate, "$lt": beforeDate}
        })
        return list(reports)
