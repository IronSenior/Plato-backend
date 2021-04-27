

from ...application.sn_group_dto import SNGroupDTO
from ...domain.model.social_network_group import SocialNetworkGroup


class SocialNetworkGroupMapper:

    @staticmethod
    def from_aggregate_to_dto(snGroup: SocialNetworkGroup):
        return SNGroupDTO(
            id=str(snGroup.id),
            userid=str(snGroup.userId),
            name=snGroup.name,
            image=snGroup.image
        )
