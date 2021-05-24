from typing import TypedDict


class TweetDTO(TypedDict):

    tweetId: str
    accountId: str
    description: str
    publicationDate: int
