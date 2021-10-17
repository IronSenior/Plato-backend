from plato_cqrs import QueryHandler
from ..service.get_tweets_service import GetTweetsService
from ...domain.tweet.model.tweet_id import TweetId
from dependency_injector.wiring import inject, Provide
from .get_tweet_query import GetTweetQuery
from .get_tweet_response import GetTweetResponse


class GetTweetHandler(QueryHandler):

    @inject
    def __init__(self, getTweetsService: GetTweetsService = Provide["GET_TWEETS_SERVICE"]):
        self.__getTweetsService: GetTweetsService = getTweetsService

    def handle(self, query: GetTweetQuery) -> GetTweetResponse:
        tweet = self.__getTweetsService.getTweetById(
            tweetId=TweetId.fromString(query.tweetId)
        )
        return GetTweetResponse(tweet)
