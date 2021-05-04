import unittest
import pytest
from unittest.mock import MagicMock, Mock
from uuid import uuid4
from ..add_sn_account_handler import AddSocialNetworkAccountHandler
from ..add_sn_account_command import AddSocialNetworkAccountCommand
from ....domain.model.social_network_account import SocialNetworkAccount
from ....domain.model.social_network_account_id import SocialNetworkAccountId
from ....domain.model.social_network_account_name import SocialNetworkAccountName
from ....domain.model.social_network import SocialNetwork
from ....domain.model.user_token import UserToken
from ....domain.exceptions.sn_account_id_already_registered import SocialNetworkAccountIdAlreadyRegistered
from .....socialNetworkGroup.domain.model.social_network_group_id import SocialNetworkGroupId
from .....user.domain.model.user_id import UserId
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestAddSocialNetworkAccountHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedAccounts = Mock()
        self.addSocialNetworkAccountHandler = AddSocialNetworkAccountHandler(
            accounts=self.mockedAccounts
        )
        return super(TestAddSocialNetworkAccountHandler, self).setUp()

    def test_add_a_new_account(self):
        self.addSocialNetworkAccountHandler.handle(
            AddSocialNetworkAccountCommand(
                accountId=str(uuid4()),
                userId=str(uuid4()),
                snGroupId=str(uuid4()),
                name=fake.first_name(),
                userToken=str(uuid4()),
                socialNetwork="twitter"
            )
        )
        self.mockedAccounts.save.assert_called_once()

    def test_dont_create_duplicated_sn_account_id(self):
        account = SocialNetworkAccount.add(
            accountId=SocialNetworkAccountId.fromString(str(uuid4())),
            snGroupId=SocialNetworkGroupId.fromString(str(uuid4())),
            name=SocialNetworkAccountName.fromString(fake.first_name()),
            userId=UserId.fromString(str(uuid4())),
            userToken=UserToken.fromString(str(uuid4())),
            socialNetwork=SocialNetwork.fromString("twitter")
        )
        self.mockedAccounts.getById = MagicMock(return_value=account)
        self.assertRaises(SocialNetworkAccountIdAlreadyRegistered,
                          self.addSocialNetworkAccountHandler.handle, AddSocialNetworkAccountCommand(
                              accountId=str(uuid4()),
                              userId=str(uuid4()),
                              snGroupId=str(uuid4()),
                              name=fake.first_name(),
                              userToken=str(uuid4()),
                              socialNetwork="twitter"
                          ))
