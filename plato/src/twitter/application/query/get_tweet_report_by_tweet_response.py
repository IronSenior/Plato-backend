from plato_cqrs import QueryResponse


class GetTweetReportsByAccountResponse(QueryResponse):

    def __init__(self, reports: list = None):
        self.__reports: list = reports or []

    @property
    def reports(self):
        return self.__reports

    def appendReport(self, reportId: str, tweetId: str, reportDate: int,
                     retweetCount: int, favCount: int, replyCount: int,
                     quoteCount: int, impressionCount: int, profileClickCount: int):
        self.__reports.append({
            "reportId": reportId,
            "tweetId": tweetId,
            "reportDate": reportDate,
            "retweetCount": retweetCount,
            "favCount": favCount,
            "replyCount": replyCount,
            "quoteCount": quoteCount,
            "impressionCount": impressionCount,
            "profileClickCount": profileClickCount
        })
