from typing import TypedDict


class AccountDTO(TypedDict):
    accountId: str
    userId: str
    brandId: str
    name: str
    accessToken: str
    accessTokenSecret: str
