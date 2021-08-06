from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from .account_name import AccountName
from .access_token import AccessToken
from .access_token_secret import AccessTokenSecret
from .account_id import AccountId
from .....shared.domain.user_id import UserId
from .....shared.domain.brand_id import BrandId


class Account(Aggregate):

    def __init__(self, userId: UserId, brandId: BrandId, name: AccountName,
                 accessToken: AccessToken, accessTokenSecret: AccessTokenSecret, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self._userId: UserId = userId
        self._brandId: BrandId = brandId
        self._name: AccountName = name
        self._accessToken: AccessToken = accessToken
        self._accessTokenSecret: AccessTokenSecret = accessTokenSecret

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
    def accessToken(self):
        return self._accessToken

    @property
    def accessTokenSecret(self):
        return self._accessTokenSecret

    @property
    def userId(self):
        return self._userId

    @classmethod
    def add(cls, accountId: AccountId, brandId: BrandId,
            name: AccountName, userId: UserId,
            accessToken: AccessToken, accessTokenSecret: AccessTokenSecret):
        return cls._create(
            cls.AccountWasAdded,
            id=accountId.value,
            brandId=str(brandId.value),
            name=name.value,
            accessToken=accessToken.value,
            accessTokenSecret=accessTokenSecret.value,
            userId=str(userId.value)
        )

    class AccountWasAdded(AggregateCreated):
        bus_string = "TWITTER_ACCOUNT_WAS_ADDED"
        brandId: str
        userId: str
        name: str
        accessToken: str
        accessTokenSecret: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            account = super().mutate(obj)
            account._brandId = self.brandId
            account._userId = self.userId
            account._name = self.name
            account._accessToken = self.accessToken
            account._accessTokenSecret = self.accessTokenSecret
            return account
