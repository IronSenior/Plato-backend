from eventsourcing.domain import Aggregate, AggregateCreated
from .username import Username
from .user_mail import UserMail
from .user_password import UserPassword
from ....shared.domain.user_id import UserId
from typing import Optional


class User(Aggregate):

    def __init__(self, username: Username,
                 usermail: UserMail, password: UserPassword, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._username: Username = username
        self._usermail: UserMail = usermail
        self._password: UserPassword = password

    @property
    def userId(self):
        return self._id

    @property
    def username(self):
        return self._username.value

    @property
    def usermail(self):
        return self._usermail.value

    @property
    def password(self):
        return self._password.value

    @classmethod
    def add(cls, userId: UserId, username: Username,
            usermail: UserMail, password: UserPassword) -> "User":
        return cls._create(
            cls.UserWasCreated,
            id=userId.value,
            username=username.value,
            usermail=usermail.value,
            password=password.value
        )

    class UserWasCreated(AggregateCreated):
        bus_string = "USER_WAS_CREATED"
        username: str
        usermail: str
        password: str

        def mutate(self, obj: Optional[Aggregate]) -> Aggregate:
            user = super().mutate(obj)
            user._username = Username.fromString(self.username)
            user._password = UserPassword.fromHash(self.password)
            user._usermail = UserMail.fromString(self.usermail)
            return user
