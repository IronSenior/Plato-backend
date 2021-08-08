import sqlalchemy as db
import os

from dotenv import load_dotenv
load_dotenv()

engine = db.create_engine(f"sqlite:///{os.environ['SQLITE_DBNAME']}")
connection = engine.connect()
metadata = db.MetaData()


def remove_existing_tables():
    sql = 'DROP TABLE IF EXISTS users;'
    engine.execute(sql)


def create_user_table():
    db.Table('users', metadata,
             db.Column('userid', db.String(36), nullable=False, primary_key=True),
             db.Column('username', db.String(255), nullable=False,),
             db.Column('email', db.String(255), nullable=False),
             db.Column('password', db.String(255), nullable=False))


if __name__ == "__main__":
    remove_existing_tables()
    create_user_table()
    metadata.create_all(engine)
