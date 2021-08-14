from ...domain.tweet.service.tweet_publisher import TweetPublisher
from ...domain.tweet.model.tweet import Tweet


class DummyTweetPublisher(TweetPublisher):

    def __init__(self):
        self.called = 0
        self.called_with = []

    def publishTweet(self, tweet: Tweet):
        self.called += 1
        self.called_with.append(tweet)
