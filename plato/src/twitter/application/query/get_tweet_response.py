from plato_cqrs import QueryResponse


class GetTweetResponse(QueryResponse):

    def __init__(self, tweet: dict):
        self.__tweet: dict = tweet

    @property
    def tweet(self):
        return self.__tweet
