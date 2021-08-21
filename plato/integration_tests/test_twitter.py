from datetime import datetime
import unittest
import faker
import json
import uuid
import string
import random
from ..main import create_app, twitterProvider
from ..src.twitter.domain.tweet.repository.tweets import Tweets
from ..src.twitter.domain.tweet.model.tweet import Tweet
from ..src.twitter.domain.tweet.model.tweet_id import TweetId
from ..src.twitter.domain.account.repository.accounts import Accounts
from ..src.twitter.domain.account.model.account import Account
from ..src.twitter.domain.account.model.account_name import AccountName
from ..src.twitter.domain.account.model.account_id import AccountId
from ..src.twitter.domain.account.model.access_token import AccessToken
from ..src.twitter.domain.account.model.access_token_secret import AccessTokenSecret
from ..src.shared.domain.user_id import UserId
from ..src.shared.domain.brand_id import BrandId
from ..src.twitter.infrastructure.service.twitter_service import TwitterService

fake = faker.Faker()


class TestTwitterIntegration(unittest.TestCase):

    def setUp(self) -> None:
        self.tweets: Tweets = twitterProvider.TWEETS()
        self.accounts: Accounts = twitterProvider.TWITTER_ACCOUNTS()
        self.tweetPublisher = twitterProvider.TWEET_PUBLISHER()
        self.app = create_app(test_env=True).test_client()
        self.user_id = uuid.uuid4()
        self.account_id = uuid.uuid4()
        self.access_headers = self.create_and_login_user()
        self.create_account()

    def create_and_login_user(self):
        email = fake.company_email()
        password = fake.password()
        self.app.post("/user/create/", json={
            "user": {
                "userId": str(self.user_id),
                "username": fake.first_name(),
                "usermail": email,
                "password": password
            }
        })
        login_response = self.app.post("/user/login/", json={
            "email": email,
            "password": password,
        })
        data = json.loads(login_response.data)
        headers = {
            'Authorization': 'Bearer {}'.format(data["access_token"])
        }
        return headers

    def create_account(self):
        account = Account.add(
            userId=UserId.fromString(str(self.user_id)),
            brandId=BrandId.fromString(str(uuid.uuid4())),
            name=AccountName.fromString(fake.company()),
            accountId=AccountId.fromString(str(self.account_id)),
            accessToken=AccessToken.fromString(str(uuid.uuid4())),
            accessTokenSecret=AccessTokenSecret.fromString(str(uuid.uuid4()))
        )
        self.accounts.save(account)

    def test_tweet_schedule(self):
        tweetId = str(uuid.uuid4())
        description = self.get_random_string(120)
        publicationDate = datetime.now().timestamp()
        response = self.app.post("/twitter/tweet/schedule/", headers=self.access_headers, json={
            "tweet": {
                "tweetId": tweetId,
                "accountId": str(self.account_id),
                "description": description,
                "publicationDate": publicationDate
            }
        })
        testing_tweet = self.tweets.getById(TweetId.fromString(str(tweetId)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(type(testing_tweet) == Tweet)
        self.assertEqual(testing_tweet.description, description)
        self.assertEqual(testing_tweet.publicationDate, datetime.fromtimestamp(publicationDate))

    def test_publish_tweet(self):
        tweetId = str(uuid.uuid4())
        description = self.get_random_string(120)
        publicationDate = datetime.now().timestamp()
        response = self.app.post("/twitter/tweet/schedule/", headers=self.access_headers, json={
            "tweet": {
                "tweetId": tweetId,
                "accountId": str(self.account_id),
                "description": description,
                "publicationDate": publicationDate
            }
        })
        self.assertEqual(response.status_code, 200)

        twitterService = TwitterService()
        twitterService.publishScheduledTweets()
        self.assertEqual(self.tweetPublisher.called, 1)
        self.assertEqual(str(self.tweetPublisher.called_with[0].id), tweetId)

    def test_get_tweet(self):
        tweetId = str(uuid.uuid4())
        description = self.get_random_string(120)
        publicationDate = datetime.now().timestamp()
        self.app.post("/twitter/tweet/schedule/", headers=self.access_headers, json={
            "tweet": {
                "tweetId": tweetId,
                "accountId": str(self.account_id),
                "description": description,
                "publicationDate": publicationDate
            }
        })
        response = self.app.get(f"/twitter/tweet/{self.account_id}/", headers=self.access_headers)
        self.assertEqual(response.status_code, 200)
        data: dict = json.loads(response.data)
        self.assertTrue(tweetId in data.keys())

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
