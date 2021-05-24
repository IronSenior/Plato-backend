
from ..exceptions.too_long_tweet import TooLongTweet


TWITTER_MAX_LENGTH = 280


class TweetDescription:

    def __init__(self, description: str):
        self.check_tweet_length(description)
        self.__value: str = description

    @property
    def value(self):
        return self.__value

    @staticmethod
    def fromString(description: str):
        return TweetDescription(description)

    def check_tweet_length(self, description: str):
        if len(description) > TWITTER_MAX_LENGTH:
            raise TooLongTweet()
