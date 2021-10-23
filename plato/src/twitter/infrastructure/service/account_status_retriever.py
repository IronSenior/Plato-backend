import os
import tweepy
from tweepy import OAuthHandler, TweepError
from ...domain.account_report.service.account_status_retriever import AccountStatusRetriever
from ...application.account_dto import AccountDTO
from ...application.account_status_dto import AccountStatusDTO


class AccountStatusRetriever(AccountStatusRetriever):

    def __init__(self) -> None:
        self.__outhHandler: OAuthHandler = OAuthHandler(
            os.environ["TWITTER_CONSUMER_KEY"],
            os.environ["TWITTER_CONSUMER_SECRET"]
        )

    def withAccount(self, account: AccountDTO) -> AccountStatusDTO:
        self.__outhHandler.set_access_token(
            account["accessToken"],
            account["accessSecret"]
        )
        api_connection = tweepy.API(self.__outhHandler)
        try:
            accountStatus = api_connection.get_user(account["name"])
        except TweepError:
            pass  # TODO: Manage errors
        return AccountStatusDTO(
            followers_count=accountStatus.followers_count,
            friends_count=accountStatus.friends_count
        )
