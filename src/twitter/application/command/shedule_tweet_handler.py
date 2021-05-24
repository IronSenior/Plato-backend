from datetime import datetime
from commandbus import CommandHandler
from dependency_injector.wiring import inject, Provide
from ...domain.tweet.repository.tweets import Tweets
from ...domain.tweet.model.tweet_id import TweetId
from ...domain.tweet.model.tweet import Tweet
from ...domain.tweet.model.tweet_description import TweetDescription
from ...domain.account.model.account_id import AccountId
from ...domain.tweet.exceptions.tweet_id_already_registered import TweetIdAlreadyRegistered
from .shedule_tweet_command import ScheduleTweetCommand


class ScheduleTweetHandler(CommandHandler):

    @inject
    def __init__(self, tweets: Tweets = Provide["TWEETS"]):
        self.__tweets: Tweets = tweets

    def handle(self, cmd: ScheduleTweetCommand):
        tweetId: TweetId = TweetId.fromString(cmd.tweetId)
        if type(self.__tweets.getById(tweetId)) is Tweet:
            raise TweetIdAlreadyRegistered("Tweet with ID ->", tweetId.value)

        tweet: Tweet = Tweet.add(
            tweetId=tweetId,
            accountId=AccountId.fromString(cmd.accountId),
            description=TweetDescription.fromString(cmd.description),
            publicationDate=datetime.fromtimestamp(cmd.publicationDate)
        )
        self.__tweets.save(tweet)
