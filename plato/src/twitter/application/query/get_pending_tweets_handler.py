from plato_cqrs import QueryHandler
from dependency_injector.wiring import Provide, inject
from ...domain.tweet.repository.tweets import Tweets
from .get_pending_tweets_query import GetPendingTweetsQuery
from .get_pending_tweets_response import GetPendingTweetsResponse


class GetPendingTweetsHandler(QueryHandler):

    @inject
    def __init__(self, tweets: Tweets = Provide["TWEETS"]):
        self.__tweets: Tweets = tweets

    def handle(self, query: GetPendingTweetsQuery) -> GetPendingTweetsResponse:
        tweets = self.__tweets.getPendingTweets()

        if not tweets:
            return None

        return GetPendingTweetsResponse(tweets=tweets)
