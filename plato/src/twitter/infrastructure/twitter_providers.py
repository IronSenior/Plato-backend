from dependency_injector import containers, providers
from .repository.account_repository import AccountRepository
from .repository.tweet_repository import TweetRepository
from .service.tweet_publisher import TweepyTweetPublisher
from .service.dummy_tweet_publisher import DummyTweetPublisher
from .read_model.get_account_service import GetTwitterAccountMongoService
from .read_model.get_tweets_service import GetTweetsMongoService
import os


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Factory(AccountRepository)
    GET_ACCOUNT_SERVICE = providers.Factory(GetTwitterAccountMongoService)
    GET_TWEETS_SERVICE = providers.Factory(GetTweetsMongoService)
    TWEETS = providers.Factory(TweetRepository)
    TWEET_PUBLISHER = providers.Factory(TweepyTweetPublisher)

    if os.environ["ENV_MODE"] == "Test":
        # ! For testing we inject a custom mocked TweetPublisher
        # ! It has to be singleton
        TWEET_PUBLISHER = providers.Singleton(DummyTweetPublisher)
