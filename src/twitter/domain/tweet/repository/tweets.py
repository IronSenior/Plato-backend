from abc import ABC
from ..model.tweet_id import TweetId
from typing import List, Optional
from ..model.tweet import Tweet
from ...account.model.account_id import AccountId


class Tweets(ABC):

    def save(self, tweet: Tweet) -> None:
        raise NotImplementedError

    def getById(self, tweetId: TweetId) -> Optional[Tweet]:
        raise NotImplementedError

    def getByAccountId(self, accountId: AccountId) -> Optional[List[Tweet]]:
        raise NotImplementedError

    def getPendingTweets(self) -> Optional[List[Tweet]]:
        raise NotImplementedError
