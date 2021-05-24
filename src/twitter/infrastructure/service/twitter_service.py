from ...domain.account.repository.accounts import Accounts
from ...domain.account.model.account_id import AccountId
from dependency_injector.wiring import inject, Provide
from ..twitter_account_dto import TwitterAccountDTO
from ..tweet_dto import TweetDTO
from ...application.command.add_account_command import AddAccountCommand
from ...domain.tweet.repository.tweets import Tweets
from ...application.command.shedule_tweet_command import ScheduleTweetCommand
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ..mapper.account_mapper import AccountMapper
from tweepy import OAuthHandler
import tweepy
import os


class TwitterService:

    @inject
    def __init__(self, accounts: Accounts = Provide["TWITTER_ACCOUNTS"], tweets: Tweets = Provide["TWEETS"]):
        self.__accounts: Accounts = accounts
        self.__tweets: Tweets = tweets
        self.__consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
        self.__consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]

    # The twitter part should be done in an application service called by the command handler (?)
    def addTwitterAccount(self, account: TwitterAccountDTO):
        oauthHandler: OAuthHandler = OAuthHandler(self.__consumerKey, self.__consumerSecret)
        oauthHandler.request_token = {'oauth_token': account["oauthToken"],
                                      'oauth_token_secret': account["oauthTokenSecret"]}

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
        accountId = AccountId.fromString(accountId)
        account = self.__accounts.getById(accountId)
        if not account:
            return None
        return AccountMapper.from_aggregate_to_dto(account)

    # This method shoul call a command (?)
    def publishScheduledTweets(self):
        tweets = self.__tweets.getPendingTweets()
        for tweet in tweets:
            account = self.__accounts.getById(AccountId.fromString(str(tweet.accountId)))
            oauthHandler: OAuthHandler = OAuthHandler(self.__consumerKey, self.__consumerSecret)
            oauthHandler.set_access_token(account.accessToken, account.accessTokenSecret)
            api_connection = tweepy.API(oauthHandler)
            api_connection.verify_credentials()
            api_connection.update_status(status=tweet.description)
