from commandbus import CommandHandler
from dependency_injector.wiring import Provide, inject
from .create_user_command import CreateUserCommand
from ...domain.repository.user_repository import UserRepository
from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.username import Username
from ...domain.model.user_password import UserPassword
from ...domain.model.user import User
from ...domain.exception.user_id_already_registered import UserIdAlreadyRegistered
from ...domain.exception.user_email_already_registered import UserEmailAlreadyRegistered


class CreateUserCommandHandler(CommandHandler):

    @inject
    def __init__(self, userRepostory: UserRepository = Provide['USERS']):
        self.userRepository: UserRepository = userRepostory

    def handle(self, cmd: CreateUserCommand):
        userId = UserId.fromString(cmd.userId)
        usermail = UserMail.fromString(cmd.userMail)

        if (type(self.userRepository.getById(userId)) == User):
            raise UserIdAlreadyRegistered("The user id is already registered")

        if (type(self.userRepository.getByEmail(usermail)) == User):
            raise UserEmailAlreadyRegistered("The user email is already registered")

        user = User.add(
            userid=userId,
            username=Username.fromString(cmd.username),
            email=usermail,
            password=UserPassword.fromString(cmd.password)
        )
        self.userRepository.save(user)
