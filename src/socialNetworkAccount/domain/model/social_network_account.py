from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from .social_network_account_name import SocialNetworkAccountName
from .user_token import UserToken
from .social_network import SocialNetwork
from .social_network_account_id import SocialNetworkAccountId
from ....user.domain.model.user_id import UserId


class SocialNetworkAccount(Aggregate):

    def __init__(self, userId: UserId, name: SocialNetworkAccountName,
                 userToken: UserToken, socialNetwork: SocialNetwork, *args, **kwargs):
        super(SocialNetworkAccount, self).__init__(*args, **kwargs)
        self._userId: UserId = userId
        self._name: SocialNetworkAccountName = name
        self._userToken: userToken = userToken
        self._socialNetwork: SocialNetwork = socialNetwork

    @property
    def accountId(self):
        return self._id

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
    def add(cls, accountId: SocialNetworkAccountId, userId: UserId,
            name: SocialNetworkAccountName, userToken: UserToken, socialNetwork: SocialNetwork):
        return cls._create(
            cls.SocialNetworkAccountWasAdded,
            id=accountId.value,
            name=name.value,
            userToken=userToken.value,
            userId=str(userId.value),
            socialNetwork=socialNetwork.value
        )

    class SocialNetworkAccountWasAdded(AggregateCreated):
        bus_string = "SOCIAL_NETWORK_ACCOUNT_WAS_ADDED"
        name: str
        userToken: str
        userId: str
        socialNetwork: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            account = super().mutate(obj)
            account._userId = self.userId
            account._name = self.name
            account._userToken = self.userToken
            account._socialNetwork = self.socialNetwork
