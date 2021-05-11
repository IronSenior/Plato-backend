from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from .account_name import AccountName
from .user_token import UserToken
from .social_network import SocialNetwork
from .account_id import AccountId
from ....shared.domain.user_id import UserId
from ....brand.domain.model.brand_id import BrandId


class Account(Aggregate):

    def __init__(self, userId: UserId, brandId: BrandId, name: AccountName,
                 userToken: UserToken, socialNetwork: SocialNetwork, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self._userId: UserId = userId
        self._brandId: BrandId = brandId
        self._name: AccountName = name
        self._userToken: userToken = userToken
        self._socialNetwork: SocialNetwork = socialNetwork

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
    def userToken(self):
        return self._userToken

    @property
    def userId(self):
        return self._userId

    @property
    def socialNetwork(self):
        return self._socialNetwork

    @classmethod
    def add(cls, accountId: AccountId, brandId: AccountId,
            name: AccountName, userId: UserId,
            userToken: UserToken, socialNetwork: SocialNetwork):
        return cls._create(
            cls.AccountWasAdded,
            id=accountId.value,
            brandId=brandId,
            name=name.value,
            userToken=userToken.value,
            userId=str(userId.value),
            socialNetwork=socialNetwork.value
        )

    class AccountWasAdded(AggregateCreated):
        bus_string = "ACCOUNT_WAS_ADDED"
        brandId: str
        name: str
        userToken: str
        userId: str
        socialNetwork: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            account = super().mutate(obj)
            account._brandId = self.brandId
            account._userId = self.userId
            account._name = self.name
            account._userToken = self.userToken
            account._socialNetwork = self.socialNetwork
            return account
