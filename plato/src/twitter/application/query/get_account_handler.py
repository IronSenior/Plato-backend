from plato_cqrs import QueryHandler
from .get_account_query import GetAccountQuery
from .get_account_response import GetAccountResponse
import sqlalchemy as db
import os


class GetAccountHandler(QueryHandler):

    def __init__(self):
        self.__engine = db.create_engine(os.environ["DB_ENGINE"])
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__accountProjection = db.Table("twitter_accounts", self.__metadata, autoload=True, autoload_with=self.__engine)

    def handle(self, query: GetAccountQuery) -> GetAccountResponse:
        query = db.select([self.__accountProjection]).where(self.__accountProjection.columns.accountid == query.accountId)
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            return None
        account = resultSet[0]

        return GetAccountResponse(
            accountId=account[0],
            brandId=account[1],
            userId=account[2],
            name=account[3],
            accessToken=account[4],
            accessTokenSecret=account[5]
        )
