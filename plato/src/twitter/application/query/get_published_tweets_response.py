from plato_cqrs import QueryResponse


class GetPublishedTweetsResponse(QueryResponse):

    def __init__(self, tweets: dict = None):
        self.__tweets: dict = tweets or {}

    @property
    def tweets(self):
        return self.__tweets

    def appendTweet(self, tweetId: str, accountId: str, description: str,
                    publicationDate: float, published: bool):
        self.__tweets.update({
            tweetId: {
                "accountId": accountId,
                "description": description,
                "publicationDate": publicationDate,
                "published": published
            }
        })
