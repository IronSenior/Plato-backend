from datetime import datetime
import uuid

from ...domain.tweet_report.repository.tweet_reports import TweetReports
from ...domain.tweet_report.service.tweet_status_retriever import TweetStatusRetriever
from ...domain.tweet_report.model.tweet_report import TweetReport
from ...domain.tweet_report.model.report_id import ReportId
from ...domain.tweet.model.tweet_id import TweetId
from ...domain.tweet.model.tweet import Tweet
from ..tweet_status_dto import TweetStatusDTO
from .create_tweet_report_command import CreateTweetReportCommand
from ..service.get_tweets_service import GetTweetsService
from dependency_injector.wiring import Provide, inject
from plato_cqrs import CommandHandler


class CreateTweetReportHandler(CommandHandler):

    @inject
    def __init__(self, tweetReports: TweetReports = Provide["TWEET_REPORTS"],
                 getTweetsService: GetTweetsService = Provide["GET_TWEETS_SERVICE"],
                 tweetStatusRetriever: TweetStatusRetriever = Provide["TWEET_STATUS_RETRIEVER"]):
        self.__tweetReports: TweetReports = tweetReports
        self.__tweetStatusRetriever: TweetStatusRetriever = tweetStatusRetriever
        self.__getTweetsService: GetTweetsService = getTweetsService

    def handle(self, cmd: CreateTweetReportCommand):
        tweetId: TweetId = TweetId.fromString(cmd.tweetId)
        tweet: Tweet = self.__getTweetsService.getTweetById(tweetId)

        tweetStatus: TweetStatusDTO = self.__tweetStatusRetriever.withTweet(tweet)

        if not tweetStatus:
            return None

        reportId = ReportId(uuid.uuid4())
        report: TweetReport = TweetReport.add(
            reportId=reportId,
            tweetId=tweetId,
            reportDate=datetime.now(),
            retweetCount=tweetStatus["retweet_count"],
            favCount=tweetStatus["favorite_count"],
            quoteCount=tweetStatus["quote_count"],
            replyCount=tweetStatus["reply_count"],
        )
        self.__tweetReports.save(report)
