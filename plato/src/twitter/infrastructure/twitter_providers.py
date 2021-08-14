from dependency_injector import containers, providers
from .repository.account_repository import AccountRepository
from .repository.tweet_repository import TweetRepository
from .service.tweet_publisher import TweepyTweetPublisher
from .service.dummy_tweet_publisher import DummyTweetPublisher
import os


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Factory(AccountRepository)
    TWEETS = providers.Factory(TweetRepository)
    TWEET_PUBLISHER = providers.Factory(TweepyTweetPublisher)

    if os.environ["ENV_MODE"] == "Test":
        # ! For testing we inject a custom mocked TweetPublisher
        # ! It has to be siggleton
        TWEET_PUBLISHER = providers.Singleton(DummyTweetPublisher)
