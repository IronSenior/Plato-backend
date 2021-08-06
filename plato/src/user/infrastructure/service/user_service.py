from ...domain.exception.incorrect_password import IncorrectPassword
from ...domain.exception.user_was_not_found import UserWasNotFound
from ...domain.repository.users import Users
from dependency_injector.wiring import Provide, inject
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ....shared.infrastructure.plato_query_bus import PlatoQueryBus
from ...application.command.create_user_command import CreateUserCommand
from ...application.query.get_user_query import GetUserQuery
from ...application.query.get_user_by_email_query import GetUserByEmailQuery
from ...application.query.get_user_by_email_response import GetUserByEmailResponse
from ...application.query.get_user_response import GetUserResponse
from ..mapper.user_mapper import UserMapper
from passlib.hash import sha256_crypt


class UserService:

    @inject
    def __init__(self, users: Users = Provide["USERS"]):
        self.users: Users = users

    def createUser(self, userDto: dir):
        PlatoCommandBus.publish(
            CreateUserCommand(
                userId=userDto["userId"],
                username=userDto["username"],
                usermail=userDto["usermail"],
                password=userDto["password"]
            )
        )

    def getUser(self, userId: str):
        user: GetUserResponse = PlatoQueryBus.publish(
            GetUserQuery(userId=userId)
        )
        if not user:
            return None
        return UserMapper.from_aggregate_to_dto(user)

    def loginUser(self, email: str, password: str):
        user: GetUserByEmailResponse = PlatoQueryBus.publish(
            GetUserByEmailQuery(email=email)
        )
        if not user:
            raise UserWasNotFound(f"User with email {email}")
        if not sha256_crypt.verify(password, user.password):
            raise IncorrectPassword(f"User with email {email}")
        return UserMapper.from_aggregate_to_dto(user)
