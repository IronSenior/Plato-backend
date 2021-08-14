from plato_cqrs import QueryHandler
from .get_brand_by_user_id_query import GetBrandByUserIdQuery
from .get_brand_by_user_id_response import GetBrandByUserIdResponse
from typing import Optional
import sqlalchemy as db
import os


class GetBrandByUserIdHandler(QueryHandler):

    def __init__(self):
        self.__engine = db.create_engine(os.environ["DB_ENGINE"])
        self.__connection = self.__engine.connect()
        self.__metadata = db.MetaData()
        self.__brandProjection = db.Table("brands", self.__metadata, autoload=True, autoload_with=self.__engine)

    def handle(self, query: GetBrandByUserIdQuery) -> Optional[GetBrandByUserIdResponse]:
        query = db.select([self.__brandProjection]).where(self.__brandProjection.columns.userid == query.userId)
        resultProxy = self.__connection.execute(query)
        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None

        getBrandByUserIdResponse = GetBrandByUserIdResponse()
        for brand in resultSet:
            getBrandByUserIdResponse.addBrand(
                brandId=brand[0],
                userId=brand[1],
                name=brand[2],
                image=brand[3]
            )
        return getBrandByUserIdResponse
