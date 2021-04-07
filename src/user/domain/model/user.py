from eventsourcing.domain import Aggregate, AggregateCreated
from .username import Username
from .user_mail import UserMail
from .user_password import UserPassword
from .user_id import UserId

class User(Aggregate):

    def __init__(self, username: Username,
                 email: UserMail, password: UserPassword, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__username: Username = username
        self.__email: UserMail = email
        self.__password: UserPassword = password
    
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
        username: str
        email: str
        password: str