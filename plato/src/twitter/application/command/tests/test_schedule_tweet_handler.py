from datetime import datetime
from ....domain.tweet.exceptions.tweet_id_already_registered import TweetIdAlreadyRegistered
from ....domain.tweet.model.tweet import Tweet
from ....domain.tweet.model.tweet_id import TweetId
from ....domain.account.model.account_id import AccountId
from ....domain.tweet.model.tweet_description import TweetDescription
import unittest
from uuid import uuid4
import string
import random
from unittest.mock import Mock, MagicMock
from ..schedule_tweet_command import ScheduleTweetCommand
from ..schedule_tweet_handler import ScheduleTweetHandler


class TestScheduleTweetHandler(unittest.TestCase):

    def setUp(self) -> None:
        self.mockedTweets = Mock()
        self.scheduleTweetHandler = ScheduleTweetHandler(
            tweets=self.mockedTweets
        )
        return super(TestScheduleTweetHandler, self).setUp()

    def test_add_a_new_tweet(self):
        self.scheduleTweetHandler.handle(
            ScheduleTweetCommand(
                tweetId=str(uuid4()),
                accountId=str(uuid4()),
                description=self.get_random_string(180),
                publicationDate=int(datetime.now().timestamp() * 1000)
            )
        )
        self.mockedTweets.save.assert_called_once()

    def test_dont_create_duplicated_tweet_id(self):
        tweet = Tweet.add(
            tweetId=TweetId.fromString(str(uuid4())),
            accountId=AccountId.fromString(str(uuid4())),
            description=TweetDescription.fromString(str(uuid4())),
            publicationDate=datetime.now()
        )
        self.mockedTweets.getById = MagicMock(return_value=tweet)
        with self.assertRaises(TweetIdAlreadyRegistered):
            self.scheduleTweetHandler.handle(
                ScheduleTweetCommand(
                    tweetId=str(uuid4()),
                    accountId=str(uuid4()),
                    description=self.get_random_string(180),
                    publicationDate=int(datetime.now().timestamp() * 1000)
                )
            )

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
