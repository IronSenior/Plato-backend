from .add_tweet_media_command import AddTweetMediaCommand
from ...domain.tweet.repository.tweets import Tweets
from ...domain.tweet.model.tweet_id import TweetId
from ...domain.tweet.model.tweet import Tweet
from dependency_injector.wiring import Provide, inject
from plato_cqrs import CommandHandler


class AddTweetMediaHandler(CommandHandler):

    @inject
    def __init__(self, tweets: Tweets = Provide["TWEETS"]):
        self.__tweets: Tweets = tweets

    def handle(self, cmd: AddTweetMediaCommand):
        tweetId: TweetId = TweetId.fromString(cmd.tweetId)

        tweet: Tweet = self.__tweets.getById(tweetId)

        if not tweet:
            return None

        tweet.addMedia(cmd.media)
        self.__tweets.save(tweet)
