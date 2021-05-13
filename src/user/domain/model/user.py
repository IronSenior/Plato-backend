from eventsourcing.domain import Aggregate, AggregateCreated
from .username import Username
from .user_mail import UserMail
from .user_password import UserPassword
from ....shared.domain.user_id import UserId
from typing import Optional


class User(Aggregate):

    def __init__(self, username: Username,
                 email: UserMail, password: UserPassword, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._username: Username = username
        self._email: UserMail = email
        self._password: UserPassword = password

    @property
    def userid(self):
        return self._id

    @property
    def username(self):
        return self._username.value

    @property
    def email(self):
        return self._email.value

    @property
    def password(self):
        return self._password.value

    @classmethod
    def add(cls, userid: UserId, username: Username,
            email: UserMail, password: UserPassword) -> "User":
        return cls._create(
            cls.UserWasCreated,
            id=userid.value,
            username=username.value,
            email=email.value,
            password=password.value
        )

    class UserWasCreated(AggregateCreated):
        bus_string = "USER_WAS_CREATED"
        username: str
        email: str
        password: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            user = super().mutate(obj)
            user._username = Username.fromString(self.username)
            user._password = UserPassword.fromHash(self.password)
            user._email = UserMail.fromString(self.email)
            return user

    def checkPassword(self, password: str) -> bool:
        return self._password.verify(password)
