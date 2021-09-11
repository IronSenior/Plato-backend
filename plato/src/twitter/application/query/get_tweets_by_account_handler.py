from plato_cqrs import QueryHandler
from ..service.get_tweets_service import GetTweetsService
from ...domain.account.model.account_id import AccountId
from dependency_injector.wiring import inject, Provide
from .get_tweets_by_account_query import GetTweetsByAccountQuery
from .get_tweets_by_account_response import GetTweetsByAccountResponse


class GetTweetsByAccountHandler(QueryHandler):

    @inject
    def __init__(self, getTweetsService: GetTweetsService = Provide["GET_TWEETS_SERVICE"]):
        self.__getTweetsService: GetTweetsService = getTweetsService

    def handle(self, query: GetTweetsByAccountQuery) -> GetTweetsByAccountResponse:
        tweets = self.__getTweetsService.getTweetsByAccount(
            accountId=AccountId.fromString(query.accountId),
            afterDate=query.afterDate,
            beforeDate=query.beforeDate
        )
        getTweetsByAccountResponse = GetTweetsByAccountResponse()
        for tweet in tweets:
            getTweetsByAccountResponse.appendTweet(
                tweetId=tweet["tweetId"],
                accountId=tweet["accountId"],
                description=tweet["description"],
                publicationDate=tweet["publicationDate"],
                published=tweet["published"]
            )

        return getTweetsByAccountResponse
