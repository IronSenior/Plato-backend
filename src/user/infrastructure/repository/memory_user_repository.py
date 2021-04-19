from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.user import User
from ...domain.repository.user_repository import UserRepository
from typing import List, Optional
from ....shared.plato_event_bus import PlatoEventBus


class MemoryUserRepository(UserRepository):

    def __init__(self):
        self.__users: List[User] = []

    def save(self, user: User) -> None:
        # super(UserEventStore, self).save(user)
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