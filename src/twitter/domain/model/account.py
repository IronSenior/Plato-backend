from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from .account_name import AccountName
from .oauth_token import OauthToken
from .oauth_verifier import OauthVerifier
from .account_id import AccountId
from ....shared.domain.user_id import UserId
from ....shared.domain.brand_id import BrandId


class Account(Aggregate):

    def __init__(self, userId: UserId, brandId: BrandId, name: AccountName,
                 oauthToken: OauthToken, oauthVerifier: OauthVerifier, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self._userId: UserId = userId
        self._brandId: BrandId = brandId
        self._name: AccountName = name
        self._oauthToken: OauthToken = oauthToken
        self._oauthVerifier: OauthVerifier = oauthVerifier

    @property
    def accountId(self):
        return self._id

    @property
    def brandId(self):
        return self._brandId

    @property
    def name(self):
        return self._name

    @property
    def oauthToken(self):
        return self._oauthToken

    @property
    def oauthVerifier(self):
        return self._oauthVerifier

    @property
    def userId(self):
        return self._userId

    @classmethod
    def add(cls, accountId: AccountId, brandId: BrandId,
            name: AccountName, userId: UserId,
            oauthToken: OauthToken, oauthVerifier: OauthVerifier):
        return cls._create(
            cls.AccountWasAdded,
            id=accountId.value,
            brandId=brandId,
            name=name.value,
            oauthToken=oauthToken.value,
            oauthVerifier=oauthVerifier,
            userId=str(userId.value)
        )

    class AccountWasAdded(AggregateCreated):
        bus_string = "TWITTER_ACCOUNT_WAS_ADDED"
        brandId: str
        userId: str
        name: str
        oauthToken: str
        oauthVerifier: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            account = super().mutate(obj)
            account._brandId = self.brandId
            account._userId = self.userId
            account._name = self.name
            account._oauthToken = self.oauthToken
            account._oauthVerifier = self.oauthVerifier
            return account
