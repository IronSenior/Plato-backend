from simpleCQRS import QueryHandler
from dependency_injector.wiring import Provide, inject
from ...domain.repository.users import Users
from ....shared.domain.user_id import UserId
from .get_user_query import GetUserQuery
from .get_user_response import GetUserResponse


class GetUserHandler(QueryHandler):

    @inject
    def __init__(self, users: Users = Provide["USERS"]):
        self.__users: Users = users

    def handle(self, query: GetUserQuery) -> GetUserResponse:
        userId = UserId.fromString(query.userId)
        user = self.__users.getById(userId)

        if not user:
            return None

        return GetUserResponse(
            userId=str(user.userId),
            username=user.username,
            password=user.password,
            email=user.email
        )
