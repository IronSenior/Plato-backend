from ...domain.repository.social_network_groups import SocialNetworkGroups
from ...domain.model.social_network_group_id import SocialNetworkGroupId
from ...domain.model.social_network_group_name import SocialNetworkGroupName
from ...domain.model.social_network_group import SocialNetworkGroup
from ...domain.model.social_network_group_image import SocialNetworkGroupImageUrl
from ....user.domain.model.user_id import UserId
from ...domain.exceptions.social_network_group_id_aready_registered import SocialNetworkGroupIdAlreadyRegistered
from .create_social_network_group_command import CreateSocialNetworkGroupCommand
from commandbus import CommandHandler
from dependency_injector.wiring import inject, Provide


class CreateSocialNetworkGroupHandler(CommandHandler):

    @inject
    def __init__(self, socialNetworikGroups: SocialNetworkGroups = Provide["SOCIAL_NETWORK_GROUPS"]):
        self.socialNetworikGroups: SocialNetworkGroups = socialNetworikGroups

    def handle(self, cmd: CreateSocialNetworkGroupCommand):
        snGroupId = SocialNetworkGroupId.fromString(cmd.id)

        if (type(self.socialNetworikGroups.getById(snGroupId)) == SocialNetworkGroup):
            raise SocialNetworkGroupIdAlreadyRegistered("Social Network Id already registered")

        socialNetworkGroup = SocialNetworkGroup.add(
            id=snGroupId,
            userId=UserId.fromString(cmd.userId),
            name=SocialNetworkGroupName.fromString(cmd.name),
            image=SocialNetworkGroupImageUrl.fromString(cmd.image)
        )
        self.socialNetworikGroups.save(socialNetworkGroup)
