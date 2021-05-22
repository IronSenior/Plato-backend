from typing import TypedDict


class TwitterAccountDTO(TypedDict):

    accountId: str
    brandId: str
    userId: str
    oauthToken: str
    oauthVerifier: str
