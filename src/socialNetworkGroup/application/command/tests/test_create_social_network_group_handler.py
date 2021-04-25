import unittest
import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4
from ..create_social_network_group_handler import CreateSocialNetworkGroupHandler
from ..create_social_network_group_command import CreateSocialNetworkGroupCommand
from ....domain.model.social_network_group import SocialNetworkGroup
from ....domain.model.social_network_group_id import SocialNetworkGroupId
from ....domain.model.social_network_group_name import SocialNetworkGroupName
from ....domain.model.social_network_group_image import SocialNetworkGroupImageUrl
from ....domain.exceptions.social_network_group_id_aready_registered import SocialNetworkGroupIdAlreadyRegistered
from .....user.domain.model.user_id import UserId
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestCreateSocialNetworkGroupHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedSocialNetworkGroupRepository = Mock()
        self.createSocialNetworkGroupHandler = CreateSocialNetworkGroupHandler(
            self.mockedSocialNetworkGroupRepository
        )
        return super(TestCreateSocialNetworkGroupHandler, self).setUp()

    def test_create_a_new_sn_group(self):
        self.createSocialNetworkGroupHandler.handle(
            CreateSocialNetworkGroupCommand(
                id=str(uuid4()),
                userId=str(uuid4()),
                name=fake.first_name(),
                image=fake.image_url()
            )
        )
        self.mockedSocialNetworkGroupRepository.save.assert_called_once()

    def test_dont_create_duplicate_sn_group_id(self):
        user = SocialNetworkGroup.add(
            id=SocialNetworkGroupId.fromString(str(uuid4())),
            userId=UserId.fromString(str(uuid4())),
            name=SocialNetworkGroupName.fromString(fake.first_name()),
            image=SocialNetworkGroupImageUrl.fromString(fake.image_url())
        )
        self.mockedSocialNetworkGroupRepository.getById = MagicMock(return_value=user)
        self.assertRaises(SocialNetworkGroupIdAlreadyRegistered,
                          self.createSocialNetworkGroupHandler.handle, CreateSocialNetworkGroupCommand(
                              id=str(uuid4()),
                              userId=str(uuid4()),
                              name=fake.first_name(),
                              image=fake.image_url()
                          ))
