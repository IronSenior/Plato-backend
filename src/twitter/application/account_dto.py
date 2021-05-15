from typing import TypedDict


class AccountDTO(TypedDict):
    accountId: str
    userId: str
    socialNetwork: str
    name: str
    userToken: str
    brandId: str
