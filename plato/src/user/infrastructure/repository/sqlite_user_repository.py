from ....shared.domain.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.username import Username
from ...domain.model.user_password import UserPassword
from ...domain.model.user import User
from ...domain.repository.users import Users
from typing import Optional
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
import sqlalchemy as db
import os


class SqliteUserRepository(Users):

    def __init__(self):
        self.__engine = db.create_engine(f"sqlite:///{os.environ['SQLITE_DBNAME']}")
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__users = db.Table("users", self.__metadata, autoload=True, autoload_with=self.__engine)

    def save(self, user: User) -> None:
        query = db.insert(self.__users).values(userid=str(user.userId), username=user.username,
                                               email=user.email, password=user.password)
        self.__connection.execute(query)
        for event in user.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, userId: UserId) -> Optional[User]:
        query = db.select([self.__users]).where(self.__users.columns.userid == str(userId.value))
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None
        return self.__getUserFromResult(resultSet[0])

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        query = db.select([self.__users]).where(self.__users.columns.email == usermail.value)
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None
        return self.__getUserFromResult(resultSet[0])

    def __getUserFromResult(self, result: tuple):
        return User.add(
            userId=UserId.fromString(result[0]),
            username=Username.fromString(result[1]),
            email=UserMail.fromString(result[2]),
            password=UserPassword.fromHash(result[3])
        )
