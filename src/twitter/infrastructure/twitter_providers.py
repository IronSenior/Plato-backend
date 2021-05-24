from dependency_injector import containers, providers
from .repository.memory_account_repository import MemoryAccountRepository
from .repository.memory_tweet_repository import MemoryTweetRepository


class TwitterProviders(containers.DeclarativeContainer):

    TWITTER_ACCOUNTS = providers.Singleton(MemoryAccountRepository)
    TWEETS = providers.Singleton(MemoryTweetRepository)
