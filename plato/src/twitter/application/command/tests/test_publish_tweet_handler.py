from datetime import datetime
import unittest
from uuid import uuid4
import pytest
from unittest.mock import MagicMock, Mock
from ..publish_tweet_handler import PublishTweetHandler
from ..publish_tweet_handler import PublishTweetCommand
from ....domain.tweet.model.tweet import Tweet
from ....domain.tweet.model.tweet_description import TweetDescription
from ....domain.tweet.model.tweet_id import TweetId
from ....domain.account.model.account_id import AccountId
from ....domain.tweet.exceptions.tweet_not_found import TweetNotFound


@pytest.mark.unit
class TestPublishTweetHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedTweets = Mock()
        self.mockedTweetPublisher = Mock()
        self.publishTweetHandler = PublishTweetHandler(
            tweets=self.mockedTweets,
            tweetPublisher=self.mockedTweetPublisher,
        )
        return super(TestPublishTweetHandler, self).setUp()

    def test_publish_a_tweet(self):
        tweetId = TweetId.fromString(str(uuid4()))
        tweet = Tweet.add(
            tweetId=tweetId,
            accountId=AccountId.fromString(str(uuid4())),
            description=TweetDescription.fromString("This is my Tweet"),
            publicationDate=datetime.now()
        )
        self.mockedTweets.getById = MagicMock(return_value=tweet)
        self.publishTweetHandler.handle(
            PublishTweetCommand(str(tweetId.value))
        )
        self.mockedTweets.save.assert_called_once()
        self.mockedTweetPublisher.publishTweet.assert_called_once()

    def test_raise_not_existing_tweet(self):
        with self.assertRaises(TweetNotFound):
            self.publishTweetHandler.handle(
                PublishTweetCommand(str(uuid4()))
            )
