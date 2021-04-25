import unittest
import pytest
from uuid import uuid4
import faker
from unittest.mock import Mock, MagicMock
from ..create_user_command import CreateUserCommand
from ..create_user_handler import CreateUserCommandHandler
from ....domain.model.user import User
from ....domain.model.user_id import UserId
from ....domain.model.user_mail import UserMail
from ....domain.model.user_password import UserPassword
from ....domain.model.username import Username
from ....domain.exception.user_email_already_registered import UserEmailAlreadyRegistered
from ....domain.exception.user_id_already_registered import UserIdAlreadyRegistered

fake = faker.Faker()


@pytest.mark.unit
class TestCreateUserCommandHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedUserRepository = Mock()
        self.mockedCheckUniqueUserMail = Mock()
        self.createUserCommandHandler = CreateUserCommandHandler(
            users=self.mockedUserRepository,
            checkUniqueUserEmail=self.mockedCheckUniqueUserMail
        )
        return super(TestCreateUserCommandHandler, self).setUp()

    def test_create_a_new_user(self):
        self.createUserCommandHandler.handle(
            CreateUserCommand(
                userid=str(uuid4()),
                username=fake.first_name(),
                usermail=fake.company_email(),
                password=fake.password()
            )
        )
        self.mockedUserRepository.save.assert_called_once()

    def test_dont_create_duplicate_user_id(self):
        user = User.add(
            userid=UserId.fromString(str(uuid4())),
            username=Username.fromString(fake.first_name()),
            email=UserMail.fromString(fake.company_email()),
            password=UserPassword.fromString(fake.password())
        )
        self.mockedUserRepository.getById = MagicMock(return_value=user)
        self.assertRaises(UserIdAlreadyRegistered,
                          self.createUserCommandHandler.handle, CreateUserCommand(
                              userid=str(uuid4()),
                              username=fake.first_name(),
                              usermail=fake.company_email(),
                              password=fake.password()
                          ))

    def test_dont_create_duplicate_user_email(self):
        userid = UserId.fromString(str(uuid4()))
        self.mockedCheckUniqueUserMail.withUserMail = MagicMock(return_value=userid)
        self.assertRaises(UserEmailAlreadyRegistered, self.createUserCommandHandler.handle, CreateUserCommand(
            userid=str(uuid4()),
            username=fake.first_name(),
            usermail=fake.company_email(),
            password=fake.password()
        ))
