from ...domain.model.social_network_group import SocialNetworkGroup
from ...domain.model.social_network_group_id import SocialNetworkGroupId
from ...domain.repository.social_network_groups import SocialNetworkGroups
from ....user.domain.model.user_id import UserId
from ....shared.plato_event_bus import PlatoEventBus
from eventsourcing.application import Application
from typing import Optional, List


class SocialNetworkGroupRepository(Application, SocialNetworkGroups):

    def __init__(self):
        self.__groups: List[SocialNetworkGroup] = []
        return super(SocialNetworkGroupRepository, self).__init__()

    def save(self, socialNetworkGroup: SocialNetworkGroup) -> None:
        super(SocialNetworkGroupRepository, self).save(socialNetworkGroup)
        self.__groups.append(socialNetworkGroup)
        for event in socialNetworkGroup.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, id: SocialNetworkGroupId) -> Optional[SocialNetworkGroup]:
        try:
            return self.repository.get(id.value)
        except Exception:
            return None

    def getByUserId(self, userId: UserId) -> Optional[List[SocialNetworkGroup]]:
        groups = []
        for group in self.__groups:
            if group.userId == userId.value:
                groups.append(group)
        return groups
