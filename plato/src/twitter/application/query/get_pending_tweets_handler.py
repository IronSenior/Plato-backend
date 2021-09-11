from plato_cqrs import QueryHandler
from .get_pending_tweets_query import GetPendingTweetsQuery
from .get_pending_tweets_response import GetPendingTweetsResponse
from dependency_injector.wiring import inject, Provide
from ..service.get_tweets_service import GetTweetsService


class GetPendingTweetsHandler(QueryHandler):

    @inject
    def __init__(self, getTweetsService: GetTweetsService = Provide["GET_TWEETS_SERVICE"]):
        self.__getTweetsService: GetTweetsService = getTweetsService

    def handle(self, query: GetPendingTweetsQuery) -> GetPendingTweetsResponse:
        tweets = self.__getTweetsService.getPendingTweets()

        getPendingTweetsResponse = GetPendingTweetsResponse()
        for tweet in tweets:
            getPendingTweetsResponse.appendTweet(
                tweetId=tweet["tweetId"],
                accountId=tweet["accountId"],
                publicationDate=tweet["publicationDate"],
                description=tweet["description"],
                published=tweet["published"]
            )

        return getPendingTweetsResponse
