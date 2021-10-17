from plato_cqrs import QueryHandler
from ..service.get_tweet_report_service import GetTweetReportsService
from ...domain.tweet.model.tweet_id import TweetId
from dependency_injector.wiring import inject, Provide
from .get_tweet_report_by_tweet_query import GetTweetReportsByTweetQuery
from .get_tweet_report_by_tweet_response import GetTweetReportsByAccountResponse


class GetTweetReportsByTweetHandler(QueryHandler):

    @inject
    def __init__(self, getTweetReportsService: GetTweetReportsService = Provide["GET_TWEET_REPORTS_SERVICE"]):
        self.__getTweetReportsService: GetTweetReportsService = getTweetReportsService

    def handle(self, query: GetTweetReportsByTweetQuery) -> GetTweetReportsByAccountResponse:
        reports = self.__getTweetReportsService.getTweetReportsByTweet(
            tweetId=TweetId.fromString(query.tweetId),
            afterDate=query.afterDate,
            beforeDate=query.beforeDate
        )
        getTweetReportsByAccountResponse = GetTweetReportsByAccountResponse()
        for report in reports:
            getTweetReportsByAccountResponse.appendReport(
                reportId=report["reportId"],
                tweetId=report["tweetId"],
                reportDate=report["reportDate"],
                retweetCount=report["retweetCount"],
                favCount=report["favoriteCount"],
                replyCount=report["replyCount"],
                quoteCount=report["quoteCount"],
                impressionCount=report.get("impressionCount", 0),
                profileClickCount=report.get("profileClickCount", 0)
            )
        return getTweetReportsByAccountResponse
