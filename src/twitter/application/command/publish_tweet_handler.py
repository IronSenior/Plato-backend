from simpleCQRS import CommandHandler
from .publish_tweet_command import PublishTweetCommand
from ...domain.tweet.repository.tweets import Tweets
from ...domain.tweet.model.tweet import Tweet
from ...domain.tweet.model.tweet_id import TweetId
from ...domain.tweet.exceptions.tweet_not_found import TweetNotFound
from ...domain.tweet.service.tweet_publisher import TweetPublisher
from dependency_injector.wiring import inject, Provide


class PublishTweetHandler(CommandHandler):

    @inject
    def __init__(self, tweets: Tweets = Provide["TWEETS"],
                 tweetPublisher: TweetPublisher = Provide["TWEET_PUBLISHER"]):
        self.__tweets: Tweets = tweets
        self.__tweetPublisher: TweetPublisher = tweetPublisher

    def handle(self, cmd: PublishTweetCommand):
        tweetId = TweetId.fromString(cmd.tweetId)
        tweet = self.__tweets.getById(tweetId)

        if type(tweet) != Tweet:
            raise TweetNotFound(tweetId)

        self.__tweetPublisher.publishTweet(tweet)
        tweet.publish()
        self.__tweets.save(tweet)
