from ....user.domain.model.user_id import UserId
from ...domain.model.social_network_group import SocialNetworkGroup
from ..mapper.sn_group_mapper import SocialNetworkGroupMapper
from typing import List, Optional
from ...domain.repository.social_network_groups import SocialNetworkGroups
from ....shared.plato_command_bus import PlatoCommandBus
from ...application.sn_group_dto import SNGroupDTO
from ...application.command.create_social_network_group_command import CreateSocialNetworkGroupCommand
from dependency_injector.wiring import inject, Provide


class SocialNetworkGroupService:

    @inject
    def __init__(self, socialNetworkGroups: SocialNetworkGroups = Provide["SOCIAL_NETWORK_GROUPS"]):
        self.socialNetworkGroups: SocialNetworkGroups = socialNetworkGroups

    def createSNGroup(self, snGroupDto: SNGroupDTO) -> None:
        PlatoCommandBus.publish(
            CreateSocialNetworkGroupCommand(
                id=snGroupDto["id"],
                userId=snGroupDto["userid"],
                name=snGroupDto["name"],
                image=snGroupDto["image"]
            )
        )

    def getByUserId(self, userid: str) -> Optional[List[SocialNetworkGroup]]:
        userId = UserId.fromString(userid)
        groups = self.socialNetworkGroups.getByUserId(userId)
        groups_list = list(map(SocialNetworkGroupMapper.from_aggregate_to_dto, groups))
        return dict(zip(list(map(lambda group: group["id"], groups_list)), groups_list))
