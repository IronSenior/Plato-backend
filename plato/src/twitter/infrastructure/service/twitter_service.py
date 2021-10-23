from datetime import datetime
from .twitter_credential_retriever import TwitterCredentialRetriever
from ...application.account_dto import AccountDTO
from ..tweet_dto import TweetDTO
from ...application.command.add_account_command import AddAccountCommand
from ...application.query.get_account_query import GetAccountQuery
from ...application.query.get_account_by_brand_query import GetAccountByBrandQuery
from ...application.query.get_account_response import GetAccountResponse
from ...application.command.create_tweet_report_command import CreateTweetReportCommand
from ...application.query.get_pending_tweets_query import GetPendingTweetsQuery
from ...application.query.get_pending_tweets_response import GetPendingTweetsResponse
from ...application.query.get_published_tweets_query import GetPublishedTweetsQuery
from ...application.query.get_published_tweets_response import GetPublishedTweetsResponse
from ...application.command.publish_tweet_command import PublishTweetCommand
from ...application.command.schedule_tweet_command import ScheduleTweetCommand
from ...application.command.create_account_report_command import CreateAccountReportCommand
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ....shared.infrastructure.plato_query_bus import PlatoQueryBus
from ...application.query.get_tweets_by_account_query import GetTweetsByAccountQuery
from ...application.query.get_tweets_by_account_response import GetTweetsByAccountResponse
from ...application.query.get_tweet_report_by_tweet_query import GetTweetReportsByTweetQuery
from ...application.query.get_tweet_report_by_tweet_response import GetTweetReportsByTweetResponse
from ...application.query.get_tweet_query import GetTweetQuery
from ...application.query.get_tweet_response import GetTweetResponse
from ...application.query.get_all_accounts_query import GetAllAccountsQuery
from ...application.query.get_accounts_response import GetAccountsResponse
from ...application.query.get_account_reports_by_account_query import GetAccountReportsByAccountQuery
from ...application.query.get_account_reports_by_account_response import GetAccountReportsByAccountResponse
from ..mapper.account_mapper import AccountMapper
from tweepy import OAuthHandler
import tweepy
import os


class TwitterService:

    def __init__(self):
        self.__consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
        self.__consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]

    def requestToken(self, callbackUrl: str):
        oauthHandler: OAuthHandler = OAuthHandler(
            self.__consumerKey,
            self.__consumerSecret,
            callback=callbackUrl
        )
        authUrl = oauthHandler.get_authorization_url()
        TwitterCredentialRetriever().saveCredentials(
            token=oauthHandler.request_token["oauth_token"],
            secret=oauthHandler.request_token["oauth_token_secret"]
        )
        return authUrl

    def addTwitterAccount(self, account: AccountDTO):
        oauthHandler: OAuthHandler = OAuthHandler(self.__consumerKey, self.__consumerSecret)
        oauthHandler.request_token = {
            'oauth_token': account["oauthToken"],
            'oauth_token_secret': TwitterCredentialRetriever().getSecretByToken(account["oauthToken"])
        }

        oauthHandler.get_access_token(verifier=account["oauthVerifier"])
        apiConnection = tweepy.API(oauthHandler)
        user = apiConnection.verify_credentials()

        PlatoCommandBus.publish(AddAccountCommand(
            accountId=account["accountId"],
            brandId=account["brandId"],
            name=user.screen_name,
            userId=account["userId"],
            accessToken=oauthHandler.access_token,
            accessTokenSecret=oauthHandler.access_token_secret
        ))

    def scheduleTweet(self, tweet: TweetDTO):
        PlatoCommandBus.publish(
            ScheduleTweetCommand(
                tweetId=tweet["tweetId"],
                accountId=tweet["accountId"],
                description=tweet["description"],
                publicationDate=tweet["publicationDate"]
            )
        )

    def getAccount(self, accountId: str):
        account: GetAccountResponse = PlatoQueryBus.publish(
            GetAccountQuery(accountId=accountId)
        )
        if not account:
            return None
        return AccountMapper.from_response_to_dto(account)

    def getAccountByBrand(self, brandId: str):
        account: GetAccountResponse = PlatoQueryBus.publish(
            GetAccountByBrandQuery(brandId=brandId)
        )
        if not account:
            return None
        return AccountMapper.from_response_to_dto(account)

    def getTweetsByAccount(self, accountId: str, afterDate: int, beforeDate: int):
        tweetsResponse: GetTweetsByAccountResponse = PlatoQueryBus.publish(
            GetTweetsByAccountQuery(accountId, afterDate, beforeDate)
        )
        if not tweetsResponse:
            return None
        return tweetsResponse.tweets

    def getTweetById(self, tweetId: str):
        tweetsResponse: GetTweetResponse = PlatoQueryBus.publish(
            GetTweetQuery(tweetId)
        )
        if not tweetsResponse:
            return None
        return tweetsResponse.tweet

    def publishScheduledTweets(self):
        my_time = int(datetime.now().timestamp() * 1000)
        tweetsResponse: GetPendingTweetsResponse = PlatoQueryBus.publish(
            GetPendingTweetsQuery(publicationDate=my_time)
        )
        for tweetId in tweetsResponse.tweets.keys():
            PlatoCommandBus.publish(
                PublishTweetCommand(tweetId)
            )

    def generateTweetsReports(self):
        tweetsReponse: GetPublishedTweetsResponse = PlatoQueryBus.publish(
            GetPublishedTweetsQuery()
        )
        for tweetId in tweetsReponse.tweets.keys():
            PlatoCommandBus.publish(
                CreateTweetReportCommand(tweetId)
            )

    def getTweetReportsByTweet(self, tweetId: str, afterDate: int, beforeDate: int):
        reportsResponse: GetTweetReportsByTweetResponse = PlatoQueryBus.publish(
            GetTweetReportsByTweetQuery(tweetId, afterDate, beforeDate)
        )
        if not reportsResponse:
            return None
        return reportsResponse.reports

    def generateAccountReport(self):
        accountsResponse: GetAccountsResponse = PlatoQueryBus.publish(
            GetAllAccountsQuery()
        )
        accountsIds = map(
            lambda account: account["accountId"],
            accountsResponse.accounts
        )
        for accountId in accountsIds:
            PlatoCommandBus.publish(
                CreateAccountReportCommand(accountId)
            )

    def getAccountReportsByAccount(self, accountId: str, afterDate: int, beforeDate: int):
        reportsResponse: GetAccountReportsByAccountResponse = PlatoQueryBus.publish(
            GetAccountReportsByAccountQuery(accountId, afterDate, beforeDate)
        )
        if not reportsResponse:
            return None
        return reportsResponse.reports
