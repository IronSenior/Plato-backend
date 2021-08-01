from flask_jwt_extended import JWTManager
from ...user.application.user_dto import UserDTO

jwtManager = JWTManager()


# * Gets the userDTO passed as identity in create_access_token
# * method and returns the identity
@jwtManager.user_identity_loader
def user_identity_lookup(user: UserDTO):
    return user["userId"]


# * This method is returned in get_current_user method
@jwtManager.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    return jwt_data["sub"]
