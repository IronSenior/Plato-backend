from ...exceptions.too_long_tweet import TooLongTweet
import unittest
import random
import string
from ..tweet_description import TweetDescription


class TestTweetDescription(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_tweet_lenght(self):
        tweet = TweetDescription.fromString(self.get_random_string(180))
        self.assertEqual(type(tweet), TweetDescription)

    def test_tweet_limit_lenght(self):
        tweet = TweetDescription.fromString(self.get_random_string(280))
        self.assertEqual(type(tweet), TweetDescription)

    def test_tweet_long_lenght(self):
        with self.assertRaises(TooLongTweet):
            TweetDescription.fromString(self.get_random_string(281))

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
