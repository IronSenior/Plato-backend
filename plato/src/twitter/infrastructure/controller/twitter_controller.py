from flask_jwt_extended import jwt_required, get_current_user
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import Unauthorized, BadRequest
from ..twitter_account_dto import TwitterAccountDTO
from ..tweet_dto import TweetDTO
from ..service.twitter_service import TwitterService


twitterFlaskBlueprint = Blueprint('Twitter', __name__, url_prefix="/twitter")


@twitterFlaskBlueprint.route('/account/add/', methods=["POST"])
@jwt_required()
def add_twitter_account(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can add Twitter Accounts")

    accountDto: TwitterAccountDTO = request.json.get("account", False)
    if not accountDto:
        raise BadRequest("No Twitter account was specified")

    if currentUserId != accountDto["userId"]:
        raise Unauthorized("Trying to add account for a different user")

    twitterService: TwitterService = TwitterService()
    try:
        twitterService.addTwitterAccount(accountDto)
    except Exception:
        raise Unauthorized("Imposible to verify twitter account")
    return jsonify(success=True)


@twitterFlaskBlueprint.route('/tweet/shedule/', methods=["POST"])
@jwt_required()
def schedule_tweet(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can schedule Tweets")

    tweetDto: TweetDTO = request.json.get("tweet", False)
    if not tweetDto:
        raise BadRequest("No Tweet was specified")

    twitterService: TwitterService = TwitterService()
    account: TwitterAccountDTO = twitterService.getAccount(tweetDto["accountId"])
    if not account:
        raise BadRequest("Twitter account not found")
    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to schedule a tweet for a different user")

    twitterService.scheduleTweet(tweet=tweetDto)
    return jsonify(success=True)


@twitterFlaskBlueprint.route('/tweet/publish/', methods=["GET"])
def publish_scheduled_tweets():
    twitterService: TwitterService = TwitterService()
    twitterService.publishScheduledTweets()
    return jsonify(success=True)
