import sqlalchemy as db
import os

from dotenv import load_dotenv
load_dotenv()


def remove_existing_tables(engine):
    sql = "DROP TABLE IF EXISTS users;"
    engine.execute(sql)
    sql = "DROP TABLE IF EXISTS brands;"
    engine.execute(sql)
    sql = "DROP TABLE IF EXISTS twitter_accounts;"
    engine.execute(sql)
    sql = "DROP TABLE IF EXISTS pending_tweets;"
    engine.execute(sql)


def create_user_table(metadata):
    db.Table('users', metadata,
             db.Column('userid', db.String(36), nullable=False, primary_key=True),
             db.Column('username', db.String(255), nullable=False,),
             db.Column('email', db.String(255), nullable=False),
             db.Column('password', db.String(255), nullable=False))


def create_brand_table(metadata):
    db.Table('brands', metadata,
             db.Column('brandid', db.String(36), nullable=False, primary_key=True),
             db.Column('userid', db.String(36), nullable=False),
             db.Column('name', db.String(255), nullable=False,),
             db.Column('image', db.String(255), nullable=False))


def create_twitter_accounts(metadata):
    db.Table('twitter_accounts', metadata,
             db.Column('accountid', db.String(36), nullable=False, primary_key=True),
             db.Column('brandid', db.String(36), nullable=False),
             db.Column('userid', db.String(36), nullable=False),
             db.Column('name', db.String(255), nullable=False,),
             db.Column('accesstoken', db.String(255), nullable=False),
             db.Column('accesssecret', db.String(255), nullable=False))


def create_pending_tweets(metadata):
    db.Table('pending_tweets', metadata,
             db.Column('tweetid', db.String(36), nullable=False, primary_key=True),
             db.Column('accountid', db.String(36), nullable=False),
             db.Column('description', db.String(255), nullable=False),
             db.Column('publicationdate', db.Float(precision=8), nullable=False),
             db.Column('published', db.Boolean(), nullable=False))


def main():
    engine = db.create_engine(f"{os.environ['DB_ENGINE']}")
    engine.connect()
    metadata = db.MetaData()
    remove_existing_tables(engine)
    create_user_table(metadata)
    create_brand_table(metadata)
    create_twitter_accounts(metadata)
    create_pending_tweets(metadata)
    metadata.create_all(engine)


if __name__ == "__main__":
    main()
