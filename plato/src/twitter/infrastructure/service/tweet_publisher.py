from dependency_injector.wiring import Provide, inject
from ...domain.tweet.service.tweet_publisher import TweetPublisher
from ...domain.tweet.model.tweet import Tweet
from ...domain.account.model.account_id import AccountId
from ...domain.account.repository.accounts import Accounts
import tweepy
from tweepy import OAuthHandler
import os


class TweepyTweetPublisher(TweetPublisher):

    @inject
    def __init__(self, accounts: Accounts = Provide["TWITTER_ACCOUNTS"]):
        self.__accounts: Accounts = accounts
        self.__outhHandler: OAuthHandler = OAuthHandler(
            os.environ["TWITTER_CONSUMER_KEY"],
            os.environ["TWITTER_CONSUMER_SECRET"]
        )

    def publishTweet(self, tweet: Tweet):
        account = self.__accounts.getById(AccountId.fromString(str(tweet.accountId)))
        self.__outhHandler.set_access_token(account.accessToken, account.accessTokenSecret)
        api_connection = tweepy.API(self.__outhHandler)
        api_connection.verify_credentials()
        api_connection.update_status(status=tweet.description)
