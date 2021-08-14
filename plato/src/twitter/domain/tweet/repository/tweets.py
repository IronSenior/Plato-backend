from abc import ABC
from ..model.tweet_id import TweetId
from typing import Optional
from ..model.tweet import Tweet


class Tweets(ABC):

    def save(self, tweet: Tweet) -> None:
        raise NotImplementedError

    def getById(self, tweetId: TweetId) -> Optional[Tweet]:
        raise NotImplementedError
