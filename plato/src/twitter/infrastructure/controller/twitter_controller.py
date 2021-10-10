from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.exceptions import Unauthorized, BadRequest
from ...application.account_dto import AccountDTO
from ..tweet_dto import TweetDTO
from ..service.twitter_service import TwitterService


TIMESTAMP_3021 = 33166368000

twitterFlaskBlueprint = Blueprint('Twitter', __name__, url_prefix="/twitter")


@twitterFlaskBlueprint.route('/account/add/', methods=["POST"])
@jwt_required()
def add_twitter_account(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can add Twitter Accounts")

    accountDto: AccountDTO = request.json.get("account", False)
    if not accountDto:
        raise BadRequest("No Twitter account was specified")

    if currentUserId != accountDto["userId"]:
        raise Unauthorized("Trying to add account for a different user")

    twitterService: TwitterService = TwitterService()
    try:
        twitterService.addTwitterAccount(accountDto)
    except Exception:
        raise Unauthorized("Impossible to verify twitter account")
    return jsonify(success=True)


@twitterFlaskBlueprint.route('/account/token/request/', methods=["GET"])
@jwt_required()
def request_twitter_token(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can add Twitter Accounts")

    twitterService: TwitterService = TwitterService()
    callbackUrl: str = request.args.get('callbackUrl', "")
    try:
        authUrl = twitterService.requestToken(callbackUrl)
    except Exception:
        raise Unauthorized("Impossible to verify twitter account")
    return jsonify({"authUrl": authUrl})


@twitterFlaskBlueprint.route('/brand/<string:brandId>/')
@jwt_required()
def get_twitter_account_by_brand(brandId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get accounts")

    twitterService: TwitterService = TwitterService()
    account = twitterService.getAccountByBrand(brandId)
    if not account:
        raise BadRequest("Twitter account not found")
    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get an account from a different user")

    return jsonify({"account": account}), 200


@twitterFlaskBlueprint.route('/tweet/schedule/', methods=["POST"])
@jwt_required()
def schedule_tweet(**kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can schedule Tweets")

    tweetDto: TweetDTO = request.json.get("tweet", False)
    if not tweetDto:
        raise BadRequest("No Tweet was specified")

    twitterService: TwitterService = TwitterService()
    account: AccountDTO = twitterService.getAccount(tweetDto["accountId"])
    if not account:
        raise BadRequest("Twitter account not found")
    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to schedule a tweet for a different user")

    twitterService.scheduleTweet(tweet=tweetDto)
    return jsonify(success=True)


@twitterFlaskBlueprint.route('/tweet/<string:accountId>/', methods=["GET"])
@jwt_required()
def get_schedule_tweets(accountId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Tweets")

    if not accountId:
        raise BadRequest("No account was specified")

    print(accountId)
    twitterService: TwitterService = TwitterService()
    account: AccountDTO = twitterService.getAccount(accountId)
    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get tweets from other user")

    afterDate = request.args.get("sinceDate") or 0
    beforeDate = request.args.get("limitDate") or TIMESTAMP_3021
    tweets: dict = twitterService.getTweetsByAccount(accountId, afterDate, beforeDate)
    return jsonify(tweets), 200


@twitterFlaskBlueprint.route('/tweet/publish/', methods=["GET"])
def publish_scheduled_tweets():
    twitterService: TwitterService = TwitterService()
    twitterService.publishScheduledTweets()
    return jsonify(success=True)
