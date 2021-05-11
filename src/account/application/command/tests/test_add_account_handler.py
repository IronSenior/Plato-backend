import unittest
import pytest
from unittest.mock import MagicMock, Mock
from uuid import uuid4
from ..add_account_handler import AddAccountHandler
from ..add_account_command import AddAccountCommand
from ....domain.model.account import Account
from ....domain.model.account_id import AccountId
from ....domain.model.account_name import AccountName
from ....domain.model.social_network import SocialNetwork
from ....domain.model.user_token import UserToken
from ....domain.exceptions.account_id_already_registered import AccountIdAlreadyRegistered
from .....brand.domain.model.brand_id import BrandId
from .....shared.domain.user_id import UserId
import faker

fake = faker.Faker()


@pytest.mark.unit
class TestAddAccountHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedAccounts = Mock()
        self.addAccountHandler = AddAccountHandler(
            accounts=self.mockedAccounts
        )
        return super(TestAddAccountHandler, self).setUp()

    def test_add_a_new_account(self):
        self.addAccountHandler.handle(
            AddAccountCommand(
                accountId=str(uuid4()),
                userId=str(uuid4()),
                brandId=str(uuid4()),
                name=fake.first_name(),
                userToken=str(uuid4()),
                socialNetwork="twitter"
            )
        )
        self.mockedAccounts.save.assert_called_once()

    def test_dont_create_duplicated_sn_account_id(self):
        account = Account.add(
            accountId=AccountId.fromString(str(uuid4())),
            brandId=BrandId.fromString(str(uuid4())),
            name=AccountName.fromString(fake.first_name()),
            userId=UserId.fromString(str(uuid4())),
            userToken=UserToken.fromString(str(uuid4())),
            socialNetwork=SocialNetwork.fromString("twitter")
        )
        self.mockedAccounts.getById = MagicMock(return_value=account)
        self.assertRaises(AccountIdAlreadyRegistered,
                          self.addAccountHandler.handle, AddAccountCommand(
                              accountId=str(uuid4()),
                              userId=str(uuid4()),
                              brandId=str(uuid4()),
                              name=fake.first_name(),
                              userToken=str(uuid4()),
                              socialNetwork="twitter"
                          ))
