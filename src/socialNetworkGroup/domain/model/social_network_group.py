from .social_network_group_id import SocialNetworkGroupId
from .social_network_group_image import SocialNetworkGroupImageUrl
from .social_network_group_name import SocialNetworkGroupName
from ....user.domain.model.user_id import UserId
from eventsourcing.domain import Aggregate, AggregateCreated
from typing import Optional


class SocialNetworkGroup(Aggregate):

    def __init__(self, userId: UserId, name: SocialNetworkGroupName,
                 image: SocialNetworkGroupImageUrl, *args, **kwargs) -> None:
        super(SocialNetworkGroup, self).__init__(*args, **kwargs)
        self._name: SocialNetworkGroupName = name
        self._userId: UserId = userId
        self._image: SocialNetworkGroupImageUrl = image

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name.value

    @property
    def userId(self):
        return self._userId.value

    @property
    def image(self):
        return self._image.value

    @classmethod
    def add(cls, id: SocialNetworkGroupId, userId: UserId,
            name: SocialNetworkGroupName, image: SocialNetworkGroupImageUrl):
        return cls._create(
            cls.SocialNetworkGroupWasCreated,
            id=id.value,
            userId=str(userId.value),
            name=name.value,
            image=image.value
        )

    class SocialNetworkGroupWasCreated(AggregateCreated):
        bus_string = "SOCIAL_NETWORK_GROUP_WAS_CREATED"
        userId: str
        name: str
        image: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            socialNetworkGroup = super().mutate(obj)
            socialNetworkGroup._userId = UserId.fromString(self.userId)
            socialNetworkGroup._name = SocialNetworkGroupName.fromString(self.name)
            socialNetworkGroup._image = SocialNetworkGroupImageUrl.fromString(self.image)
            return socialNetworkGroup
