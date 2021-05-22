from ...domain.repository.accounts import Accounts
from dependency_injector.wiring import inject, Provide
from ..twitter_account_dto import TwitterAccountDTO
from ...application.command.add_account_command import AddAccountCommand
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from tweepy import OAuthHandler, TweepError
import tweepy
import os

CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]


class TwitterAccountService:

    @inject
    def __init__(self, accounts: Accounts = Provide["TWITTER_ACCOUNTS"]):
        self.__accounts: Accounts = accounts
        self.__twitter: OAuthHandler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    def addTwitterAccount(self, account: TwitterAccountDTO):
        self.__twitter.request_token = {'oauth_token': account["oauthToken"],
                                        'oauth_token_secret': account["oauthVerifier"]}
        try:
            self.__twitter.get_access_token(account["oauthVerifier"])
            apiConnection = tweepy.API(self.__twitter)
            user = apiConnection.verify_credentials()
        except TweepError:
            return Exception

        PlatoCommandBus.publish(AddAccountCommand(
            accountId=account["accountId"],
            brandId=account["brandId"],
            name=user.screen_name,
            userId=account["userId"],
            accessToken=self.__twitter.access_token,
            accessTokenSecret=self.__twitter.access_token_secret
        ))
