from abc import ABC, abstractmethod
from ...tweet.model.tweet import Tweet


class TweetStatusRetriever(ABC):

    @abstractmethod
    def withTweet(self, tweet: Tweet) -> dict:
        raise NotImplementedError()
