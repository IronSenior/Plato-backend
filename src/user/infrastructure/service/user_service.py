from typing import List
from dependency_injector.wiring import Provide, inject
from ...domain.repository.user_repository import UserRepository
from ....shared.plato_command_bus import PlatoCommandBus
from ...application.command.create_user_command import CreateUserCommand
from ...domain.model.user_id import UserId
from ...domain.model.user import User
from ..mapper.user_mapper import UserMapper


class UserService:

    @inject
    def __init__(self, userRepository: UserRepository = Provide["USERS"]):
        self.userRepository: UserRepository = userRepository

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
        user = self.userRepository.getById(userid)
        userDto = UserMapper.from_aggregate_to_dto(user)
        return userDto

    def getAllUsers(self):
        users: List[User] = self.userRepository.getAll()
        usersDto = {}
        for user in users:
            usersDto[str(user.userid)] = UserMapper.from_aggregate_to_dto(user)
        return usersDto
