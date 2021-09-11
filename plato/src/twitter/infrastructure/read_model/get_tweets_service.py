from ...application.service.get_tweets_service import GetTweetsService
from ...domain.account.model.account_id import AccountId
import datetime
import pymongo
import os


class GetTweetsMongoService(GetTweetsService):

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["tweets"]

    def getPendingTweets(self):
        tweets = self.__db.find({
            "published": False,
            "publicationDate": {"$lt": datetime.datetime.now().timestamp()}
        })
        return list(tweets)

    def getTweetsByAccount(self, accountId: AccountId,
                           afterDate: float, beforeDate: float):
        tweets = self.__db.find({
            "accountId": str(accountId.value),
            "publicationDate": {"$gt": afterDate, "$lt": beforeDate}
        })
        return list(tweets)
