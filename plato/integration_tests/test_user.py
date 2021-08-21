import unittest
import faker
import json
import uuid
from ..main import create_app, userProvider
from ..src.user.domain.repository.users import Users
from ..src.user.domain.model.user import User
from ..src.shared.domain.user_id import UserId
from ..src.user.domain.model.username import Username
from ..src.user.domain.model.user_mail import UserMail
from ..src.user.domain.model.user_password import UserPassword
fake = faker.Faker()


class TestUserIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.users: Users = userProvider.USERS()
        self.app = create_app(test_env=True).test_client()

    def test_user_creation(self):
        user_id = str(uuid.uuid4())
        email = fake.company_email()
        username = fake.first_name()
        self.app.post("/user/create/", json={
            "user": {
                "userId": user_id,
                "username": username,
                "usermail": email,
                "password": fake.password()
            }
        })
        testing_user = self.users.getById(UserId.fromString(user_id))
        self.assertTrue(type(testing_user) == User)
        self.assertEqual(testing_user.email, email)
        self.assertEqual(testing_user.username, username)

    def test_correct_user_login(self):
        email = fake.company_email()
        username = fake.first_name()
        password = fake.password()
        user = User.add(
            userId=UserId.fromString(str(uuid.uuid4())),
            username=Username.fromString(username),
            email=UserMail.fromString(email),
            password=UserPassword.fromString(password)
        )
        self.users.save(user)
        login_response = self.app.post("/user/login/", json={
            "email": email,
            "password": password
        })
        data = json.loads(login_response.data)
        self.assertTrue("access_token" in data.keys())

    def test_incorrect_password_user_login(self):
        email = fake.company_email()
        username = fake.first_name()
        password = fake.password()
        user = User.add(
            userId=UserId.fromString(str(uuid.uuid4())),
            username=Username.fromString(username),
            email=UserMail.fromString(email),
            password=UserPassword.fromString(password)
        )
        self.users.save(user)
        login_response = self.app.post("/user/login/", json={
            "email": email,
            "password": fake.password()
        })
        self.assertEqual(login_response.status_code, 401)

    def test_incorrect_email_user_login(self):
        email = fake.company_email()
        username = fake.first_name()
        password = fake.password()
        user = User.add(
            userId=UserId.fromString(str(uuid.uuid4())),
            username=Username.fromString(username),
            email=UserMail.fromString(email),
            password=UserPassword.fromString(password)
        )
        self.users.save(user)
        login_response = self.app.post("/user/login/", json={
            "email": fake.company_email(),
            "password": password
        })
        self.assertEqual(login_response.status_code, 401)
