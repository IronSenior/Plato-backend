from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.tweet_report.model.tweet_report import TweetReport
import pymongo
import os


@PlatoEventBus.on("TWEET_REPORT_WAS_CREATED")
def onTweetReportWasCreated(event: TweetReport.TweetReportWasCreated):
    db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    tweetReportDTO = {
        "reportId": str(event.originator_id),
        "tweetId": event.tweetId,
        "reportDate": event.reportDate,
        "retweetCount": event.retweetCount,
        "favoriteCount": event.favCount,
        "quoteCount": event.quoteCount,
        "replyCount": event.replyCount
    }
    db["tweet_reports"].insert_one(tweetReportDTO)
