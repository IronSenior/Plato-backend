from dependency_injector.wiring import Provide, inject
import requests
from requests_oauthlib import OAuth1
import os
from ...domain.tweet_report.service.tweet_status_retriever import TweetStatusRetriever
from ...domain.account.model.account_id import AccountId
from ...application.service.get_account_service import GetTwitterAccountService


class TweetStatusTweepyRetriever(TweetStatusRetriever):

    @inject
    def __init__(self, accounts: GetTwitterAccountService = Provide["GET_ACCOUNT_SERVICE"]):
        self.__accounts: GetTwitterAccountService = accounts

    def withTweet(self, tweet: dict) -> dict:
        if not tweet.get("twitterRef", False):
            return None

        account = self.__accounts.getAccountById(AccountId.fromString(str(tweet["accountId"])))
        auth = OAuth1(
            os.environ["TWITTER_CONSUMER_KEY"],
            os.environ["TWITTER_CONSUMER_SECRET"],
            account["accessToken"],
            account["accessSecret"]
        )
        twitterStatus = requests.get(
            f"https://api.twitter.com/2/tweets/{tweet['twitterRef']}?"
            "tweet.fields=organic_metrics,public_metrics",
            auth=auth
        )
        if twitterStatus.json().get("errors", False):
            return None

        tweetData = twitterStatus.json()["data"]
        return {
            "retweet_count": tweetData["organic_metrics"]["retweet_count"],
            "favorite_count": tweetData["organic_metrics"]["like_count"],
            "quote_count": tweetData["public_metrics"]["quote_count"],
            "reply_count": tweetData["organic_metrics"]["reply_count"],
            "impression_count": tweetData["organic_metrics"]["impression_count"],
            "profile_click_count": tweetData["organic_metrics"]["user_profile_clicks"]
        }
