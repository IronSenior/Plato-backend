from abc import ABC, abstractmethod
from ..model.tweet import Tweet


class TweetPublisher(ABC):

    @abstractmethod
    def publishTweet(self, tweet: Tweet):
        raise NotImplementedError()
