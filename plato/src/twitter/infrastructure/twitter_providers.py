from dependency_injector import containers, providers
from .repository.account_repository import AccountRepository
from .repository.memory_tweet_repository import MemoryTweetRepository


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Factory(AccountRepository)
    TWEETS = providers.Singleton(MemoryTweetRepository)
