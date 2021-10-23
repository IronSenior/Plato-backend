from ....shared.infrastructure.plato_event_bus import PlatoEventBus
from ...domain.account_report.model.account_report import AccountReport
import pymongo
import os


@PlatoEventBus.on("ACCOUNT_REPORT_WAS_CREATED")
def onAccountReportWasCreated(event: AccountReport.AccountReportWasCreated):
    db = pymongo.MongoClient(os.environ["MONGODB_URL"])[os.environ["MONGODB_DBNAME"]]
    accountReportDTO = {
        "reportId": str(event.originator_id),
        "accountId": event.accountId,
        "reportDate": event.reportDate,
        "followersCount": event.followersCount,
        "friendsCount": event.friendsCount
    }
    db["account_reports"].insert_one(accountReportDTO)
