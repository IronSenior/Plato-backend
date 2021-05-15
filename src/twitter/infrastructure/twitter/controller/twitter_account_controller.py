from flask_jwt_extended.view_decorators import jwt_required, get_current_user
from flask import Blueprint  # request
# import tweepy
from werkzeug.exceptions import Unauthorized
# from ...oauth_dto import Oauth2DTO
from .....user.application.user_dto import UserDTO

twitterAccountFlaskBlueprint = Blueprint('Twitter Account', __name__, url_prefix="/twitter/account")


@twitterAccountFlaskBlueprint.route('/add/', methods=["POST"])
@jwt_required
def create_brand(**kw):
    user: UserDTO = get_current_user()
    if not user:
        raise Unauthorized("Only logged users can add Twitter Accounts")

    # oauth2: Oauth2DTO = request.json.get("oauth2", False)
    # auth = tweepy.OAuthHandler(oauth2["consumerKey"], oauth2["consumerSecret"])
