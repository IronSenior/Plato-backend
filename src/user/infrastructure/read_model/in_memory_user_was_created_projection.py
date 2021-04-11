from ....shared.plato_event_bus import PlatoEventBus
from ...domain.model.user import User
from ...domain.model.user_id import UserId
from ...domain.model.user_mail import UserMail
from ...domain.model.user_password import UserPassword
from ...domain.model.username import Username
from .user_model import UserModel
from dependency_injector.wiring import Provide, inject


@PlatoEventBus.on("USER_WAS_CREATED")
@inject
def userWasCreatedProjection(event: User.UserWasCreated,
                             userModel: UserModel = Provide["USER_MODEL"]):
    user = User.add(
        userid=UserId(event.originator_id),
        username=Username.fromString(event.username),
        password=UserPassword.fromHash(event.password),
        email=UserMail.fromString(event.email)
    )
    userModel.save(user)
