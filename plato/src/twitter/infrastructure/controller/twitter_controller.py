from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest
from ...application.account_dto import AccountDTO
from ..tweet_dto import TweetDTO
from ..service.twitter_service import TwitterService


TIMESTAMP_3021 = 33166368000000

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


@twitterFlaskBlueprint.route('/brand/<string:brandId>/account/')
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


@twitterFlaskBlueprint.route('/tweet/<string:tweetId>/media/', methods=["POST"])
@jwt_required()
def upload_tweet_media(tweetId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Tweets")

    if not tweetId:
        raise BadRequest("No tweet was specified")

    if 'file' not in request.files:
        raise BadRequest("There is no media in the request")

    media = request.files['file']
    if media.filename == '':
        raise BadRequest("No selected media in the request")

    twitterService: TwitterService = TwitterService()
    tweet = twitterService.getTweetById(tweetId)
    if not tweet:
        raise NotFound("Tweet was not found")

    account = twitterService.getAccount(tweet["accountId"])

    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get tweets from other user")

    twitterService.addMediaToTweet(tweetId, media)
    return jsonify(success=True)


@twitterFlaskBlueprint.route('/tweet/<string:accountId>/', methods=["GET"])
@jwt_required()
def get_schedule_tweets(accountId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Tweets")

    if not accountId:
        raise BadRequest("No account was specified")

    twitterService: TwitterService = TwitterService()
    account: AccountDTO = twitterService.getAccount(accountId)
    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get tweets from other user")

    afterDate = request.args.get("sinceDate") or 0
    beforeDate = request.args.get("limitDate") or TIMESTAMP_3021
    tweets: dict = twitterService.getTweetsByAccount(accountId, int(afterDate), int(beforeDate))
    return jsonify(tweets), 200


@twitterFlaskBlueprint.route('/tweet/<string:tweetId>/report/', methods=["GET"])
@jwt_required()
def get_tweet_reports(tweetId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Tweets")

    if not tweetId:
        raise BadRequest("No tweet was specified")

    twitterService: TwitterService = TwitterService()
    tweet = twitterService.getTweetById(tweetId)
    account = twitterService.getAccount(tweet["accountId"])

    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get tweets from other user")

    afterDate = request.args.get("sinceDate") or 0
    beforeDate = request.args.get("limitDate") or TIMESTAMP_3021
    tweetReports: list = twitterService.getTweetReportsByTweet(tweetId, int(afterDate), int(beforeDate))
    return jsonify(tweetReports), 200


@twitterFlaskBlueprint.route('/account/<string:accountId>/report/', methods=["GET"])
@jwt_required()
def get_account_reports(accountId: str = None, **kw):
    currentUserId: str = get_current_user()
    if not currentUserId:
        raise Unauthorized("Only logged users can get Tweets")

    if not accountId:
        raise BadRequest("No tweet was specified")

    twitterService: TwitterService = TwitterService()
    account = twitterService.getAccount(accountId)

    if account["userId"] != currentUserId:
        raise Unauthorized("Trying to get tweets from other user")

    afterDate = request.args.get("sinceDate") or 0
    beforeDate = request.args.get("limitDate") or TIMESTAMP_3021
    tweetReports: list = twitterService.getAccountReportsByAccount(accountId, int(afterDate), int(beforeDate))
    return jsonify(tweetReports), 200


def publish_scheduled_tweets():
    twitterService: TwitterService = TwitterService()
    twitterService.publishScheduledTweets()


def generate_tweets_reports():
    twitterService: TwitterService = TwitterService()
    twitterService.generateTweetsReports()


def generate_account_reports():
    twitterService: TwitterService = TwitterService()
    twitterService.generateAccountReport()
