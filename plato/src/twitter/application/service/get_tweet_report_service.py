from abc import ABC
from ...domain.tweet.model.tweet_id import TweetId


class GetTweetReportsService(ABC):

    def getTweetReportsByTweet(self, tweetId: TweetId,
                               afterDate: int, beforeDate: int):
        raise NotImplementedError()
