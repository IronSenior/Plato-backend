from plato_cqrs import QueryHandler
from ...domain.repository.users import Users
from ...domain.model.user_mail import UserMail
from .get_user_by_email_query import GetUserByEmailQuery
from .get_user_response import GetUserResponse
from dependency_injector.wiring import inject, Provide
from typing import Optional


class GetUserByEmailHandler(QueryHandler):

    @inject
    def __init__(self, users: Users = Provide["USERS"]):
        self.__users: Users = users

    def handle(self, query: GetUserByEmailQuery) -> Optional[GetUserResponse]:
        userMail = UserMail.fromString(query.email)

        user = self.__users.getByEmail(userMail)

        if not user:
            return None
        return GetUserResponse(
            userId=user.userId,
            username=user.username,
            usermail=user.usermail,
            password=user.password
        )
