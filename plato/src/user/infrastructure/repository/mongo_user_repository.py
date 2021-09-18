from ....shared.domain.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.username import Username
from ...domain.model.user_password import UserPassword
from ...domain.model.user import User
from ...domain.repository.users import Users
from typing import Optional
from ....shared.infrastructure.plato_event_bus import PlatoEventBus
import pymongo
import os


class MongoUserRepository(Users):

    def __init__(self):
        self.__db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
        self.__users = self.__db["users"]

    def save(self, user: User) -> None:
        self.__users.insert_one({
            "userId": str(user.userId),
            "username": user.username,
            "usermail": user.usermail,
            "password": user.password
        })
        for event in user.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, userId: UserId) -> Optional[User]:
        user = self.__users.find_one({"userId": str(userId.value)})
        if not user:
            return None
        return self.__getUserFromResult(user)

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        user = self.__users.find_one({"usermail": usermail.value})
        if not user:
            return None
        return self.__getUserFromResult(user)

    def __getUserFromResult(self, result: tuple):
        return User.add(
            userId=UserId.fromString(result["userId"]),
            username=Username.fromString(result["username"]),
            usermail=UserMail.fromString(result["usermail"]),
            password=UserPassword.fromHash(result["password"])
        )
