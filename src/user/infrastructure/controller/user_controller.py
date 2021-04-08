from flask import Blueprint
from flask import request
from flask import jsonify
from werkzeug.exceptions import BadRequest, NotFound
from ..service.user_service import UserService

userFlaskBlueprint = Blueprint('user', __name__, url_prefix="/user")


@userFlaskBlueprint.route('/create/', methods=["POST"])
def create_user(**kw):
    userService: UserService = UserService()
    user_json = request.json.get("user", False)
    if not user_json:
        raise BadRequest("No user was specified")

    userService.createUser(user_json)
    return jsonify({"status": "ok"}), 200


@userFlaskBlueprint.route('/get/<string:userid>/', methods=["GET"])
def get_user(userid, **kw):
    userService: UserService = UserService()
    if not userid:
        raise NotFound("User was not found")

    user = userService.getUser(userid)
    if not user:
        raise NotFound("User was not found")
    return jsonify(user), 200
