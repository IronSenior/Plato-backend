from datetime import datetime
from .twitter_credential_retriever import TwitterCredentialRetriever
from ...application.account_dto import AccountDTO
from ..tweet_dto import TweetDTO
from ...application.command.add_account_command import AddAccountCommand
from ...application.query.get_account_query import GetAccountQuery
from ...application.query.get_account_by_brand_query import GetAccountByBrandQuery
from ...application.query.get_account_response import GetAccountResponse
from ...application.query.get_pending_tweets_query import GetPendingTweetsQuery
from ...application.query.get_pending_tweets_response import GetPendingTweetsResponse
from ...application.command.publish_tweet_command import PublishTweetCommand
from ...application.command.schedule_tweet_command import ScheduleTweetCommand
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ....shared.infrastructure.plato_query_bus import PlatoQueryBus
from ...application.query.get_tweets_by_account_query import GetTweetsByAccountQuery
from ...application.query.get_tweets_by_account_response import GetTweetsByAccountResponse
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

    def getTweetsByAccount(self, accountId: str, afterDate: float, beforeDate: float):
        tweetsResponse: GetTweetsByAccountResponse = PlatoQueryBus.publish(
            GetTweetsByAccountQuery(accountId, afterDate, beforeDate)
        )
        if not tweetsResponse:
            return None
        return tweetsResponse.tweets

    def publishScheduledTweets(self):
        my_time = datetime.now().timestamp()
        tweetsResponse: GetPendingTweetsResponse = PlatoQueryBus.publish(
            GetPendingTweetsQuery(publicationDate=my_time)
        )
        for tweetId in tweetsResponse.tweets.keys():
            PlatoCommandBus.publish(
                PublishTweetCommand(tweetId)
            )
