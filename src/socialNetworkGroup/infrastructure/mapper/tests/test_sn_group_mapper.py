import unittest
import faker
from uuid import uuid4
from unittest.mock import Mock
from ..sn_group_mapper import SocialNetworkGroupMapper
from ....domain.model.social_network_group import SocialNetworkGroup
from .....user.domain.model.user_id import UserId
from ....domain.model.social_network_group_id import SocialNetworkGroupId
from ....domain.model.social_network_group_image import SocialNetworkGroupImageUrl
from ....domain.model.social_network_group_name import SocialNetworkGroupName
from ....application.sn_group_dto import SNGroupDTO

fake = faker.Faker()


class TestUserMapper(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedUserRepository = Mock()
        return super(TestUserMapper, self).setUp()

    def test_from_user_to_dto(self):
        groupid = SocialNetworkGroupId.fromString(str(uuid4()))
        userid = UserId.fromString(str(uuid4()))
        name = SocialNetworkGroupName.fromString(fake.company())
        image = SocialNetworkGroupImageUrl.fromString(fake.image_url())
        group = SocialNetworkGroup.add(
            id=groupid,
            userId=userid,
            name=name,
            image=image
        )
        groupDto: SNGroupDTO = SocialNetworkGroupMapper.from_aggregate_to_dto(group)
        self.assertEqual(str(userid.value), groupDto["userid"])
        self.assertEqual(str(groupid.value), groupDto["id"])
        self.assertEqual(name.value, groupDto["name"])
        self.assertEqual(image.value, groupDto["image"])
