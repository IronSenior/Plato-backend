from flask_jwt_extended import JWTManager
from ..user.infrastructure.service.user_service import UserService
from ..user.application.user_dto import UserDTO

jwtManager = JWTManager()


# * Gets the userDTO passed as identity in create_access_token
# * method and returns the identity
@jwtManager.user_identity_loader
def user_identity_lookup(user: UserDTO):
    return user["userid"]


# * This method is returned in get_current_user method
@jwtManager.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    userService: UserService = UserService()
    user = userService.getUser(jwt_data["sub"])
    return user
