from ..read_model.user_model import UserModel
from dependency_injector.wiring import Provide, inject
from ....shared.plato_command_bus import PlatoCommandBus
from ...application.command.create_user_command import CreateUserCommand
from ...domain.model.user_id import UserId
from ..mapper.user_mapper import UserMapper


class UserService:

    @inject
    def __init__(self, userModel: UserModel = Provide["USER_MODEL"]):
        self.userModel: UserModel = userModel

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
        user = self.userModel.getById(userid)
        if not user:
            return None
        userDto = UserMapper.from_aggregate_to_dto(user)
        return userDto
