from plato_cqrs import QueryHandler
from .get_tweets_by_account_query import GetTweetsByAccountQuery
from .get_tweets_by_account_response import GetTweetsByAccountResponse
import sqlalchemy as db
import os


class GetTweetsByAccountHandler(QueryHandler):

    def __init__(self):
        self.__engine = db.create_engine(os.environ["DB_ENGINE"])
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__tweetsProjection = db.Table("pending_tweets", self.__metadata, autoload=True, autoload_with=self.__engine)

    def handle(self, query: GetTweetsByAccountQuery) -> GetTweetsByAccountResponse:
        query = db.select([self.__tweetsProjection]).where(
            self.__tweetsProjection.columns.accountid == query.accountId,
            self.__tweetsProjection.columns.publicationdate < query.beforeDate,
            self.__tweetsProjection.columns.publicationdate > query.afterDate
        )
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            return None

        getTweetsByAccountResponse = GetTweetsByAccountResponse()
        for tweet in resultSet:
            getTweetsByAccountResponse.appendTweet(
                tweetId=tweet[0],
                accountId=tweet[1],
                description=tweet[2],
                publicationDate=tweet[3],
                published=tweet[4]
            )

        return getTweetsByAccountResponse
