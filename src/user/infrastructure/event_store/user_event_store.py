from ...domain.model.user_id import UserId
from ...domain.model.user import User
from ...domain.repository.user_repository import UserRepository
from eventsourcing.application import AggregateNotFound, Application
from typing import Optional
from ....shared.plato_event_bus import PlatoEventBus


class UserEventStore(UserRepository, Application):

    def save(self, user: User) -> None:
        super(UserEventStore, self).save(user)
        for event in user.collect_events():
            PlatoEventBus.emit(event.bus_string, event)

    def find(self, userId: UserId) -> Optional[User]:
        try:
            user = self.repository.get(userId.value)
        except AggregateNotFound:
            return None
        return user

    def get(self, userId: UserId) -> User:
        return self.repository.get(userId.value)
