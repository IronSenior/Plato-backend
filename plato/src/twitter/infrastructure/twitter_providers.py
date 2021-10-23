from dependency_injector import containers, providers
from .repository.account_repository import AccountRepository
from .repository.tweet_repository import TweetRepository
from .service.tweet_publisher import TweepyTweetPublisher
from .repository.tweet_report_repository import TweetReportRepository
from .repository.account_report_repository import AccountReportRepository
from .service.tweet_status_retriever import TweetStatusTweepyRetriever
from .service.dummy_tweet_publisher import DummyTweetPublisher
from .read_model.get_tweet_reports_service import GetTweetReportsMongoService
from .read_model.get_account_service import GetTwitterAccountMongoService
from .read_model.get_tweets_service import GetTweetsMongoService
from .service.account_status_retriever import AccountStatusRetriever
import os


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Factory(AccountRepository)
    GET_ACCOUNT_SERVICE = providers.Factory(GetTwitterAccountMongoService)
    GET_TWEETS_SERVICE = providers.Factory(GetTweetsMongoService)
    GET_TWEET_REPORTS_SERVICE = providers.Factory(GetTweetReportsMongoService)
    TWEETS = providers.Factory(TweetRepository)
    TWEET_REPORTS = providers.Factory(TweetReportRepository)
    TWEET_PUBLISHER = providers.Factory(TweepyTweetPublisher)
    TWEET_STATUS_RETRIEVER = providers.Factory(TweetStatusTweepyRetriever)
    ACCOUNT_STATUS_RETRIEVER = providers.Factory(AccountStatusRetriever)
    ACCOUNT_REPORTS = providers.Factory(AccountReportRepository)

    if os.environ["ENV_MODE"] == "Test":
        # ! For testing we inject a custom mocked TweetPublisher
        # ! It has to be singleton
        TWEET_PUBLISHER = providers.Singleton(DummyTweetPublisher)
