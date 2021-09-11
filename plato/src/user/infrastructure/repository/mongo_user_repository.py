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

    def save(self, user: User) -> None:
        self.__db.insert_one({
            "userId": user.userId,
            "username": user.username,
            "email": user.email,
            "password": user.password
        })
        for event in user.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, userId: UserId) -> Optional[User]:
        user = self.__db.find_one({"userId": str(userId.value)})
        return self.__getUserFromResult(user)

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        user = self.__db.find_one({"email": usermail.value})
        return self.__getUserFromResult(user)

    def __getUserFromResult(self, result: tuple):
        return User.add(
            userId=UserId.fromString(result["userId"]),
            username=Username.fromString(result["username"]),
            email=UserMail.fromString(result["email"]),
            password=UserPassword.fromHash(result["password"])
        )
