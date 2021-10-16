from plato_cqrs import QueryHandler
from .get_published_tweets_query import GetPublishedTweetsQuery
from .get_published_tweets_response import GetPublishedTweetsResponse
from dependency_injector.wiring import inject, Provide
from ..service.get_tweets_service import GetTweetsService


class GetPublishedTweetsHandler(QueryHandler):

    @inject
    def __init__(self, getTweetsService: GetTweetsService = Provide["GET_TWEETS_SERVICE"]):
        self.__getTweetsService: GetTweetsService = getTweetsService

    def handle(self, query: GetPublishedTweetsQuery) -> GetPublishedTweetsResponse:
        tweets = self.__getTweetsService.getPublishedTweets()

        getPublishedTweetsResponse = GetPublishedTweetsResponse()
        for tweet in tweets:
            getPublishedTweetsResponse.appendTweet(
                tweetId=tweet["tweetId"],
                accountId=tweet["accountId"],
                publicationDate=tweet["publicationDate"],
                description=tweet["description"],
                published=tweet["published"]
            )

        return getPublishedTweetsResponse
