from dependency_injector.wiring import Provide, inject
import tweepy
from tweepy import OAuthHandler, TweepError
import os
from ...domain.tweet_report.service.tweet_status_retriever import TweetStatusRetriever
from ...domain.account.model.account_id import AccountId
from ...application.service.get_account_service import GetTwitterAccountService


class TweetStatusTweepyRetriever(TweetStatusRetriever):

    @inject
    def __init__(self, accounts: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"]):
        self.__accounts: GetTwitterAccountService = accounts
        self.__outhHandler: OAuthHandler = OAuthHandler(
            os.environ["TWITTER_CONSUMER_KEY"],
            os.environ["TWITTER_CONSUMER_SECRET"]
        )

    def withTweet(self, tweet: dict) -> dict:
        account = self.__accounts.getAccountById(AccountId.fromString(str(tweet["accountId"])))
        self.__outhHandler.set_access_token(account["accessToken"], account["accessSecret"])
        api_connection = tweepy.API(self.__outhHandler)

        if not tweet.get("twitterRef", False):
            return None

        try:
            status = api_connection.get_status(id=tweet["twitterRef"])
        except TweepError:
            return None

        return {
            "retweet_count": status.retweet_count,
            "favorite_count": status.favorite_count,
            "quote_count": 0,
            "reply_count": 0
        }
