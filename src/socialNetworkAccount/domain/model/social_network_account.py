from typing import Optional
from eventsourcing.domain import Aggregate, AggregateCreated
from .social_network_account_name import SocialNetworkAccountName
from .user_token import UserToken
from .social_network import SocialNetwork
from .social_network_account_id import SocialNetworkAccountId
from ....user.domain.model.user_id import UserId
from ....socialNetworkGroup.domain.model.social_network_group_id import SocialNetworkGroupId


class SocialNetworkAccount(Aggregate):

    def __init__(self, userId: UserId, snGroupId: SocialNetworkGroupId, name: SocialNetworkAccountName,
                 userToken: UserToken, socialNetwork: SocialNetwork, *args, **kwargs):
        super(SocialNetworkAccount, self).__init__(*args, **kwargs)
        self._userId: UserId = userId
        self._snGroupId: SocialNetworkGroupId = snGroupId
        self._name: SocialNetworkAccountName = name
        self._userToken: userToken = userToken
        self._socialNetwork: SocialNetwork = socialNetwork

    @property
    def accountId(self):
        return self._id

    @property
    def snGroupId(self):
        return self._snGroupId

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
    def add(cls, accountId: SocialNetworkAccountId, snGroupId: SocialNetworkAccountId,
            name: SocialNetworkAccountName, userId: UserId,
            userToken: UserToken, socialNetwork: SocialNetwork):
        return cls._create(
            cls.SocialNetworkAccountWasAdded,
            id=accountId.value,
            snGroupId=snGroupId,
            name=name.value,
            userToken=userToken.value,
            userId=str(userId.value),
            socialNetwork=socialNetwork.value
        )

    class SocialNetworkAccountWasAdded(AggregateCreated):
        bus_string = "SOCIAL_NETWORK_ACCOUNT_WAS_ADDED"
        snGroupId: str
        name: str
        userToken: str
        userId: str
        socialNetwork: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            account = super().mutate(obj)
            account._snGroupId = self.snGroupId
            account._userId = self.userId
            account._name = self.name
            account._userToken = self.userToken
            account._socialNetwork = self.socialNetwork
            return account
