from typing import TypedDict


class TweetStatusDTO(TypedDict):
    retweet_count: int
    favorite_count: int
    quote_count: int
    reply_count: int
    impression_count: int
    profile_click_count: int
