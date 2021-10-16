from abc import ABC
from ...domain.account.model.account_id import AccountId
from ...domain.tweet.model.tweet_id import TweetId


class GetTweetsService(ABC):

    def getPendingTweets(self):
        raise NotImplementedError()

    def getTweetsByAccount(self, accountId: AccountId,
                           afterDate: float, beforeDate: float):
        raise NotImplementedError()

    def getTweetById(self, tweetId: TweetId):
        raise NotImplementedError()

    def getPublishedTweets(self):
        raise NotImplementedError()
