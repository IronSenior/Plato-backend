from flask_jwt_extended import jwt_required, get_current_user
from flask import Blueprint, request
from werkzeug.exceptions import Unauthorized, BadRequest
from ..twitter_account_dto import TwitterAccountDTO
from ..service.twitter_account_service import TwitterAccountService
from ....shared.application.user_dto import UserDTO


twitterAccountFlaskBlueprint = Blueprint('Twitter Account', __name__, url_prefix="/twitter/account")


@twitterAccountFlaskBlueprint.route('/add/', methods=["POST"])
@jwt_required
def create_brand(**kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can add Twitter Accounts")

    accountDto: TwitterAccountDTO = request.json.get("account", False)
    if not accountDto:
        raise BadRequest("No Twitter account was specified")

    if user["userid"] != accountDto["userId"]:
        raise Unauthorized("Trying to add acount for a diferent user")

    twitterService: TwitterAccountService = TwitterAccountService()
    try:
        twitterService.addTwitterAccount(accountDto)
    except Exception:
        raise Unauthorized("Imposible to verify twitter account")
    return 200
