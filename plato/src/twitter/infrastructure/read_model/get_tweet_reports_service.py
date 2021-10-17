from ...application.service.get_tweet_report_service import GetTweetReportsService
from ...domain.tweet.model.tweet_id import TweetId
import pymongo
import os


class GetTweetReportsMongoService(GetTweetReportsService):

    def __init__(self):
        self.__client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        self.__db = self.__client[os.environ["MONGODB_DBNAME"]]["tweet_reports"]

    def getTweetReportsByTweet(self, tweetId: TweetId, afterDate: int, beforeDate: int):
        reports = self.__db.find({
            "tweetId": str(tweetId.value),
            "reportDate": {"$gt": afterDate, "$lt": beforeDate}
        })
        return list(reports)
