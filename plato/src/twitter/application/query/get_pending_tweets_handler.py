from plato_cqrs import QueryHandler
from .get_pending_tweets_query import GetPendingTweetsQuery
from .get_pending_tweets_response import GetPendingTweetsResponse
import sqlalchemy as db
from sqlalchemy.sql.expression import false
import os


class GetPendingTweetsHandler(QueryHandler):

    def __init__(self):
        self.__engine = db.create_engine(os.environ["DB_ENGINE"])
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__tweetsProjection = db.Table("pending_tweets", self.__metadata, autoload=True, autoload_with=self.__engine)

    def handle(self, query: GetPendingTweetsQuery) -> GetPendingTweetsResponse:
        query = db.select([self.__tweetsProjection]).where(
            self.__tweetsProjection.columns.published == false(),
            self.__tweetsProjection.columns.publicationdate <= query.publicationDate
        )
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            return None

        getPendingTweetsResponse = GetPendingTweetsResponse()
        for tweet in resultSet:
            getPendingTweetsResponse.appendTweet(
                tweetId=tweet[0],
                accountId=tweet[1],
                description=tweet[2],
                publicationDate=tweet[3],
                published=tweet[4]
            )

        return getPendingTweetsResponse
