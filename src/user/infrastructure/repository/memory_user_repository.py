from ....shared.domain.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.user import User
from ...domain.repository.users import Users
from typing import List, Optional
from ....shared.infrastructure.plato_event_bus import PlatoEventBus


class MemoryUserRepository(Users):

    def __init__(self):
        self.__users: List[User] = []

    def save(self, user: User) -> None:
        self.__users.append(user)
        for event in user.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def getById(self, userid: UserId) -> Optional[User]:
        for user in self.__users:
            if userid.value == user.userid:
                return user

    def getByEmail(self, usermail: UserMail) -> Optional[User]:
        for user in self.__users:
            if usermail.value == user.email:
                return user
