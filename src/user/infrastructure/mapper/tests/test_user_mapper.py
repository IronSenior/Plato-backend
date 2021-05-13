import unittest
import faker
from uuid import uuid4
from unittest.mock import Mock
from ..user_mapper import UserMapper
from ....domain.model.user import User
from .....shared.domain.user_id import UserId
from ....domain.model.user_mail import UserMail
from ....domain.model.user_password import UserPassword
from ....domain.model.username import Username
from ....application.user_dto import UserDTO

fake = faker.Faker()


class TestUserMapper(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedUserRepository = Mock()
        return super(TestUserMapper, self).setUp()

    def test_from_user_to_dto(self):
        userid = UserId.fromString(str(uuid4()))
        username = Username.fromString(fake.first_name())
        email = UserMail.fromString(fake.company_email())
        password = UserPassword.fromString(fake.password())
        user = User.add(
            userid=userid,
            username=username,
            email=email,
            password=password
        )
        userDto: UserDTO = UserMapper.from_aggregate_to_dto(user)
        self.assertEqual(str(userid.value), userDto["userid"])
        self.assertEqual(username.value, userDto["username"])
        self.assertEqual(email.value, userDto["email"])
        self.assertEqual(password.value, userDto["password"])
