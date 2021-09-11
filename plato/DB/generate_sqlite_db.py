import sqlalchemy as db
import os
import pymongo

from dotenv import load_dotenv
load_dotenv()


def remove_existing_tables(engine):
    sql = "DROP TABLE IF EXISTS users;"
    engine.execute(sql)


def create_user_table(metadata):
    db.Table('users', metadata,
             db.Column('userid', db.String(36), nullable=False, primary_key=True),
             db.Column('username', db.String(255), nullable=False,),
             db.Column('email', db.String(255), nullable=False),
             db.Column('password', db.String(255), nullable=False))


def main():
    engine = db.create_engine(os.environ['DB_ENGINE'])
    engine.connect()
    metadata = db.MetaData()
    remove_existing_tables(engine)
    create_user_table(metadata)
    metadata.create_all(engine)
    if os.environ["ENV_MODE"] == "Test":
        mongo_client = pymongo.MongoClient(os.environ["MONGODB_URL"])
        mongo_client.drop_database(os.environ["MONGODB_DBNAME"])


if __name__ == "__main__":
    main()
