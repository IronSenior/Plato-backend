import sqlalchemy as db
import os

from dotenv import load_dotenv
load_dotenv()


def remove_existing_tables(engine):
    sql = 'DROP TABLE IF EXISTS users;'
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


def main():
    engine = db.create_engine(f"{os.environ['DB_ENGINE']}")
    engine.connect()
    metadata = db.MetaData()
    remove_existing_tables(engine)
    create_user_table(metadata)
    create_brand_table(metadata)
    metadata.create_all(engine)


if __name__ == "__main__":
    main()
