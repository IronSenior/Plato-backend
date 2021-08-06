from ...application.user_dto import UserDTO
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from ..service.user_service import UserService
from ...domain.exception.incorrect_password import IncorrectPassword
from ...domain.exception.user_was_not_found import UserWasNotFound

userFlaskBlueprint = Blueprint('User', __name__, url_prefix="/user")


@userFlaskBlueprint.route('/create/', methods=["POST"])
def create_user(**kw):
    userService: UserService = UserService()
    user_json = request.json.get("user", False)
    if not user_json:
        raise BadRequest("No user was specified")

    userService.createUser(user_json)
    return jsonify({}), 200


@userFlaskBlueprint.route('/get/<string:userId>/', methods=["GET"])
def get_user(userId, **kw):
    userService: UserService = UserService()
    if not userId:
        raise NotFound("User was not found")
    user = userService.getUser(userId)
    if not user:
        raise NotFound("User was not found")
    return jsonify(user), 200


@userFlaskBlueprint.route('/login/', methods=["POST"])
def login(**kw):
    userService: UserService = UserService()
    email = request.json.get("email", False)
    password = request.json.get("password", False)
    try:
        user: UserDTO = userService.loginUser(email, password)
    except IncorrectPassword as e:
        raise Unauthorized("Wrong password or email") from e
    except UserWasNotFound as e:
        raise Unauthorized("Wrong password or email") from e
    jwt_token = create_access_token(identity=user)
    return jsonify({'access_token': jwt_token, 'user': user}), 200
