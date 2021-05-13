from ...domain.model.user_mail import UserMail
from ...domain.exception.incorrect_password import IncorrectPassword
from ...domain.exception.user_was_not_found import UserWasNotFound
from ...domain.repository.users import Users
from dependency_injector.wiring import Provide, inject
from ....shared.infrastructure.plato_command_bus import PlatoCommandBus
from ...application.command.create_user_command import CreateUserCommand
from ....shared.domain.user_id import UserId
from ..mapper.user_mapper import UserMapper


class UserService:

    @inject
    def __init__(self, users: Users = Provide["USERS"]):
        self.users: Users = users

    def createUser(self, userDto: dir):
        PlatoCommandBus.publish(
            CreateUserCommand(
                userid=userDto["userid"],
                username=userDto["username"],
                usermail=userDto["usermail"],
                password=userDto["password"]
            )
        )

    def getUser(self, userid: str):
        userid = UserId.fromString(userid)
        user = self.users.getById(userid)
        if not user:
            return None
        userDto = UserMapper.from_aggregate_to_dto(user)
        return userDto

    def loginUser(self, email: str, password: str):
        userMail = UserMail.fromString(email)
        user = self.users.getByEmail(userMail)
        if not user:
            raise UserWasNotFound(f"User with email {email}")
        if not user.checkPassword(password):
            raise IncorrectPassword(f"User with email {email}")
        userDto = UserMapper.from_aggregate_to_dto(user)
        return userDto
