from commandbus import CommandHandler
from dependency_injector.wiring import Provide, inject
from .create_user_command import CreateUserCommand
from ...domain.repository.users import Users
from ....shared.domain.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.username import Username
from ...domain.model.user_password import UserPassword
from ...domain.model.user import User
from ...domain.exception.user_id_already_registered import UserIdAlreadyRegistered
from ...domain.exception.user_email_already_registered import UserEmailAlreadyRegistered
from ...domain.services.check_unique_user_email import CheckUniqueUserEmail


class CreateUserCommandHandler(CommandHandler):

    @inject
    def __init__(self, users: Users = Provide['USERS'],
                 checkUniqueUserEmail: CheckUniqueUserEmail = Provide["CHECK_UNIQUE_USER_EMAIL"]):
        self.users: Users = users
        self.checkUniqueUserEmail: CheckUniqueUserEmail = checkUniqueUserEmail

    def handle(self, cmd: CreateUserCommand):
        userId = UserId.fromString(cmd.userId)
        usermail = UserMail.fromString(cmd.userMail)

        if (type(self.users.getById(userId)) == User):
            raise UserIdAlreadyRegistered("The user id is already registered")

        if (type(self.checkUniqueUserEmail.withUserMail(usermail)) == UserId):
            raise UserEmailAlreadyRegistered("The user email is already registered")

        user = User.add(
            userid=userId,
            username=Username.fromString(cmd.username),
            email=usermail,
            password=UserPassword.fromString(cmd.password)
        )
        self.users.save(user)
